from PIL import Image
import json
import math

def image_lbp(image):
    image=image.convert('L')
    result=Image.new('L',image.size,255)
    for x in range(1,image.size[0]-1):
        for y in range(1,image.size[1]-1):
            pixes=[]
            dealmap=[(0,0),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
            for item in dealmap:
                pixes.append(image.getpixel((x+item[0],y+item[1])))
            LBPvalue=0
            for index in range(8):
                LBPvalue+=(pixes[index+1]>pixes[0])<<(8-index-1)
            result.putpixel((x,y),LBPvalue)

            '''
            #等价模式
            temp=(LBPvalue<<1)|(LBPvalue>>7)
            temp=bin(temp&LBPvalue)
            if temp.count('1')<=2:
                result.putpixel((x,y),LBPvalue)
            else:
                result.putpixel((x,y),255)
            '''

            '''
            #旋转不变
            temps=[]
            for i in range(8):
                temp=(LBPvalue<<i)|(LBPvalue>>(8-i))
                temps.append(temp)
            result.putpixel((x,y),min(temps))
            '''
            #等价 and 旋转不变
            temp=(LBPvalue<<1)|(LBPvalue>>7)
            temp=bin(temp&LBPvalue)
            if temp.count('1')<=2:
                LBP_temps=[]
                for i in range(8):
                    LBP_temp=(LBPvalue<<i)|(LBPvalue>>(8-i))
                    LBP_temps.append(LBP_temp)
                result.putpixel((x,y),min(LBP_temps))
            else:
                result.putpixel((x,y),0)

    LBP_histogram=[0 for i in range(256)]
    for x in range(1,result.size[0]):
        for y in range(1,result.size[1]):
            pix=result.getpixel((x,y))
            LBP_histogram[pix]+=1
    return LBP_histogram


class FaceRecognize():
    def __init__(self):
        self.typedata={}
        self.load_trained_data()

    def train(self,image,label):
        image_his=image_lbp(image)
        try:
            self.typedata[label].append(image_his)
        except:
            self.typedata[label]=[image_his]

    def save_trained_data(self,filename="trained_data.json"):
        try:
            f=open(filename,'w',encoding='utf-8')
        except:
            print("Open file failed!")
            return
        json.dump(self.typedata,f)
        f.close()

    def load_trained_data(self,filename="trained_data.json"):
        try:
            data=json.loads(open(filename,'r',encoding='utf-8').read())
        except:
            print("Load trained data failed!")
            return
        self.typedata=data

    def chi_square_statistic(self,his_one,his_two):
        result=0
        for index in range(256):
            try:
                result+=(his_one[index]-his_two[index])**2/(his_one[index]+his_two[index])
            except:
                continue
        return result

    def compare(self,image):
        his=image_lbp(image)
        compare_result={}
        for key in self.typedata:
            count=0
            compare_value=0
            for img in self.typedata[key]:
                compare_value+=self.chi_square_statistic(his,img)
                count+=1
            compare_result[key]=compare_value/count
        return compare_result

def train():
    import os
    facerecognize=FaceRecognize()
    for imgname in os.listdir('faces'):
        image=Image.open('faces/%s'%imgname)
        facerecognize.train(image,'face')
    facerecognize.save_trained_data()


if __name__=="__main__":
    train()
    facerecognize=FaceRecognize()
    while True:
        imgpath=input("Input img path:")
        try:
            img=Image.open(imgpath)
        except:
            print('Open Failed!')
            continue
        result=facerecognize.compare(img)
        print(result)
