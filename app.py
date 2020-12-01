from flask import Flask, g
from flask_cors import CORS

import models
from blueprints.jobs import job

DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(job, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(job, url_prefix='/trackr/jobs')


@app.before_request
def before_request():
    """ Connect to db before each request """
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """ Close the db after each request """
    g.db.close()
    return response


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
