import os
from dotenv import load_dotenv
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from API.app.factory import create_app

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    # Crear la aplicación
    app = create_app()

    # Exponer endpoint /metrics en la raíz
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    # Configurar modo debug
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Ejecutar el servidor
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5002)),
        debug=debug_mode
    )
