from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workout(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   muscle_group = db.Column(db.String(100), nullable=False)
   exercise = db.Column(db.String(100), nullable=False)
   sets = db.Column(db.Integer, nullable=False)
   reps = db.Column(db.Integer, nullable=False)
   date = db.Column(db.Date, nullable=False)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(100), unique=True, nullable=False)
   password = db.Column(db.String(100), nullable=False)
