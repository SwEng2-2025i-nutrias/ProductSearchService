from flask import Flask
from flasgger import Swagger
from API.adapters.routes.product_search_api import product_search_bp

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Product Search Service API',
        'uiversion': 3,
        'specs_route': '/swagger/'
    }
    Swagger(app)
    app.register_blueprint(product_search_bp)
    return app