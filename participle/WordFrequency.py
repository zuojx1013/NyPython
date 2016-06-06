import jieba
import os
import openpyxl
import re


def participle(data):
    jieba.set_dictionary("dict/dict.txt")
    jieba.initialize()
    result=jieba.cut(data,cut_all=False)
    return result

def wordfrequency(text):
    sub_re='[\!\/_,$%^*\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?【】“”;-]+'
    text=re.sub(sub_re,'',text)
    result={}
    words=[word for word in participle(text)]
    words=list(set(words))
    for word in words:
        if(word=='.' or word=='?' or word==' ' or word=='\n'):
            continue
        All=re.findall(word,text)
        result[word]=len(All)
    return result

def main():
    try:
        os.mkdir('result')
    except:
        pass
    for filename in os.listdir('result'):
        if filename.endswith('txt'):
            excel=openpyxl.Workbook(write_only=True)
            sheet=excel.create_sheet()
            result=wordfrequency(open('result/'+filename,'rb').read().decode('utf-8','ignore'))
            result=sorted(result.items(),key=lambda x:x[1],reverse=True)
            for item in result:
                if(item[0].replace('\n','')=='' or item[0].replace('\r\n','')==''):
                    continue
                sheet.append(item)
            excel.save('result/%s.xlsx'%filename.split('.')[0])

main()
