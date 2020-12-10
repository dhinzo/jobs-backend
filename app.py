from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import os

import models
from blueprints.jobs import job
from blueprints.users import user

DEBUG = True
PORT = 8000

app = Flask(__name__)


# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_SAMESITE='None'
# )


app.secret_key = "3058nN3433Da"
login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        # print("loading the following user: " + user_id)
        return user
    except models.DoesNotExist:
        return None


CORS(job, origins=['http://localhost:3000',
                   'https://myjobtrackr-app.herokuapp.com'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000',
                    'https://myjobtrackr-app.herokuapp.com'], supports_credentials=True)


app.register_blueprint(job, url_prefix='/trackr/jobs')
app.register_blueprint(user, url_prefix='/trackr/users')


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
    return 'hello world'


if 'ON_HEROKU' in os.environ:
    print('\non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
