from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

class HTMLData(db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    WaveRead = db.Column(db.Float, nullable=True)  # Wave reading
    WaveUnitId = db.Column(db.Integer, db.ForeignKey('units.UnitId'), nullable=True)  # Foreign key to Units
    WaveUnit = db.relationship("Units", foreign_keys=[WaveUnitId])  # Relationship to Units

    TempRead = db.Column(db.Float, nullable=True)  # Temperature reading
    TempUnitId = db.Column(db.Integer, db.ForeignKey('units.UnitId'), nullable=True)  # Foreign key to Units
    TempUnit = db.relationship("Units", foreign_keys=[TempUnitId])  # Relationship to Units

    Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Reading date

    LocationId = db.Column(db.Integer, db.ForeignKey('locations.Id'), nullable=False)  # Foreign key to Locations
    Location = db.relationship("Locations", foreign_keys=[LocationId])  # Relationship to Locations

    def to_dict(self):
        return {
            'id': self.Id,
            'wave_read': self.WaveRead,
            'wave_unit_id': self.WaveUnitId,
            'temp_read': self.TempRead,
            'temp_unit_id': self.TempUnitId,
            'date': self.Date.isoformat(),  # Return ISO formatted date for consistency
            'location_id': self.LocationId,
        }

# Other Models with correct naming conventions
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
