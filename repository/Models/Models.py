from app import db

class Locations(db.Model):
    __table__ = db.Table('locations', db.metadata, autoload=True, autoload_with=db.engine)

class Units(db.Model):
    __table__ = db.Table('units', db.metadata, autoload=True, autoload_with=db.engine)

class HTMLData(db.Model):
    __table__ = db.Table('htmldata', db.metadata, autoload=True, autoload_with=db.engine)

class GifData(db.Model):
    __table__ = db.Table('gifdata', db.metadata, autoload=True, autoload_with=db.engine)

class GlassStormIoData(db.Model):
    __table__ = db.Table('GlassStormIoData', db.metadata, autoload=True, autoload_with=db.engine)    

class DailyGifReading(db.Model):
    __table__ = db.Table('DailyGifReading', db.metadata, autoload=True, autoload_with=db.engine)   

class DailyGlassStormReading(db.Model):
    __table__ = db.Table('DailyGlassStormReading', db.metadata, autoload=True, autoload_with=db.engine)   

class DailyHTMLReading(db.Model):
    __table__ = db.Table('DailyHTMLReading', db.metadata, autoload=True, autoload_with=db.engine)   