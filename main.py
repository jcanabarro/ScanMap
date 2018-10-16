from icmprequest import IcmpRequest
from hosts import Hosts
from TcpRequest import TcpRequest

icmp = IcmpRequest()
tcp = TcpRequest()
available_hosts = Hosts("10.81.80.0", "255.255.248.0")
hosts = available_hosts.get_available_hosts()

alive_hosts = []

for host in hosts:
    verify = icmp.verbose_ping(str(host), 0.125, 1)
    if verify is not None:
        alive_hosts.append(verify)

for host, delay in alive_hosts:
    tcp.scan_ports(host, delay)
