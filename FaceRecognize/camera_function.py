import pygame
import pygame.camera
from pygame.locals import *
import PIL
from PIL import Image
import time


def camstream():
    DEVICE = '/dev/video0'
    SIZE = (640, 480)
    FILENAME = 'capture.png'
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    while capture:
        screen = camera.get_image(screen)
        pil_string_image = pygame.image.tostring(screen,"RGBA",False)
        im=Image.frombytes("RGBA",(640,480),pil_string_image)
        im.show()
        time.sleep(0.5)
        im.close()
        display.blit(screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_s:
                pygame.image.save(screen, FILENAME)
    camera.stop()
    pygame.quit()
    return

class Capture(object):
    def __init__(self):
        pygame.init()
        pygame.camera.init()
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)

        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    self.cam.stop()
                    going = False
            self.get_and_flip()

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

if __name__ == '__main__':
    #camstream()
    #cam=Capture()
    #cam.main()
