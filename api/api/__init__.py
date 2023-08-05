from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) 

    from .routes import tickers_bp
    app.register_blueprint(tickers_bp)

    return app

app = create_app()
