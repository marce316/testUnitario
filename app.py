from flask import Flask
from config import Config
from models import db
from routes.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar base de datos
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(main)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)