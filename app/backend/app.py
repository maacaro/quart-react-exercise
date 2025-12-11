"""
Main Quart application factory for the practice exercise.
"""

# --- Compatibilidad con Flask 3.x (parche para PROVIDE_AUTOMATIC_OPTIONS) ---
try:
    # Quart utiliza internamente la clase Config de Flask.
    # En Flask 2.x existía PROVIDE_AUTOMATIC_OPTIONS; en 3.x ya no.
    from flask import Config  # type: ignore

    if "PROVIDE_AUTOMATIC_OPTIONS" not in Config.default_config:
        # Restauramos la clave antigua para que add_url_rule no reviente.
        Config.default_config["PROVIDE_AUTOMATIC_OPTIONS"] = True
except Exception:
    # Si algo falla (o estamos en una versión que no lo necesita), lo ignoramos.
    pass
# ---------------------------------------------------------------------------

from quart import Quart, jsonify


def create_app() -> Quart:
    """Create and configure the Quart application."""
    app = Quart(__name__)

    # Registrar blueprint de tasks
    from .tasks.routes import tasks_bp

    # Todas las rutas del blueprint irán bajo /api
    app.register_blueprint(tasks_bp, url_prefix="/api")

    # Healthcheck simple para Playwright / pruebas
    @app.route("/api/health")
    async def health():
        return jsonify({"status": "ok"}), 200

    return app


# Instancia global para poder hacer `python app.py`
app = create_app()

if __name__ == "__main__":
    # Servidor de desarrollo en http://localhost:5000
    app.run(port=5000)
