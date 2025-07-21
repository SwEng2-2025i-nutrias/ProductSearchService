import os
import sys
from dotenv import load_dotenv
from flask import jsonify
from waitress import serve

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

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200

    port = int(os.getenv("PORT", 5002))
    serve(app, host='0.0.0.0', port=port)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)