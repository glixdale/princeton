from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Street_Number = db.Column(db.Integer, nullable=False)
    Street_Name = db.Column(db.String(200), nullable=False)
    Address_Line_2 = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(200), nullable=False)
    Zip = db.Column(db.Integer, nullable=False)
    State = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(10), nullable=False)
    Phone2 = db.Column(db.String(10), nullable=True)
    Phone3 = db.Column(db.String(10), nullable=True)
    Fax = db.Column(db.String(10), nullable=True)
    def __repr__(self):
        return '<Task %r>' % self.id



@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect ('/')
    except:
        return 'There was a problem deleting that task'
    
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    

if __name__=="__main__":
    app.run(debug=True)