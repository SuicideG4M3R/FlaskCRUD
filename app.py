from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


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


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    context = {
        'form': {
            'username': 'text',
            'email': 'email'
        }
    }
    if request.method == 'GET':
        return render_template('index.html', context=context)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        if not username or not email:
            context['error'] = 'Username and email are required'
            return render_template('index.html', context=context)
        if User.query.filter_by(username=username).first():
            context['error'] = f'User with username {username} already exists'
            return render_template('index.html', context=context)
        if not len(username) >= 3:
            context['error'] = 'Username must be at least 3 characters'
            return render_template('index.html', context=context)
        if '@' not in email:
            context['error'] = 'Email must contain @'
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


if __name__ == '__main__':
    app.run(debug=True)
