from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from server import create_app, db
from server.forms import RegistrationForm
from server.models import User
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            name=form.name.data,
            username=form.username.data,
            phone=form.phone.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/post")
def post():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
