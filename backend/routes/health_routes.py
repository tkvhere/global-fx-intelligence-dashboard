from flask import Blueprint, jsonify

health_bp = Blueprint('health_bp', __name__)


@health_bp.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'Global FX Intelligence API',
        'version': '1.0.0',
    })
