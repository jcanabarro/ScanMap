import numpy as np
from icmprequest import IcmpRequest

icmp = IcmpRequest()

median_delay = icmp.verbose_ping("10.81.121.36", 2, 10)

print(np.sum(median_delay) / len(median_delay))

