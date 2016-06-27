import requests
import docclass
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (Android 5.1; Mobile; rv:47.0) Gecko/47.0 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'}

def train():
    docfilter=docclass.FisherClassifier(docclass.getChineseWords)
    url={'体育':'http://channel.chinanews.com/cns/s/channel:ty.shtml?pager=%s&pagenum=20',
         '娱乐':'http://channel.chinanews.com/cns/s/channel:yl.shtml?pager=%s&pagenum=20',
         '金融':'http://channel.chinanews.com/cns/s/channel:fortune.shtml?pager=%s&pagenum=20',
         '财经':'http://channel.chinanews.com/cns/s/channel:cj.shtml?pager=%s&pagenum=20',
         '军事':'http://channel.chinanews.com/cns/s/channel:mil.shtml?pager=%s&pagenum=20',
         '国际':'http://channel.chinanews.com/cns/s/channel:gj.shtml?pager=%s&pagenum=20',
         '社会':'http://channel.chinanews.com/cns/s/channel:sh.shtml?pager=%s&pagenum=20'}
    for key in url:
        startpage=1
        while startpage<100:
            try:
                html=requests.get(url[key]%(startpage),headers=headers).text.replace(' ','')
            except:
                break
            result=re.findall('"title":"(.*?)"',html)
            for item in result:
                docfilter.train(item,key)
            print(key,startpage,'ok')
            startpage+=1
    docfilter.saveTrainData()

def test():
    docfilter=docclass.FisherClassifier(docclass.getChineseWords)
    docfilter.loadtrainedData()
    while True:
        title=input('news title:')
        categarie=docfilter.classify(title)
        print(categarie)

test()
