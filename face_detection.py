import pkg_resources
import cv2
cascPath = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_frontalface_default.xml')


faceCascade = cv2.CascadeClassifier(cascPath)

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
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame in browser
    return cv2.imencode('.jpg', frame)[1].tobytes()