import cv2
import base64
import pickle
import numpy as np
import datetime

class Utils:
    @staticmethod
    def decode(new_encoding):
        np_bytes = base64.b64decode(new_encoding)
        np_array = pickle.loads(np_bytes)
        return np_array[0]


class Canvas:
    base_cap_width = 640
    base_cap_height = 480

    #text defaults
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    font_color = (255, 255, 255)

    thick = 1
    font_size = 0.9

    def __init__(self, _class):
        self._class = _class
        self.height = Canvas.base_cap_height+120
        self.width = Canvas.base_cap_width+360

        #create an empty frame
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.frame[:] = (225, 225, 225)
        
        #add current class to frame title screen
        text = f"Class:{_class}"

        self.title_bar = np.zeros((50, self.width, 3), dtype=np.uint8)
        self.title_bar[:] = (253, 153, 11)

        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.title_bar = cv2.putText(self.title_bar, text, (10,text_height+15), self.font, self.font_size, self.font_color, self.thick,cv2.LINE_AA)    


        text = f"Face AMS"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.title_bar = cv2.putText(self.title_bar, text, (self.width//2 - text_width//2,text_height+15), self.font, self.font_size, self.font_color, self.thick,cv2.LINE_AA)

        self.update_titlebar()
    
    def update_datetime(self):
        self.clear_titlebar()

        text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.title_bar = cv2.putText(self.title_bar, text, (self.width - text_width,text_height+15), self.font, self.font_size, self.font_color, self.thick,cv2.LINE_AA)
        
        self.update_titlebar()


    def update_titlebar(self):
        self.frame[0:50] = self.title_bar


    def clear_titlebar(self):
        text = f"Class:{self._class}"

        self.title_bar = np.zeros((50, self.width, 3), dtype=np.uint8)
        self.title_bar[:] = (253, 153, 11)

        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.title_bar = cv2.putText(self.title_bar, text, (10,text_height+15), self.font, self.font_size, self.font_color, self.thick,cv2.LINE_AA)    


        text = f"Face AMS"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.title_bar = cv2.putText(self.title_bar, text, (self.width//2 - text_width//2,text_height+15), self.font, self.font_size, self.font_color, self.thick,cv2.LINE_AA)

        self.update_titlebar()
