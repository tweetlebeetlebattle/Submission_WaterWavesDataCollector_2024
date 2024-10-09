from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class HTMLData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class GifData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class GlassStormIoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class DailyGifReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class DailyGlassStormReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...

class DailyHTMLReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define other columns here...


def initialize_database(app):
    with app.app_context():  # Ensures app context is active
        db.create_all()  # This will create the tables based on your models

