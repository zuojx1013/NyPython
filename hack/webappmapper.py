import queue
import threading
import os
import requests
import urllib

def buildWordlist(wordlist_file,resume=None):
    f=open(wordlist_file,'r')
    raw_words=f.readlines()
    f.close()

    found_resume=False
    words=[]

    for word in raw_words:
        word=word.rstrip()
        if resume is not None:
            if found_resume:
                words.append(word)
            else:
                if word==resume:
                    found_resume=True
                    print('Resumr wordlist from :%s '%resume)
        else:
            words.append(word)
    return words

def dirBruter(target_url,word_queue,extensions=None):
    while len(word_queue):
        attempt=word_queue.pop()
        attempt_list=[]
        if '.' not in attempt:
            attempt_list.append('/%s/'%(attempt))
        else:
            attempt_list.append('/%s'%attempt)

        if extensions:
            for extension in extensions:
                attempt_list.append('/%s%s'%(attempt,extension))
        for bruter in attempt_list:
            url='%s%s'%(target_url,urllib.parse.quote(bruter))
            try:
                print(url)
                res=requests.get(url,timeout=30)
                if len(res.text):
                    if(res.status_code==200):
                        print(res.status_code,'--',url,'\n')
            except:
                continue

def mapper():
    word_queue=buildWordlist('SVNDigger/all.txt')
    target_url='http://nyloner.cn'
    extensions=['.html','.bak','.orig','.inc']
    threads=50
    for i in range(threads):
        t=threading.Thread(target=dirBruter,args=(target_url,word_queue,extensions))
        t.start()

mapper()
