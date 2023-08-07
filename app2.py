from flask import Flask, render_template, url_for, request, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import random, names
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users1.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = str(random.randint(0,200))
        new_task = Todo(content=task_content, name = names.get_full_name())

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:

        tasks = Todo.query.order_by(desc(Todo.date_created)).all()
        top_names = Todo.query.order_by(desc(Todo.date_created)).all()
        top_num = Todo.query.order_by(desc(Todo.date_created)).first()
        return render_template ('index.html', tasks=tasks, top_num=top_num, top_names=top_names)

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

