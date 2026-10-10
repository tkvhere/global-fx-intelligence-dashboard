from flask import Blueprint, jsonify, request

from services.forecast_service import generate_forecast, get_forecast_evaluation

forecast_bp = Blueprint('forecast_bp', __name__)


@forecast_bp.route('/api/forecast', methods=['GET'])
def forecast():
    base = (request.args.get('base') or 'USD').upper()
    target = (request.args.get('target') or 'INR').upper()
    horizon = int(request.args.get('horizon', '7'))
    try:
        result = generate_forecast(base, target, horizon=horizon)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Forecast generation failed: {exc}'}), 502


@forecast_bp.route('/api/forecast/evaluation', methods=['GET'])
def forecast_evaluation():
    base = (request.args.get('base') or 'USD').upper()
    target = (request.args.get('target') or 'INR').upper()
    try:
        result = get_forecast_evaluation(base, target)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Forecast evaluation failed: {exc}'}), 502
