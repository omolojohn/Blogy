from flask import Flask, render_template, request, url_for
from server import create_app, db
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register")
def register():
    return render_template('register.html')

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
