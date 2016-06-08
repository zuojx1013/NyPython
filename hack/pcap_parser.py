import re
import zlib
from scapy.all import *


def getHttpHeaders(http_payload):
    try:
        headers=dict(re.findall(r'\r\n([A-Za-z]{2,}.*?\w): (.*?)\r\n',http_payload))
        if headers=={}:
            return None
    except:
        return None
    return headers

def extractImage(headers,data):
    image=None
    image_type=None
    try:
        if 'image' in headers['Content-Type']:
            image_type=headers['Content-Type'].split('/')[1]
            startindex=None
            endindex=None
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
    except:
        return None,None
    return image,image_type

def httpAssembler(pacp_file):
    carved_images=0
    imgdir='images'
    a=rdpcap(pacp_file)
    sessions=a.sessions()
    for session in sessions:
        http_payload=b''
        for packet in sessions[session]:
            try:
                if(packet[TCP].dport==80 or packet[TCP].sport==80):
                    http_payload+=bytes(packet[TCP].payload)
            except:
                pass
        headers=getHttpHeaders(http_payload.decode('utf-8','ignore'))
        if headers is None:
            continue
        print(headers)
        image,image_type=extractImage(headers,http_payload)
        if image is not None and image_type is not None:
            filename='%s-pic_%d.%s'%(pacp_file,carved_images,image_type)
            img=open('%s/%s'%(imgdir,filename),'wb')
            img.write(image)
            img.close()
            carved_images+=1

httpAssembler('data.pcap')
