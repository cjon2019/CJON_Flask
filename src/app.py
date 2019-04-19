from flask import Flask
from flask_cors import CORS
from .config import app_config
from .models import bcrypt, db
from .models import user
from .views.user_view import user_api
from .views.job_view import jobs_api
import os
def create_app(env_name):
    '''
    Create Application
    '''
    app = Flask(__name__)
    CORS(app)
    config_name = os.getenv('FLASK_ENV')
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'application/json'
    app.register_blueprint(user_api, url_prefix='/api/v1/users')
    app.register_blueprint(jobs_api, url_prefix='/api/v1/jobs')
    bcrypt.init_app(app)
    db.init_app(app)
    @app.route('/')
    def index():
        return 'This is the index route'

    return app