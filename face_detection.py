import os
from flask import Flask
import pkg_resources
import numpy as np
import cv2
import db

cascPath = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_frontalface_default.xml')


faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = ""
# if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
video_capture = cv2.VideoCapture(0)  


def camera_stream():

    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_roi_resized = cv2.resize(face_roi, (128, 128))
        image = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        for user in db.view():
            user_image = cv2.imread("static/"+user.image, cv2.IMREAD_GRAYSCALE)
            user_image_resized = cv2.resize(user_image, (128, 128))

            diff = cv2.absdiff(face_roi_resized, user_image_resized)
            similarity = np.sum(diff)

            similarity_threshold = 200000000
            
            if similarity < similarity_threshold:
                cv2.putText(image, user.name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
        # video_capture.release();
    # Display the resulting frame in browser
    return cv2.imencode('.jpg', frame)[1].tobytes()