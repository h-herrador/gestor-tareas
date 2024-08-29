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
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = To_do.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There has been an issue adding your task"
    

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
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


if __name__ == "__main__":
    app.run(debug = True)