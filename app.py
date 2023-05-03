from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()
    student = Student(nickname='0000', first_name='Daryna', last_name='Hudzitska')
    db.session.add(student)
    db.session.commit()


@app.route('/')
def index():
    return 'This is server for Module 1. Sorry for the late submission('

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [{'id': student.id, 'nickname': student.nickname, 'first_name': student.first_name, 'last_name': student.last_name} for student in students]
    return jsonify(result)

@app.route('/students/<string:nickname>/token', methods=['GET'])
def get_token(nickname):
    student = Student.query.filter_by(nickname=nickname).first()
    if student:
        token = str(uuid.uuid4())
        return jsonify({'token': token})
    return jsonify({'message': 'Student not found'})


@app.route('/students', methods=['POST'])
def create_student():
    token = request.headers.get('Authorization')
    if token == app.config['SECRET_KEY']:
        data = request.get_json()
        nickname = data.get('nickname')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        student = Student(nickname=nickname, first_name=first_name, last_name=last_name)
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student created'})
    return jsonify({'message': 'Unauthorized'}), 401


if __name__ == '__main__':
    app.run(debug=True)
