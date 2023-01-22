import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask

from server import api, config, logs, views
from server.models import db

CONFIG = config.Config()

def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIG)

    file_handler = RotatingFileHandler(
            filename=CONFIG.LOG_PATH,
            maxBytes=1000000,
            backupCount=5,
            encoding='utf-8'
        )
    file_handler.setFormatter(
        Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    )
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.register_blueprint(views.routes, url_prefix='/')
    app.register_blueprint(api.routes_v1, url_prefix='/api/v1')
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.logger.info('APP started')
    
    return app