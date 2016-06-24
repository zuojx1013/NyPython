from scapy.all import *
import time
import json
from scapy.utils import PcapReader, PcapWriter
#sniff(filter="",iface='any',prn=function,count=N)

def getHttpHeaders(http_payload):
    try:
        headers=dict(re.findall(r'\r\n(.*?): (.*?)\r\n',http_payload))
        if headers=={}:
            return None
    except:
        return None
    return headers

def baseInfor(packet,data):
    try:
        baseinfor='%s<==>%s\n'%(packet[IP].dst,packet[IP].src)
    except:
        baseinfor=''
    baseinfor+=data.split('\r\n\r\n')[0]
    return baseinfor

def getUser(packet,baseinfor):
    f=open('userdata.txt','a')
    f.write(baseinfor+'\n')
    f.write("Data:{}".format(packet[IP].payload)+'\n\n\n')
    f.close()

def packet_callback(packet):
    try:
        statue=packet[TCP].load
    except:
        return
    data=packet[TCP].load.decode('utf-8','ignore')
    headers=getHttpHeaders(data)
    if headers==None:
        return
    baseinfor=baseInfor(packet,data)
    print(baseinfor,'\n-----')
    passwd_packet=str(packet[TCP].payload)
    if  'password' in passwd_packet.lower() or 'passwd' in passwd_packet.lower() or 'username' in passwd_packet.lower():
        getUser(packet,baseinfor)
    '''
    writer=PcapWriter('data.pcap', append = True)
    writer.write(packet)
    writer.flush()
    writer.close()
    '''

while True:
    try:
        packets=sniff(filter='',prn=packet_callback,count=10000)
    except KeyboardInterrupt:
        pcapname=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        wrpcap('pcap/%s.pcap'%pcapname,packets)
        break
    pcapname=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    wrpcap('pcap/%s.pcap'%pcapname,packets)
