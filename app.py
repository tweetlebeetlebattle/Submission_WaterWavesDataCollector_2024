from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from repository.Models.Models import db, initialize_database
from controller.home_controller import home_controller
import os

# def schedule_fetch_save_data():
#     from service.service_shared import SharedService
#     service = SharedService()
#     service.fetch_save_all_data()
    
def create_app():
    app = Flask(__name__)
    app.config.from_object('repository.dbConfig.DevelopmentConfig')
    
    db.init_app(app)
    
    with app.app_context():
        initialize_database(app)  
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=schedule_fetch_save_data, trigger='cron', hour=18, minute=30)
    # scheduler.start()

    app.register_blueprint(home_controller)
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
