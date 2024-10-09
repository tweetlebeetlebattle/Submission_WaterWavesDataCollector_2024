from flask import Flask
from repository.Models.Models import db, initialize_database  # Import your db and initialize function
from controller.home_controller import home_controller  

def create_app():
    app = Flask(__name__)
    app.config.from_object('repository.dbConfig.DevelopmentConfig')

    db.init_app(app)  # Initialize the SQLAlchemy instance with the app

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    app.register_blueprint(home_controller)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():  # Ensures the context is active when initializing the database
        initialize_database(app)
    app.run(debug=True)
