from scapy.all import *

eth = Ether(dst = "ff:ff:ff:ff:ff:ff")
arp = ARP(pdst = '198.13.13.1/16')
answered, unanswered = srp(eth/arp)

for i in range(0, len(answered)):
    print answered[i][1].psrc + " -- " + answered[i][1].hwsrc
