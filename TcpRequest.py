import socket, threading


class TcpRequest:

    def __TCP_connect(self, ip, port_number, delay, output):
        s = socket.socket()
        s.settimeout(delay)
        try:
            s.connect((ip, port_number))
            output.append(port_number)
        except (socket.error, socket.herror, socket.timeout, socket.gaierror):
            pass
        finally:
            s.close()

    def scan_ports(self, host_ip, delay):
        available_ports = []
        for i in range(1, 65):
            threads = []
            for port in range(i, 1024 + i):
                thread = threading.Thread(target=self.__TCP_connect, args=(host_ip, port, delay * 1.5, available_ports,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

        return available_ports
