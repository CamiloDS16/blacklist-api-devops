from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import DATABASE_URL
import logging

db = SQLAlchemy()
logger = logging.getLogger(__name__)

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if not DATABASE_URL.startswith('sqlite'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'connect_timeout': 5
            }
        }
    else:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Could not create database tables: {e}")
            logger.warning("Application will start but database operations may fail")