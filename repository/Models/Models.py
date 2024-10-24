from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Locations(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    def to_dict(self):
        return {
            'id': self.Id,
            'name': self.Name, 
        }

class Units(db.Model):
    UnitId = db.Column(db.Integer, primary_key=True)
    UnitName = db.Column(db.String, nullable=False)
    def to_dict(self):
        return {
            'id': self.UnitId,
            'name': self.UnitName,  
        }
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

