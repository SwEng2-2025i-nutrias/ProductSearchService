from flask import request, current_app
import logging

# Configurar un logger básico si no existe
# Esto asegura que los logs se muestren en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def register_logging_middleware(app):
    @app.before_request
    def log_request_info():
        """Registra información de cada petición entrante."""
        current_app.logger.info('--- Petición Entrante ---')
        # current_app.logger.info(f'Path: {request.path}')
        # current_app.logger.info(f'Método: {request.method}')
        # current_app.logger.info(f'Headers: \n{request.headers}')
        # # Cuidado al loguear el body, puede ser grande. Lo limitamos.
        # body = request.get_data(as_text=True)
        # current_app.logger.info(f'Body: {body[:500] if body else "No Body"}')
        # current_app.logger.info('-------------------------')

    @app.after_request
    def log_response_info(response):
        # """Registra información de cada respuesta saliente."""
        # current_app.logger.info(f'--- Respuesta Saliente para {request.path} ---')
        # current_app.logger.info(f'Status: {response.status_code}')
        # current_app.logger.info('----------------------------------')
        return response

    @app.teardown_appcontext
    def log_exception(exception=None):
        """Registra cualquier excepción no controlada que ocurra."""
        if exception:
            current_app.logger.error('!!! Error No Controlado !!!', exc_info=True)
