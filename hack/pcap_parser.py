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

def extractImage(headers,http_payload):
    image=None
    image_type=None
    try:
        if 'image' in headers['Content-Type']:
            image_type=headers['Content-Type'].split('/')[1]
            image=http_payload[http_payload.index('\r\n\r\n')+4:]
            try:
                if 'Content-Encoding' in headers.keys():
                    if headers['Content-Encoding']=='gzip':
                        image=zlib.decompress(image,16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding']=='deflate':
                        image=zlib.decompress(image)
            except:
                pass
    except:
        return None,None
    return image,image_type

def httpAssembler(pacp_file):
    carved_images=0
    imgdir='images'
    a=rdpcap(pacp_file)
    sessions=a.sessions()
    for session in sessions:
        http_payload=''
        for packet in sessions[session]:
            try:
                if(packet[TCP].dport==80 or packet[TCP].sport==80):
                    http_payload+=str(packet[TCP].payload)
            except:
                pass
        http_payload=re.sub('\\\\r\\\\n','\\r\\n',http_payload)
        headers=getHttpHeaders(http_payload)
        if headers is None:
            continue
        print(headers)
        image,image_type=extractImage(headers,http_payload)
        if image is not None and image_type is not None:
            filename='%s-pic_%d.%s'%(pacp_file,carved_images,image_type)
            img=open('%s/%s'%(imgdir,filename),'w')
            img.write(image)
            img.close()
            carved_images+=1

httpAssembler('data.pcap')
