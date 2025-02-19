from flask import Flask
import secrets

def create_app():
    app = Flask(__name__)
    
    # Generate a secure secret key
    app.secret_key = secrets.token_hex(16)
    # Alternatively, we can set a static secret key:
    # app.secret_key = 'your-secure-secret-key-here'  # We have to make sure to use a strong secret key in production
    
    from app.routes import main
    app.register_blueprint(main)

    return app
