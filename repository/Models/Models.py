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
    global Locations, Units, HTMLData, GifData, GlassStormIoData, DailyGifReading, DailyGlassStormReading, DailyHTMLReading
    Locations = getattr(Base.classes, 'Locations', None)  # Note: case-sensitive
    Units = getattr(Base.classes, 'Units', None)  # Note: case-sensitive
    HTMLData = getattr(Base.classes, 'HTMLData', None)  # Correctly mapped to HTMLData
    GifData = getattr(Base.classes, 'GifData', None)
    GlassStormIoData = getattr(Base.classes, 'GlassStormIoData', None)
    DailyGifReading = getattr(Base.classes, 'DailyGifReading', None)
    DailyGlassStormReading = getattr(Base.classes, 'DailyGlassStormReading', None)
    DailyHTMLReading = getattr(Base.classes, 'DailyHTMLReading', None)

    # Log if the model mapping was successful
    if HTMLData is None:
        print("HTMLData model mapping failed. Please check the table name in the database.")
    else:
        print("HTMLData model successfully mapped.")

    print("Database initialized and tables reflected.")


# Utility function to convert query results to dictionary format
def to_dict(model_instance):
    """Convert SQLAlchemy model instance to dictionary."""
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}
