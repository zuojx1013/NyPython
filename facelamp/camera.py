from camera_ui import Ui_MainWindow
import pygame
import pygame.camera
from pygame.locals import *
import PIL
from PIL import Image
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap

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
        self.timeid=self.startTimer(100)
        self.camera_image=CameraImage()
        self.setting_init()

    def setting_init(self):
        self.action.triggered.connect(self.appclose)

    def timerEvent(self,event):
        image=self.camera_image.get_PIL_image()
        image.save('temp.jpg')
        path=QPixmap('./temp.jpg')
        self.imagelabel.setPixmap(path)

    def appclose(self):
        self.camera_image.cam.stop()
        self.close()

if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    cam=Camera()
    cam.show()
    sys.exit(app.exec_())
