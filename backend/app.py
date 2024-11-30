from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS
from utils import manifest_handler
from models import user

app = Flask(__name__)
CORS(app)

@app.route("/home", methods=["POST"])
def home():
    return render_template('../frontend/src/LandingPage.jsx')

@app.route("/fileUpload", methods=["POST"])
def fileUpload():
    if 'file' not in request.files:
        return "File not found!", 400
    file = request.files['file']
    manifest_handler.retrieval(file)
    return redirect('/home')

@app.route("/login", methods=["POST"])
def login():
    if (request.method == 'POST'):
        first_name = request.get_json()
        if not first_name:
            return (jsonify({"Message": "You must include a first name."}), 400)
        user.set_user(first_name)
    return {'first_name': user.get_user()}
    
if __name__ == '__main__':
    app.run(debug=True)