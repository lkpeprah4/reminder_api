from . import db
from datetime import datetime



class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    reminders = db.relationship("Reminders", backref="user", lazy=True)
    
class Reminders(db.Model):
    __tablename__= "reminders"
    id= db.Column(db.Integer, primary_key=True)
    message=db.Column(db.String(100),nullable=False)
    schedule_time=db.Column(db.DateTime, nullable=False)
    repeat_frequency=db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))

