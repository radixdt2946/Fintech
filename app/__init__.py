# from flask import Flask
# from app.routes import route_handler
# app = Flask(__name__)
# app.register_blueprint(route_handler)

# app.run(debug=True)

from flask import Flask
from app.routes import main

def create_app():
    app = Flask(__name__)    
    app.config.from_object('config.Config')
    app.register_blueprint(main)
    return app