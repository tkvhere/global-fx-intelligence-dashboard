from flask import Flask, jsonify
from flask_cors import CORS

from database.db import init_db
from routes.currency_routes import currency_bp
from routes.forecast_routes import forecast_bp
from routes.health_routes import health_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    app.config['JSON_SORT_KEYS'] = False

    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(currency_bp)
    app.register_blueprint(forecast_bp)

    @app.route('/')
    def index():
        return jsonify({
            'name': 'Global FX Intelligence API',
            'status': 'running',
            'documentation': '/api/health',
        })

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
