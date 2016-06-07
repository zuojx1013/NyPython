import socket
import os
from netaddr import IPNetwork,IPAddress
import time
import threading

class Sniffer():
    def __init__(self,host):
        if os.name=='nt':
            self.socket_protocol=socket.IPPROTO_IP
        else:
            self.socket_protocol=socket.IPPROTO_ICMP
        self.sniffer=socket.socket(socket.AF_INET,socket.SOCK_RAW,self.socket_protocol)
        self.sniffer.bind((host,0))
        self.sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        if os.name=='nt':
            self.sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    def read(self):
        raw_buffer=self.sniffer.recvfrom(65565)
        return raw_buffer

    def close(self):
        if os.name=='nt':
            self.sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)


def udp_sender(subnet,magic_message):
    time.sleep(2)
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message.encode(),('%s'%ip,65212))
        except:
            pass

def scanner():
    sniffer=Sniffer('10.11.184.163')
    subnet='10.11.0.0/24'
    magic_message="hello"
    t=threading.Thread(target=udp_sender,args=(subnet,magic_message))
    t.start()
    try:
        while True:
            print(sniffer.read()[1][0])
    except KeyboardInterrupt:
        print("CTRL-C")
        sniffer.close()
        t._stop()

if __name__=='__main__':
    scanner()
