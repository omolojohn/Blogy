from flask import Flask, jsonify, request
from server import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Blogy API"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5555)
