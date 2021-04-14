import os
import cv2
import dlib
import base64
import pickle
import sqlite3
import datetime
import argparse
import numpy as np
import pandas as pd
import face_recognition
import matplotlib.pyplot as plt
from utils import Utils

class AttendancePipeline:
    #The model directory where resnet ssd model is stored
    models_dir = os.path.join(os.path.dirname(
        os.getcwd()), "project", "base", "models")
    # Prototxt file path of the face detection model
    prototxtPath = os.path.join(
        models_dir, "Resnet_SSD_deploy.prototxt")
    # path for weights of the trained resnet ssd caffe model
    weightsPath = os.path.join(
        models_dir, "Res10_300x300_SSD_iter_140000.caffemodel")

    #load the face detection model using cv2 dnn library as caffe model
    faceNet = cv2.dnn.readNetFromCaffe(
        prototxtPath, weightsPath)

    #the directory where our project main database is stored
    db_dir = os.path.join(os.path.dirname(
        os.getcwd()), "project", "db.sqlite3")

    def __init__(self, class_based=False, cam_idx=0):
        self.conn = sqlite3.connect(self.db_dir)

        students = pd.read_sql(f"SELECT * FROM school_student WHERE study_class_id == {1}", self.conn)
        
        students["face_encoding"] = students["face_encoding"].apply(Utils.decode)
        
        users = pd.read_sql(f"SELECT * FROM account_user WHERE id in ({students['user_id'].tolist()})".replace('[','').replace(']', ''), self.conn)
        users["user_id"] = users["id"]

        self.merged = pd.merge(self.students, self.users, on='user_id')[["student_id", "face_encoding", "full_name"]]
        
        self.routines = pd.read_sql(f"SELECT * FROM school_routine WHERE _class_id = {1}", self.conn)


    def _init_db_(self):
        pass


    def run_pipeline(self):
        cap = cv2.VideoCapture(0)
        faces = []
        while True:
            ret, frame = cap.read()
            if ret:
                (h, w) = frame.shape[:2]
                frame =  cv2.flip(frame, 1)
                blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                    (104.0, 177.0, 123.0))
                faceNet.setInput(blob)
                detections = faceNet.forward()

                for i in range(0, detections.shape[2]):
                    confidence = detections[0, 0, i, 2]

                    if confidence > 0.5:
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        (startX, startY) = (max(0, startX), max(0, startY))
                        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                        
                        faceimage = frame[startY:endY, startX:endX]
                        faceimage = faceimage[:, :, ::-1]

                        faces.append(faceimage)
                        
                        face_encodings = face_recognition.face_encodings(faceimage)
                        if face_encodings:
                            student_details = get_nearest_student(face_encodings)
                            date = datetime.datetime.now()
                            current_time = date.time()
                            current_datetime = date.strftime('%Y-%m-%d %H:%M:%S')
                            routine, start_time, end_time = check_routine(current_time, date.date())
                            if routine is not None:
                                attendance = (routine, int(student_details["student_id"]), 'P', current_datetime)
                                if not attendance_exists(attendance, start_time, end_time):
                                    sql = ''' INSERT INTO school_attendance(routine_id, student_id, status, date)
                                                VALUES(?,?,?,?) '''
                                    cur = self.conn.cursor()
                                    cur.execute(sql, attendance)
                                    self.conn.commit()
                            
                            cv2.rectangle(frame, (startX, startY),
                                        (endX, endY), (255, 255, 0), 2)
                            cv2.putText(frame, student_details["full_name"], (startX, startY-40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                            cv2.putText(frame, str(student_details["student_id"]), (startX, startY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.imshow("Face AMS", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


    def get_nearest_student(self, b):
        def get_sim(a):
            return np.dot(a, b[0])/(np.linalg.norm(a)*np.linalg.norm(b[0]))
        
        return self.merged.iloc[self.merged["face_encoding"].apply(get_sim).idxmax()]

    def check_routine(self, time, date):
        for index, row in routines.iterrows():
            start_time = datetime.datetime.strptime(row["start_time"], "%H:%M:%S").time()
            end_time = datetime.datetime.strptime(row["end_time"], "%H:%M:%S").time()
            
            if time >= start_time and time <= end_time:
                return (row["id"],
                        datetime.datetime.combine(date, start_time).strftime('%Y-%m-%d %H:%M:%S'), 
                        datetime.datetime.combine(date, end_time).strftime('%Y-%m-%d %H:%M:%S'))
    
        return None, None, None

    def attendance_exists(self, attendance, start_time, end_time):
        result = pd.read_sql(f"SELECT * FROM school_attendance WHERE \
                    routine_id={attendance[0]} AND \
                    student_id = {attendance[1]} AND \
                    date BETWEEN '{start_time}' AND '{end_time}'", self.conn)
        return len(result) != 0

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--camera', required=False, type=int,
                    help='Which camera to use for attendance detection and marking', default=0)
    ap.add_argument('--class', required=False, type=int,
                    help='In which class is the camera attached', default=None)

    args = vars(ap.parse_args())

    _class_id = args["class"]
    camera_idx = args["camera"]

    if _class_id is not None:
        
