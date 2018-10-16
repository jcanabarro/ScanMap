from icmprequest import IcmpRequest
from hosts import Hosts
from TcpRequest import TcpRequest
import sys, os, subprocess

icmp = IcmpRequest()
tcp = TcpRequest()


if sys.argv[1] == '-network':
    ip = sys.argv[3]
    mask = sys.argv[5]
    # available_hosts = Hosts("10.81.80.0", "255.255.248.0")
    available_hosts = Hosts(ip, mask)
    hosts = available_hosts.get_available_hosts()

    alive_hosts = []

    for host in hosts:
        verify = icmp.verbose_ping(str(host), 0.125, 1)
        if verify is not None:
            alive_hosts.append(verify)

    info_host = []

    for host in alive_hosts:
        ports = tcp.scan_ports(host[0], host[1])
        info_host.append((host[0], host[1], ports))

elif sys.argv[1] == '-single':
    print(os.system("traceroute " + sys.argv[2]))
