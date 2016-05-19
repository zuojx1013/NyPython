import jieba
import os
import openpyxl
import re


def participle(data):
    jieba.enable_parallel(4)
    result=jieba.cut(data,cut_all=False)
    return result

def wordfrequency(text):
    sub_re='[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,'',text)
    result={}
    words=[word for word in participle(text)]
    for word in words:
        try:
            result[word]+=1
        except:
            result[word]=1
    return result

def loadFunctionWords():
    result=[]
    for line in open('functionwords','r'):
        result.append(line.replace('\n',''))
    return result

def main():
    functionwords=loadFunctionWords()
    for filename in os.listdir('.'):
        if filename.endswith('txt'):
            excel=openpyxl.Workbook(write_only=True)
            sheet=excel.create_sheet()
            result=wordfrequency(open(filename,'rb').read().decode('gbk','ignore'))
            result=sorted(result.items(),key=lambda x:x[1],reverse=True)
            for item in result:
                if item[0] in functionwords:
                    continue
                sheet.append(item)
            excel.save('%s.xlsx'%filename)

main()
