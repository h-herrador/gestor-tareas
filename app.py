from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

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


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        deadline = request.form.get('deadline') # siempre devuelve None
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d') 
        except:
            deadline = None

        new_task = To_do(content = task_content, deadline = deadline)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return "There has been an issue adding your task"

    else:
        tasks = To_do.query.order_by(To_do.date_created).all()
        return render_template('index.html', tasks = tasks)
    

@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():
    return redirect('/')


@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    task_to_delete = To_do.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There has been an issue deleting your task"
    

@app.route('/tasks/update/<int:id>', methods = ['GET', 'POST'])
def update_task(id):
    task = To_do.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            task.deadline = datetime.strptime(request.form.get('deadline'), '%Y-%m-%d')
        except:
            task.deadline = None
        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return "There has been an issue updating your task"
    else:
        return render_template('update.html', task = task)

@app.route('/marks', methods = ['POST', 'GET'])
def marks():
    if request.method == 'POST':
        subject = request.form['subject']
        grade = request.form['grade']
        weight = request.form.get('weight')
        if not weight:
            weight = 100
        else:
            try:
                weight = int(weight)
            except:
                weight = 100

        new_mark = Marks(subject = subject, grade = grade, weight = weight)
        
        try:
            db.session.add(new_mark)
            db.session.commit()
            return redirect('/marks')
        
        except:
            return "There has been an issue adding your mark"

    
    else:
        marks = Marks.query.order_by(Marks.id).all()
        return render_template('marks/marks.html', marks = marks, subjects = ["AL", "FC"])
    
@app.route('/marks/delete/<int:id>')
def delete_mark(id):
    mark_to_delete = Marks.query.get_or_404(id)
    try:
        db.session.delete(mark_to_delete)
        db.session.commit()
        return redirect('/marks')
    except:
        return "There has been an issue deleting your mark"
    
@app.route('/marks/update/<int:id>', methods = ['GET', 'POST'])
def update_mark(id):
    mark = Marks.query.get_or_404(id)
    if request.method == 'POST':
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        weight = request.form.get('weight')
        grade, weight = float(grade), int(weight)
        
        mark.subject, mark.grade, mark.weight = subject, grade, weight
        try:
            db.session.commit()
            return redirect('/marks')
        except:
            return "There has been an issue updating your mark"
    else:
        return render_template('marks/update.html', mark = mark, subjects = ["FC", "AL"])



if __name__ == "__main__":
    app.run(debug = True)