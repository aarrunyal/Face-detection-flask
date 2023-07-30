from flask import Flask, request, jsonify, render_template, redirect
from person import Person;
import db
import os, random, datetime

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

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    person = Person("", data.name,data.age, data.email, data.image)
    db.insert(person)
    return jsonify({
                'status': '200',
                'msg': 'Success creating a new person!'
            })

@app.route('/user', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [Person.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all books in library!'
                })
        return jsonify({
            'error': f"Error! Book with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting all persons!',
                    'no_of_books': len(bks)
                })


if __name__ == '__main__':
    app.run(debug=True)