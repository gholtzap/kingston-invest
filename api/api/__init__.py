from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) 

    # Register tickers_bp
    from .routes import tickers_bp
    app.register_blueprint(tickers_bp)

    # Register auth_bp
    from .routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

app = create_app()
