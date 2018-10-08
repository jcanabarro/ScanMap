import ipaddress
import math


def str_to_int(vec):
    return int(vec, base=2)


def fill_zeros(b):
    number_of_zeros = 8 - len(b)
    return '0' * number_of_zeros + b


def address2bin(addr):
    return ''.join([fill_zeros(bin(int(n))[2:]) for n in addr.split('.')])


def bin2address(b):
    parts = [b[:8], b[8:16], b[16:24], b[24:32]]
    print(parts)
    return '.'.join([str(int(p, 2)) for p in parts])


class Hosts:

    def __init__(self, ip, mask):
        self.mask = mask
        self.ip = ip
        self.binary_mask = address2bin(self.mask)
        self.binary_ip = address2bin(self.ip)

    def get_available_hosts(self):
        ip_address = math.log((2 ** 32) - str_to_int(self.binary_mask) - 1) / math.log(2)
        return list(ipaddress.ip_network(self.ip + '/' + str(32 - round(ip_address))))
