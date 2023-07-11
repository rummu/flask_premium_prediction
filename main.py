from flask import Flask ,render_template , request, Blueprint
from flask_cors import CORS
from premium import app
from recommendations import recApp

mainApp = Flask(__name__)
mainApp.register_blueprint(app)
mainApp.register_blueprint(recApp)
CORS(mainApp)

#To run: flask --app main.py --debug run 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)