import os, sys, socket, struct, select, time

"""
    A pure python ping implementation using raw socket.


    Note that ICMP messages can only be sent from processes running as root.


    Derived from ping.c distributed in Linux's netkit. That code is
    copyright (c) 1989 by The Regents of the University of California.
    That code is in turn derived from code written by Mike Muuss of the
    US Army Ballistic Research Laboratory in December, 1983 and
    placed in the public domain. They have my thanks.

    Bugs are naturally mine. I'd be glad to hear about them. There are
    certainly word - size dependenceies here.

    Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.

    Original Version from Matthew Dixon Cowles:
      -> ftp://ftp.visi.com/users/mdc/ping.py

    Rewrite by Jens Diemer:
      -> http://www.python-forum.de/post-69122.html#69122


    Revision history
    ~~~~~~~~~~~~~~~~

    March 11, 2010
    changes by Samuel Stauffer:
    - replaced time.clock with default_timer which is set to
      time.clock on windows and time.time on other systems.

    May 30, 2007
    little rewrite by Jens Diemer:
     -  change socket asterisk import to a normal import
     -  replace time.time() with time.clock()
     -  delete "return None" (or change to "return" only)
     -  in checksum() rename "str" to "source_string"

    November 22, 1997
    Initial hack. Doesn't do much, but rather than try to guess
    what features I (or others) will want in the future, I've only
    put in what I need now.

    December 16, 1997
    For some reason, the checksum bytes are in the wrong order when
    this is run under Solaris 2.X for SPARC but it works right under
    Linux x86. Since I don't know just what's wrong, I'll swap the
    bytes always and then do an htons().

    December 4, 2000
    Changed the struct.pack() calls to pack the checksum and ID as
    unsigned. My thanks to Jerome Poincheval for the fix.

    Januari 27, 2015
    Changed receive response to not accept ICMP request messages.
    It was possible to receive the very request that was sent.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: $
    $Rev: $
    $Author: $
"""


class IcmpRequest:

    def __init__(self):
        self.default_timer = 0
        if sys.platform == "win32":
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
        self.ICMP_ECHO_REQUEST = 8
        self.delay = 0
        self.answer = 0

    def checksum(self, source_string):
        sum = 0
        countTo = (len(source_string) / 2) * 2
        count = 0
        while count < countTo:
            sum = sum + source_string[count + 1] * 256 + source_string[count]
            sum = sum & 0xffffffff
            count = count + 2

        if countTo < len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        self.answer = ~sum
        self.answer = self.answer & 0xffff

        self.answer = self.answer >> 8 | (self.answer << 8 & 0xff00)

        return self.answer

    def receive_one_ping(self, my_socket, ID, timeout):
        """
        receive the ping from the socket.
        """
        timeLeft = timeout
        while True:
            startedSelect = self.default_timer()
            whatReady = select.select([my_socket], [], [], timeLeft)
            howLongInSelect = (self.default_timer() - startedSelect)
            if not whatReady[0]:  # Timeout
                return

            timeReceived = self.default_timer()
            recPacket, addr = my_socket.recvfrom(1024)
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader
            )
            if type != 8 and packetID == ID:
                bytesInDouble = struct.calcsize("d")
                timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
                return timeReceived - timeSent

            timeLeft = timeLeft - howLongInSelect
            if timeLeft <= 0:
                return

    def send_one_ping(self, my_socket, dest_addr, ID):
        """
        Send one ping to the given >dest_addr<.
        """
        dest_addr = socket.gethostbyname(dest_addr)

        my_checksum = 0

        header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytesInDouble = struct.calcsize("d")
        data = (192 - bytesInDouble) * "Q"
        data = struct.pack("d", self.default_timer()) + str.encode(data)

        my_checksum = self.checksum(header + data)

        header = struct.pack(
            "bbHHh", self.ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
        )
        packet = header + data
        my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1

    def do_one(self, dest_addr, timeout):
        """
        Returns either the delay (in seconds) or none on timeout.
        """
        icmp = socket.getprotobyname("icmp")
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as errno:
            if errno == 1:
                # Operation not permitted
                msg = (
                    " - Note that ICMP messages can only be sent from processes"
                    " running as root."
                )
                raise socket.error(msg)
            raise  # raise the original error

        my_ID = os.getpid() & 0xFFFF

        self.send_one_ping(my_socket, dest_addr, my_ID)
        delay = self.receive_one_ping(my_socket, my_ID, timeout)

        my_socket.close()
        return delay

    def verbose_ping(self, dest_addr, timeout, count):
        """
        Send >count< ping to >dest_addr< with the given >timeout< and display
        the result.
        """
        median_delay = []
        for i in range(count):
            # print("ping %s..." % dest_addr, end=' ')
            try:
                self.delay = self.do_one(dest_addr, timeout)
            except socket.gaierror:
                # print("failed. (socket error)")
                break

            if self.delay is None:
                # print("failed. (timeout within %ssec.)" % timeout)
                pass
            else:
                self.delay = self.delay * 1000
                median_delay.append(self.delay)
                # print("get ping in %0.4fms" % self.delay)
                return dest_addr
        # print()
        return None
