from camera_ui import Ui_MainWindow
import pygame
import pygame.camera
from pygame.locals import *
import PIL
from PIL import Image,ImageQt,ImageDraw,ImageFont
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import numpy as np
import math
from facerecognize import FaceRecognize
import time


class CameraImage():
    def __init__(self):
        pygame.camera.init()
        self.cam=pygame.camera.Camera(pygame.camera.list_cameras()[0],(640,480))
        self.cam.start()

    def get_PIL_image(self):
        webcamImage = self.cam.get_image()
        pil_string_image = pygame.image.tostring(webcamImage,"RGBA",False)
        img=Image.frombytes("RGBA",(640,480),pil_string_image)
        return img

class Camera(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Camera,self).__init__()
        self.setupUi(self)
        self.timeid=self.startTimer(200)
        self.camera_image=CameraImage()
        self.setting_init()
        self.font=ImageFont.truetype('GB2312.ttf',24)
        self.facerecognize=FaceRecognize()
        self.facerecognize.load_trained_data('facedata.json')

    def setting_init(self):
        self.action.triggered.connect(self.appclose)

    #计算该像素是肤色的概率
    def calculate(self,x):
        x=np.matrix(x)
        m=np.matrix([156.5599,117.4361])
        C=np.matrix([[299.4574,12.1430],[12.1430,160.130]])
        result=(-0.5)*(x-m)*(C.I)*(x-m).T
        return math.exp(result)

    #需要改进
    def get_facearea(self,x_value,y_value):
        x_min=255
        x_max=0
        y_min=255
        y_max=0
        for key in x_value:
            if x_value[key]<10:
                continue
            if key<x_min:
                x_min=key
            if key>x_max:
                x_max=key

        for key in y_value:
            if y_value[key]<10:
                continue
            if key>y_max:
                y_max=key
            if key<y_min:
                y_min=key
        return [x_min,y_min,x_max,y_max]


    def get_face(self,image):
        image2=image.convert('YCbCr')
        image2=image2.resize((int(image.size[0]/10),int(image.size[1]/10)),Image.ANTIALIAS)
        x_value={}
        y_value={}
        for x in range(image2.size[0]):
            for y in range(image2.size[1]):
                pix=image2.getpixel((x,y))
                CrCb=[pix[2],pix[1]]
                value=self.calculate(CrCb)
                if value>0.4:
                    try:
                        x_value[x]+=1
                    except:
                        x_value[x]=1
                    try:
                        y_value[y]+=1
                    except:
                        y_value[y]=1
        area=self.get_facearea(x_value,y_value)
        face=image.crop([x*10 for x in area])
        '''
        face.save('faces/%s.jpg'%(time.strftime("%Y%m%d_%H%M%S",time.localtime())))4
        '''
        recog_result=self.facerecognize.compare(face)
        result="你谁呀？"
        for key in recog_result:
            if recog_result[key]<500:
                result=key
        draw=ImageDraw.Draw(image)
        draw.text((int((area[0]+area[2])/2)*10,area[3]*10-50),result,font=self.font,fill='#111111')
        draw.rectangle([x*10 for x in area])
        return image

    def train(self):
        import os
        for filename in os.listdir('faces'):
            image=Image.open('faces/%s'%filename)
            self.facerecognize.train(image,'boss')
        self.facerecognize.save_trained_data('facedata.json')

    def timerEvent(self,event):
        image=self.camera_image.get_PIL_image()
        image=image.transpose(Image.FLIP_LEFT_RIGHT)#左右镜像
        image=self.get_face(image)
        image=ImageQt.ImageQt(image)
        self.imagelabel.setPixmap(QPixmap.fromImage(image))

    def appclose(self):
        self.camera_image.cam.stop()
        self.close()

if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    cam=Camera()
    cam.show()
    sys.exit(app.exec_())
