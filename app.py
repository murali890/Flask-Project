from flask import Flask, render_template, request, redirect,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    task= db.Column(db.String(100))
    date= db.Column(db.DateTime)
    
    
    
@app.route('/')
def index():
    get_data= Todo.query.all()

    return render_template("index.html",title="TODO APP",getdata=get_data)

@app.route('/add/',methods=['POST'])
def add():
    data= request.form['task']
    print("task data",data)
    todo = Todo(task=data,date=datetime.now())
   
    
    db.session.add(todo)
    print("date",todo)

    db.session.commit()

    return redirect(('/'))

@app.route('/delete/<id>/')

def delete(id):
    try:
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return abort(404)


@app.route('/update/<id>/',methods=['GET','POST'])
def update(id):
    tos = Todo.query.get(id)
    if request.method == 'POST':
        tos.task = request.form['task']
        db.session.commit()
        print(request.form)
        return redirect('/')
    else:
        
        get_data= Todo.query.all()
        return render_template("index.html",updatetodo=tos,title="TODO APP",getdata=get_data)





if __name__ == '__main__':
    app.run(debug=True)