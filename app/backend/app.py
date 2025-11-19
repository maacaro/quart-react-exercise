"""
Application Factory
Creates and configures the Quart application
"""
from quart import Quart
from quart_cors import cors
import os

# TODO: Import the tasks blueprint
# from app.backend.tasks.routes import tasks_bp


def create_app():
    """
    Application factory function
    Creates and configures the Quart app instance

    Returns:
        Quart: Configured application instance
    """
    app = Quart(__name__)

    # Enable CORS for frontend communication
    app = cors(app, allow_origin=os.getenv('CORS_ORIGIN', 'http://localhost:5173'))

    # TODO: Register the tasks blueprint
    # Hint: app.register_blueprint(tasks_bp, url_prefix='/api')

    @app.route('/api/health')
    async def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'API is running'}

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('BACKEND_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
