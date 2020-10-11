import cv2
from mss import mss   #Multiple Screen Shots
from PIL import Image #Python Image Library
import matplotlib.pyplot as plt
import numpy as np
import time

class Vision:
    def __init__(self):
        self.static_templates = {
            'test_db': 'assets/obs.png',
            'fermer' : 'assets/fermer.png',
            'gauche' : 'assets/arrow_1.png',
            'droite' : 'assets/arrow_2.png',
            'depart' : 'assets/depart.png',
            'dice' : 'assets/dice.png',
            'event' : 'assets/event.png',
            'stage_nc' : 'assets/not_clear.png',
            'quest': 'assets/quete.png',
            'types': 'assets/types.png',
            'u_star': 'assets/unfilled_star.png',
            'ok_button':'assets/ok.png',
            'terre':'assets/terre.png',
            'friend':'assets/friend.png',
            'stage_sel': 'assets/stage_sel.png',
            'stage_clear': 'assets/stage_cleared.png',
            'start': 'assets/start.png',
            'ki' : 'assets/ki.png',
            'KO' : 'assets/KO.png',
            'end': 'assets/end.png'         
        }
        
        # reading images in B&W
        self.templates = { k: cv2.imread(v, 0) for (k,v) in self.static_templates.items()}

        # Find a way to automatically compute the width and height	
        self.monitor = {'top': 0, 'left':0 , 'width' : 1920, 'height':1080}

        self.screen = mss();
        self.frame = None

    def convert_rgb_to_bgr(self,img):
        return img[:,:, ::-1]

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor) #To change to capture only interesed app
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        '''
        print("Showing image")
        cv2.imshow('Gray image', img_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        # wrong displaying
        #imgplot = plt.imshow(img)
        #plt.show()
        return img_gray

    def refresh_frame(self):
    	self.frame = self.take_screenshot()

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image with a targetted greyscaled image
        """
        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    

    def find_templates(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
            )

    def scaled_templates(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        s = 0.9
        initial_template = self.templates[name];
        while s < 1.2 :
            scaled_template = cv2.resize(initial_template, (0,0), fx = s, fy = s)
            matches = self.match_template(
                    image,
                    scaled_template,
                    threshold
                )
            if np.shape(matches)[1] >= 1:
                return matches
            s += 0.05;
        return matches

