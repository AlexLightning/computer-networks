from scapy.all import *
from struct import *
import sys

ip = IP()
ip.src = '198.13.0.15' #mid1
ip.dst = '198.13.0.14' #rt1
ip.tos = int('011110' + '11', 2) #setare DSCP si ECN


tcp = TCP()
tcp.sport = 54321
tcp.dport = 10000

optiune = 'MSS'
op_index = TCPOptions[1][optiune]
op_format = TCPOptions[0][op_index]
valoare = struct.pack(op_format[1], 2)
tcp.options = [(optiune, valoare)]
tcp.flags = 'EC'# CWR si ECE

## SYN ##
tcp.seq = 100
tcp.flags = 'S' # flag de SYN
raspuns_syn_ack = sr1(ip/tcp)

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1
tcp.flags = 'A'
ACK = ip / tcp

send(ACK)

for ch in "salut, lume":
    tcp.flags = 'PAEC'
    #tcp.ack = raspuns_syn_ack.seq + 1
    print "Sent: " + ch
    rcv = sr1(ip/tcp/ch)
    rcv
    tcp.seq += 1

tcp.flags='R'
RES = ip/tcp
send(RES)
