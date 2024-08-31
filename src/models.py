from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class To_do(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now())
    deadline = db.Column(db.DateTime, nullable = True, default = None)


    def __repr__(self):
        return f"<Task {self.id}>"

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable = False)
    grade = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Integer, nullable = False, default = 100)