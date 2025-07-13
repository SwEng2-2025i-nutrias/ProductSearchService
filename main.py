import os
from dotenv import load_dotenv
from API.app.factory import create_app

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    # Crear la aplicación
    app = create_app()
    
    # Configurar modo debug
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Ejecutar el servidor
    app.run(
        host='0.0.0.0', 
        port=int(os.getenv("PORT", 5002)), 
        debug=debug_mode
    )