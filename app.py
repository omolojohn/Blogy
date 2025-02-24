from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from server import create_app, db
from server.forms import RegistrationForm
from server.forms import LoginForm
from server.models import User
from config import Config
from werkzeug.security import check_password_hash


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data,
            phone=form.phone.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id 
            flash('Login successful!', 'success')
            return redirect(url_for('post'))

        flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)

@app.route("/post")
def post():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True, port=5555)
