from flask import request, render_template, redirect, session, url_for
from app import my_app, db
from app.models.user import User

@my_app.route('/')
def index():
    name = 'Murphy Ijemba'
    return render_template('hello.html', name=name)

@my_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        query = db.query(User).filter(
            User.username == request.form.get('username')
        )
        user = query.first()
        if user.check_password(request.form.get('password')):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))

@my_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            username=request.form.get('username')
        )
        user.set_password(request.form.get('password'))
        db.add(user)
        db.commit()
        return redirect(url_for('login'))

@my_app.route('/logout')
def logout():
    session.pop('username', None)
    redirect(url_for('login'))
