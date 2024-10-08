from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .repository.dbConfig import DevelopmentConfig
from .controller.home_controller import home_controller  

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Closes the database session at the end of each request."""
    db.session.remove()

app.register_blueprint(home_controller)

if __name__ == '__main__':
    app.run(debug=True)
