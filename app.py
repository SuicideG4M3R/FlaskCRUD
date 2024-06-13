from flask import Flask, render_template, redirect
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


@app.route('/users')
def show_users():
    context = {
        'users': User.query.all()
    }
    return render_template('index.html', context=context)


@app.route('/create-user')
def create_user():
    return f'CREATE USER'


@app.route('/generate-users')
def generate_users():
    names = ['alice', 'bob', 'charlie', 'david', 'eve', 'robert', 'james', 'emily']
    for i in names:
        user = User(username=i.capitalize(), email=f'{i}@example.com')
        db.session.add(user)
    db.session.commit()
    return redirect('/users')


if __name__ == '__main__':
    app.run(debug=True)
