from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from models import setup_db, Question,Category, db, paginate_questions
from flask_cors import CORS

app = Flask(__name__)
Migrate(app, db)
setup_db(app)
CORS(app)

# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow_Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Controll-Allow-Methods',
                         'POST,PATCH,DELETE,GET,OPTIONS')
    return response

# GET


@app.route('/', methods=['GET'])
def get_all_plants():
    return "Hiiii"


if __name__ == "__main__":
    app.run()
