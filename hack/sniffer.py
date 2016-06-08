from scapy.all import *
import time
import json
from scapy.utils import PcapReader, PcapWriter
#sniff(filter="",iface='any',prn=function,count=N)

header_list=['content-encoding','Referer', 'Date', 'Host','Accept-Encoding','User-Agent','Link','User-agent', 'Set-Cookie','Content-Type','Server_IP','Accept-Language','Cookie','Content-type','Content-Encoding']

def getHttpHeaders(http_payload):
    try:
        headers=dict(re.findall(r'\r\n([A-Za-z]{2,}.*?\w): (.*?)\r\n',http_payload))
        if headers=={}:
            return None
    except:
        return None
    return headers

def getUser(packet,headers):
    try:
        baseinfor=baseInfor(packet,headers)
    except:
        return
    f=open('userdata.txt','a')
    f.write(baseinfor)
    f.write("Data:{}".format(packet[IP].payload)+'\n\n\n')
    f.close()

def getImage(packet,headers):
    data=packet[TCP].load
    data=bytes(data)
    image_type=headers['Content-Type'].split('/')[1]
    startindex=None
    endindex=None
    image=None
    if image_type=='png' or image_type=='PNG':
        for index in range(len(data)):
            try:
                if data[index]==0x89 and data[index+1]==0x50 and data[index+2]==0x4e and data[index+3]==0x47:
                    startindex=index
            except:
                break
        if startindex==None:
            return
        image=data[startindex:]
    if image_type=='jpeg':
        for index in range(len(data)):
            try:
                if data[index]==0xff and data[index+1]==0xd8:
                    startindex=index
            except:
                break
        if startindex==None:
            return
        image=data[startindex:]
    if image==None:
        return
    imgname=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    img=open('images/%s.%s'%(imgname,image_type),'wb')
    img.write(image)
    img.close()

def getJson(packet,headers):
    data=packet.payload
    startindex=None
    for index in len(data):
        try:
            if data[index]==13 and data[index+1]==10 and data[index+2]==13 and data[index+3]==10:
                startindex=index
        except:
            break
    if startindex==None:
        return
    jsondata=data[startindex:]
    encoding=None
    content_type=headers['Content-Type'].split(';')
    for item in content_type:
        if 'charset' in item:
            encoding=item.replace('charset=','')
    if encoding==None:
        encoding='utf-8'
    jsondata=jsondata.decode(encoding,'ignore')
    try:
        jsondata=json.loads(jsondata)
    except:
        pass
    writetext=baseInfor(packet,headers)
    writetext+='----\n'
    try:
        for key in jsondata:
            if jsondata[key]=='':
                continue
            writetext+=key+':'+jsondata[key]+'\n'
    except:
        writetext+='%s'%jsondata+'\n\n\n'
    f=open('json.txt','a',encoding='utf-8')
    f.write(writetext)
    f.close()

def baseInfor(packet,headers):
    baseinfor='%s<==>%s\n'%(packet[IP].dst,packet[IP].src)
    for key in header_list:
        try:
            item=headers[key]
            if item=='':
                continue
            baseinfor+=key+': '+item+'\n'
        except:
            continue
    return baseinfor

def getLink(packet,headers):
    data=packet.payload
    startindex=None
    endindex=None
    for index in len(data):
        try:
            if data[index]==b'P' and data[index+1]==b'O' and data[index+2]==b'S' and data[index+3]==b'T':
                startindex=index
            if data[index]==b'G' and data[index+1]==b'E' and data[index+2]==b'T':
                startindex=index
            if data[index]==b'H' and data[index+1]==b'T' and data[index+2]==b'T' and data[index+3]==b'P':
                endindex=index
        except:
            break

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
        getUser(packet,headers)
    try:
        if 'image' in headers['Content-Type']:
            getImage(packet,headers)
    except:
        pass
    try:
        if 'application/json' in headers['Content-Type']:
            getJson(packet,headers)
    except:
        pass
    try:
        baseinfor=baseInfor(packet,headers)
        print(baseinfor)
    except:
        pass
    writer=PcapWriter('data.pcap', append = True)
    writer.write(packet)
    writer.flush()
    writer.close()

sniff(filter='',prn=packet_callback,count=100000)
