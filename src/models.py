from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class To_do(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now())
    deadline = db.Column(db.DateTime, nullable = True, default = None)
    

class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)


class Marks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject_id = db.Column(db.String(200), db.ForeignKey(Subjects.id), nullable = False)
    grade = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Integer, default = 100)

    subject = db.relationship('Subjects', backref = db.backref('marks', lazy = True))