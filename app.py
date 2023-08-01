from flask import Flask, request, jsonify, render_template, redirect, Response
from person import Person;
import db
import os, random, datetime
from face_detection import camera_stream

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'

if not os.path.isfile('person.db'):
    db.create_table()

def generateRandomInt():
    return random.randrange(1000, 9999, 4)

def uploadFile(file):
    try:
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, UPLOAD_FOLDER)
        if(os.path.exists(final_directory) == False):
            os.makedirs(final_directory)
        ext = file.filename.split(".")[1]
        fileName = str(datetime.datetime.now().timestamp()).replace(".", "")
        fileName = fileName+ "."+ext
        path = os.path.join(UPLOAD_FOLDER, fileName)
        file.save(path)
        return fileName
    except :
        print("An exception occurred")

@app.route("/")
def index():
    users = db.view()
    return render_template("index.html", users=users)

@app.route("/create",  methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        fileName = ""
        if request.files['image']:
            fileName = uploadFile(request.files['image'])
        print(fileName)
        person = Person(generateRandomInt(), request.form['name'],request.form['age'], request.form['email'], fileName)
        db.insert(person)     
        return redirect("/")
    return render_template("create.html")

@app.route("/save", methods=('GET', 'POST'))
def delete():
    db.deleteAll()
    return redirect("/")

def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # concate frame one by one and show result
        
@app.route("/video_stream")
def video_stream():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()