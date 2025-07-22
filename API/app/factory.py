from flask import Flask, redirect, url_for
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from API.adapters.routes.product_search_api import product_search_bp

def create_app():
    app = Flask(__name__)
    
    # Configuración completa de Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Product Search Service API",
            "description": "API para buscar y filtrar productos con múltiples criterios",
            "version": "1.0.0",
            "termsOfService": "",
            "contact": {
                "name": "SwEng2-2025i-nutrias",
                "url": "https://github.com/SwEng2-2025i-nutrias"
            }
        },
        "host": "localhost:5002",
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Product Search",
                "description": "Endpoints para búsqueda y filtrado de productos"
            },
            {
                "name": "Monitoring", 
                "description": "Endpoints de métricas y monitoreo"
            }
        ]
    }
    
    app.config['SWAGGER'] = swagger_config
    
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)
    
    # Initialize Swagger with template
    Swagger(app, template=swagger_template)
    
    # Ruta raíz que redirije al Swagger UI
    @app.route('/')
    def index():
        """
        Página de inicio - Redirije a la documentación Swagger
        """
        return redirect('/swagger/')
    
    # Ruta de salud del servicio
    @app.route('/health')
    def health():
        """
        Endpoint de verificación de salud del servicio
        ---
        tags:
          - Monitoring
        summary: Verificar estado del servicio
        description: Retorna el estado de salud del servicio
        responses:
          200:
            description: Servicio funcionando correctamente
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "healthy"
                    service:
                      type: string
                      example: "Product Search Service"
                    version:
                      type: string
                      example: "1.0.0"
        """
        return {
            "status": "healthy",
            "service": "Product Search Service", 
            "version": "1.0.0"
        }
    
    app.register_blueprint(product_search_bp)
    return app