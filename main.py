from icmprequest import IcmpRequest
from hosts import Hosts
from TcpRequest import TcpRequest
import sys
import subprocess
import resource
import re


icmp = IcmpRequest()
tcp = TcpRequest()
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

if sys.argv[1] == '-network':
    ip = sys.argv[3]
    mask = sys.argv[5]
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

    with open("data.json", "a") as f:
        f.write("hosts: [\n")
        for index, host in enumerate(info_host):
            f.write("\t%d: {\n\t\tip: '%s',\n\t\tlatency: %.6s,\n\t\tport: %s\n\t},\n" % (
            index, str(host[0]), str(host[1]), str(host[2])))
        f.write("]\n")

elif sys.argv[1] == '-single':
    print("Single")
    output = subprocess.check_output("traceroute " + sys.argv[2], shell=True).decode("utf-8").split("\n")[1:-1]
    ip = ''.join(str(output[len(output) - 1:]))
    ip = ip[ip.find("(") + 1:ip.find(")")]
    ports = tcp.scan_ports(ip, 1)
    print(ports)

