from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

db = SQLAlchemy()
Base = automap_base()

def initialize_database(app):
    DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(DATABASE_URL)
    
    # Reflect the database schema
    Base.prepare(engine, reflect=True)

    # Print out reflected table names for confirmation
    reflected_tables = Base.classes.keys()
    print("Reflected tables:", reflected_tables)

    # Map the tables to your global variables
    global Locations, Units, HTMLData, GifData, GlassStormIoData, DailyGifReading, DailyGlassStormReading, DailyHTMLReading, DataFetchingLogs
    Locations = getattr(Base.classes, 'Locations', None) 
    Units = getattr(Base.classes, 'Units', None) 
    HTMLData = getattr(Base.classes, 'HTMLData', None)  
    GifData = getattr(Base.classes, 'GifData', None)
    GlassStormIoData = getattr(Base.classes, 'GlassStormIoData', None)
    DailyGifReading = getattr(Base.classes, 'DailyGifReading', None)
    DailyGlassStormReading = getattr(Base.classes, 'DailyGlassStormReading', None)
    DailyHTMLReading = getattr(Base.classes, 'DailyHTMLReading', None)
    DataFetchingLogs = getattr(Base.classes, 'DataFetchingLogs', None)

    print("Database initialized and tables reflected.")


# Utility function to convert query results to dictionary format
def to_dict(model_instance):
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}
