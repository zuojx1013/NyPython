import re
import math
import json
import jieba

def participle(data):
    jieba.enable_parallel(4)
    result=jieba.cut(data,cut_all=True)
    return result

def getEngwords(doc):
    splitter=re.compile('\\W*')
    words=[word.lower() for word in splitter.split(doc) if len(word) >2 and len(word)<20]
    return dict([(word,1) for word in words])

def getChineseWords(text):
    sub_re='[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,'',text)
    words=participle(text)
    return dict([(word,1) for word in words])

class Classifier:
    def __init__(self,getfeatures,filename=None):
        self.thresholds={}
        self.fc={}
        self.cc={}
        self.getfeatures=getfeatures

    def incf(self,feature,cat):#增加对特征/分类组合的计数值
        self.fc.setdefault(feature,{})
        self.fc[feature].setdefault(cat,0)
        self.fc[feature][cat]+=1

    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1

    def setThreshold(self,cat,threshold_count):
        self.thresholds[cat]=threshold_count

    def getThreshold(self,cat):
        if cat not in self.thresholds:
            return 1
        return self.thresholds[cat]

    def featureCount(self,feature,cat):
        if feature in self.fc and cat in self.fc[feature]:
            return float(self.fc[feature][cat])
        return 0.0

    def catCount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0

    def totalCount(self):
        return sum(self.cc.values())

    def categaries(self):
        return [key for key in self.cc]

    def train(self,item,cat):
        features=self.getfeatures(item)
        for feature in features:
            self.incf(feature,cat)
        self.incc(cat)

    def featureProb(self,feature,categarie):
        if self.catCount(categarie)==0:
            return 0
        return self.featureCount(feature,categarie)/self.catCount(categarie)

    def weightedProb(self,feature,categarie,prf,weight=1.0,ap=0.5):
        basicprob=prf(feature,categarie)
        totals=sum([self.featureCount(feature,cat) for cat in self.categaries()])
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

    def loadtrainedData(self,filename):
        data=json.loads(open(filename,'r',encoding='utf-8').read())
        self.fc=data['fc']
        self.cc=data['cc']

    def saveTrainData(self,filename='traindata.json'):
        data={}
        data['fc']=self.fc
        data['cc']=self.cc
        f=open(filename,'w',encoding='utf-8')
        json.dump(data,f)
        f.close()

class NaiveBayes(Classifier):
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        p=1
        for feature in features:
            p*=self.weightedProb(feature,cat,self.featureProb)
        return p

    def prob(self,item,cat):
        catprob=self.catCount(cat)/self.totalCount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    def classify(self,item,default=None):
        max=0
        probs={}
        for cat in self.categaries():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat
        for cat in probs:
            if cat==best:
                continue
            if probs[cat]*self.getThreshold(best)>probs[best]:
                return default
        print(probs)
        return best


class FisherClassifier(Classifier):
    def __init__(self,getfeatures):
        Classifier.__init__(self,getfeatures)
        self.minimums={}

    def setminimum(self,cat,minnum):
        self.minimums[cat]=minnum

    def getminimum(self,cat):
        if cat in self.minimums:
            return self.minimums[cat]
        return 0

    def cprob(self,feature,cat):
        clf=self.featureProb(feature,cat)
        if clf==0:
            return 0
        freqnum=sum([self.featureProb(feature,cat) for cat in self.categaries()])
        p=clf/freqnum
        return p

    def fisherProb(self,item,cat):
        p=1
        features=self.getfeatures(item)
        for feature in features:
            p*=self.weightedProb(feature,cat,self.cprob)
        fscore=-2*math.log(p)
        return self.invchi2(fscore,len(features)*2)

    def invchi2(self,chi,df):#倒置对数卡方函数
        m=chi/2
        sumcount=term=math.exp(-m)
        for i in range(1,int(df/2)):
            term*=m/i
            sumcount+=term
        return min(sumcount,1)

    def classify(self,item,default=None):
        best=default
        maxnum=0
        for cat in self.categaries():
            p=self.fisherProb(item,cat)
            if p>self.getminimum(cat) and p>maxnum:
                best=cat
                maxnum=p
        return best
