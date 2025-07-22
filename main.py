import os
import sys
from dotenv import load_dotenv
from flask import jsonify
from waitress import serve
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

try:
    from API.app.factory import create_app
    from flask_cors import CORS
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

load_dotenv()

try:
    app = create_app()  # ← CLAVE: Con paréntesis
    
    CORS(app, resources={r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    
        # Exponer endpoint /metrics en la raíz
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200

    #  # Configurar modo debug
    # debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    port = int(os.getenv("PORT", 5002))
    serve(app, host='0.0.0.0', port=port)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
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
