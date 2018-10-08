from icmprequest import IcmpRequest
from hosts import Hosts
import socket, threading


def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''


def scan_ports(host_ip, delay):
    threads = []  # To run TCP_connect concurrently
    output = {}  # For printing purposes

    # Spawning threads to scan ports
    for i in range(1000):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    # Starting threads
    for i in range(1000):
        threads[i].start()

    # Locking the script until all threads complete
    for i in range(1000):
        threads[i].join()

    # Printing listening ports from small to large
    for i in range(1000):
        if output[i] == 'Listening':
            print(str(i) + ': ' + output[i])


icmp = IcmpRequest()
available_hosts = Hosts("10.81.0.0", "255.255.255.0")
hosts = available_hosts.get_available_hosts()

alive_hosts = []

for host in hosts:
    verify = icmp.verbose_ping(str(host), 0.125, 1)
    if verify is not None:
        alive_hosts.append(verify)

alive_hosts.pop(0)

for host in alive_hosts:
    scan_ports(host, 2)
