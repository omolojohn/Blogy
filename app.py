from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from server import create_app, db
from server.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from server.models import User, Category, Comment, Post


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

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
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('post'))
        flash("Invalid username or password.", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        category_id = request.form.get("category")

        if not title or not body:
            flash("Title and content cannot be empty.", "danger")
        else:
            new_post = Post(
                title=title,
                body=body,
                category_id=category_id,
                user_id=current_user.id
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("post"))

    categories = Category.query.all()  
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("post.html", categories=categories, posts=posts)


if __name__ == "__main__":
    app.run(debug=True, port=5555)
