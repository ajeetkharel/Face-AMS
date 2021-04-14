import numpy as np
import cv2
import os
import face_recognition
import argparse
import sqlite3

models_dir = os.path.join(os.path.dirname(
    os.getcwd()), "project", "base", "models")
prototxtPath = os.path.join(
    models_dir, "Resnet_SSD_deploy.prototxt")
weightsPath = os.path.join(
    models_dir, "Res10_300x300_SSD_iter_140000.caffemodel")
faceNet = cv2.dnn.readNetFromCaffe(
    prototxtPath, weightsPath)

db_dir = os.path.join(os.path.dirname(
    os.getcwd()), "project", "db.sqlite3")
    

def run_strean(cam_idx):
    cap = cv2.VideoCapture(cam_idx)
    while True:
        ret, frame = cap.read()
        if ret:
            (h, w) = frame.shape[:2]
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

                    cv2.rectangle(frame, (startX, startY),
                                  (endX, endY), (255, 255, 0), 2)
                    face = frame[startY:endY, startX:endX]
                    encoding = face_recognition.face_encodings(np.array(face))

                    # np_bytes = base64.b64decode(model.np_field)
                    # np_array = pickle.loads(np_bytes)

            cv2.imshow("Face AMS", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--camera', required=False, type=int,
                    help='Which camera to use for attendance detection and marking', default=0)
    ap.add_argument('--class', required=False, type=int,
                    help='In which class is the camera attached', default=1)

    args = vars(ap.parse_args())

    _class_id = args["class"]
    camera_idx = args["camera"]

    # run_strean(camera_idx)
    conn = sqlite3.connect(db_dir)

    c = conn.cursor()

    c.execute('''
                 SELECT * FROM sqlite_master WHERE type='table'; ''')
    
    print(c.fetchall())
    
    conn.close()