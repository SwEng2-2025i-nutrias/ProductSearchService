import os
from dotenv import load_dotenv

from API.app.factory import create_app

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    # Crear la aplicación (ya incluye prometheus-flask-exporter)
    app = create_app()

    print("=== Endpoints registrados ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:30s} {rule.methods} {rule.rule}")

    # Configurar modo debug
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Ejecutar el servidor
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5002)),
        debug=False  # Prometheus metrics need debug=False
    )
