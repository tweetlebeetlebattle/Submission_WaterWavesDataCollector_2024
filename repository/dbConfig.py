import os
from dotenv import load_dotenv
load_dotenv()
connectionString = os.getenv("databaseConnectionString")
class Config:
    # Common configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = connectionString