from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db=SQLAlchemy()
jwt=JWTManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)#initialising my db
    jwt.init_app(app)#initialising my jwt

    from .auth_routes import auth_bp#imprting route
    app.register_blueprint(auth_bp)#registering route

    from .reminder_routes import reminder_bp
    app.register_blueprint(reminder_bp)

    from .scheduler import init_scheduler
    init_scheduler(app)

    with app.app_context():
        db.create_all()

    return app

