import os
import cv2
import pickle
import base64
import sqlite3
import datetime
import numpy as np
import pandas as pd

class BaseUtils:
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

    #the directory where our project main database is stored
    db_dir = os.path.join(os.path.dirname(
        os.getcwd()), "project", "db.sqlite3")


    def __init__(self, _class):
        self._class = _class
        self.height = Canvas.base_cap_height+50
        self.width = Canvas.base_cap_width+400

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

    def update_routine(self, subject_id, start_time, end_time):
        self.routine_box = np.zeros((150, 400, 3), dtype=np.uint8)
        self.routine_box[:] = (216, 216, 222)

        text = "Current Routine"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.routine_box = cv2.putText(self.routine_box, text, (200 - text_width//2,text_height+10), self.font, self.font_size, (0,0,0), self.thick,cv2.LINE_AA)

        th = text_height+20

        conn = sqlite3.connect(self.db_dir)
        subject = pd.read_sql(f"SELECT * FROM school_subject where id = {subject_id}", conn)["name"].tolist()[0]

        text = f"Subject: {subject}"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.routine_box = cv2.putText(self.routine_box, text, (10,th+text_height+15), self.font, self.font_size, (0,0,0), self.thick,cv2.LINE_AA)
        
        th += text_height+15

        text = f"Start time: {start_time}"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.routine_box = cv2.putText(self.routine_box, text, (10,th+text_height+15), self.font, self.font_size, (0,0,0), self.thick,cv2.LINE_AA)
        
        th += text_height+15

        text = f"End time: {end_time}"
        (text_width, text_height) = cv2.getTextSize(text, self.font, self.font_size, self.thick)[0]
        self.routine_box = cv2.putText(self.routine_box, text, (10,th+text_height+15), self.font, self.font_size, (0,0,0), self.thick,cv2.LINE_AA)

        self.update_routinebox()

    def update_recognizedlist(self):
        self.recognizedlist_box = np.zeros((330, 400, 3), dtype=np.uint8)
        self.recognizedlist_box[:] = (165, 163, 163)



        self.update_recognizedlistbox()

    
    def update_camframe(self, frame):
        self.frame[50:, 400:] = frame
        

    def update_titlebar(self):
        self.frame[0:50] = self.title_bar

    
    def update_routinebox(self):
        self.frame[50:200, :400] = self.routine_box

    
    def update_recognizedlistbox(self):
        self.frame[200:530, :400] = self.recognizedlist_box


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
