import numpy as np
from icmprequest import IcmpRequest
from hosts import Hosts

icmp = IcmpRequest()
available_hosts = Hosts("255.255.255.0", "10.81.0.0")
available_hosts.get_available_hosts()

# median_delay = icmp.verbose_ping("10.81.121.36", 2, 100)
#
# print(np.sum(median_delay) / len(median_delay))
