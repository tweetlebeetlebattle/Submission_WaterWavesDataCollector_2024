from flask import Flask
from repository.Models.Models import db, initialize_database  # Import db and initialize function
from controller.home_controller import home_controller

def create_app():
    app = Flask(__name__)
    app.config.from_object('repository.dbConfig.DevelopmentConfig')
    
    db.init_app(app)
    
    with app.app_context():
        initialize_database(app)  # Reflect existing tables
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    app.register_blueprint(home_controller)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
