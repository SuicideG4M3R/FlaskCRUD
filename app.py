from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from form import check_user


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def welcome_page():
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def show_users():
    context = {
        'users': User.query.all()
    }
    return render_template('index.html', context=context)


@app.route('/user/<int:id>', methods=['GET'])
def show_user(id):
    single_user = User.query.filter_by(id=id).first()
    if not single_user:
        return redirect('/users')

    if request.method == 'GET':
        context = {
            'user': single_user
        }
        return render_template('index.html', context=context)


@app.route('/user/<int:id>/delete', methods=['GET'])
def delete_user(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        if not user:
            return redirect('/users')
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    context = {
        'form': {
            'username': {'type': 'text', 'placeholder': '', 'name': 'username'},
            'email': {'type': 'email', 'placeholder': '', 'name': 'email'}
        }
    }
    if request.method == 'GET':
        return render_template('index.html', context=context)

    if request.method == 'POST':
        username = request.form.get('username').lower().capitalize()
        email = request.form.get('email').lower()

        # If receives render_template from func, returns that template, else passes
        valid = check_user(username, email, context)
        if valid:
            return valid

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            context['error'] = f'User already exists'
            return render_template('index.html', context=context)

        user = User(username=username, email=email)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            context['error'] = f'Something went wrong: {e}'
            return render_template('index.html', context=context)
        return redirect('/users')


@app.route('/generate-users', methods=['GET'])
def generate_users():
    if not User.query.first():
        names = ['alice', 'bob', 'charlie', 'david', 'eve', 'robert', 'james', 'emily']
        for i in names:
            user = User(username=i.capitalize(), email=f'{i}@example.com')
            db.session.add(user)
        db.session.commit()
        return redirect('/users')
    return 'Database already has entries'


@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return redirect('/users')
    context = {
        'form': {
            'username': {'type': 'text', 'placeholder': f'{user.username}', 'name': 'username'},
            'email': {'type': 'email', 'placeholder': f'{user.email}', 'name': 'email'}
        }
    }
    if request.method == 'GET':
        return render_template('index.html', context=context)

    if request.method == 'POST':
        new_username = request.form.get('username').lower().capitalize()
        new_email = request.form.get('email').lower()

        # If receives render_template from func, returns that template, else passes
        valid = check_user(new_username, new_email, context)
        if valid:
            return valid

        existing_username = User.query.filter(User.username == new_username, User.id != user.id).first()
        existing_email = User.query.filter(User.email == new_email, User.id != user.id).first()
        if existing_username or existing_email:
            context['error'] = f'User already exists'
            return render_template('index.html', context=context)

        try:
            user.username = new_username
            user.email = new_email
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            context['error'] = f'Something went wrong: {e}'
            return render_template('index.html', context=context)
        context['error'] = f'User successfully changed'
        return render_template('index.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
