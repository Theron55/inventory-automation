from flask import Flask
from routes.products import products_bp


from db import Base, engine
import models.product

def create_app():
    app = Flask(__name__)

    # Create database tables (runs at startup)
    Base.metadata.create_all(bind=engine)

    # Register blueprints (routes)
    app.register_blueprint(products_bp)
    
    @app.get("/")
    def home():
        return {"message": "Inventory API is running!"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
