import socket, threading


class TcpRequest:

    def __TCP_connect(self, ip, port_number, delay, output):
        TCPsock = socket.socket()
        TCPsock.settimeout(delay)
        try:
            TCPsock.connect((ip, port_number))
            output[port_number] = 'Listening'

        except:
            output[port_number] = ''

    def scan_ports(self, host_ip, delay):
        threads = []
        output = {}

        # Spawning threads to scan ports
        for i in range(1000):
            t = threading.Thread(target=self.__TCP_connect, args=(host_ip, i, delay * 1.5, output))
            threads.append(t)

        # Starting threads
        for i in range(1000):
            threads[i].start()

        # Locking the script until all threads complete
        for i in range(1000):
            threads[i].join()

        print('Checking [%s] available ports: [ ' % host_ip, end="")
        # Printing listening ports from small to large
        for i in range(1000):
            if output[i] == 'Listening':
                print(str(i) + ' ', end="")
        print(']')
