from flask import Blueprint, jsonify, request

from config import SUPPORTED_CURRENCIES, DEFAULT_BASE
from services.alert_service import create_alert, delete_alert, get_alert_history, list_alerts, toggle_alert
from services.converter_service import convert_amount
from services.exchange_rate_service import get_historical_rates, get_latest_rates, get_snapshot_for_pair
from services.historical_service import build_pair_summary, get_daily_percentage_change
from services.volatility_service import compute_volatility

currency_bp = Blueprint('currency_bp', __name__)


@currency_bp.route('/api/currencies', methods=['GET'])
def currencies():
    return jsonify({
        'base': DEFAULT_BASE,
        'source': 'Frankfurter API',
        'currencies': [
            {'code': code, 'name': name} for code, name in SUPPORTED_CURRENCIES.items()
        ],
    })


@currency_bp.route('/api/rates', methods=['GET'])
def rates():
    base = (request.args.get('base') or DEFAULT_BASE).upper()
    try:
        payload = get_latest_rates(base)
        return jsonify(payload)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Failed to fetch rates: {exc}'}), 502


@currency_bp.route('/api/rates/history', methods=['GET'])
def history_rates():
    base = (request.args.get('base') or DEFAULT_BASE).upper()
    symbols = request.args.get('symbols', '')
    days = request.args.get('days', '90')
    try:
        days_value = int(days)
        payload = get_historical_rates(base_currency=base, symbols=symbols, days=days_value)
        return jsonify(payload)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Failed to fetch historical rates: {exc}'}), 502


@currency_bp.route('/api/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from', '').upper()
    to_currency = request.args.get('to', '').upper()
    amount = request.args.get('amount', '0')

    try:
        result = convert_amount(amount, from_currency, to_currency)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Conversion failed: {exc}'}), 502


@currency_bp.route('/api/analytics', methods=['GET'])
def analytics():
    base = (request.args.get('base') or DEFAULT_BASE).upper()
    target = (request.args.get('target') or 'INR').upper()
    days = int(request.args.get('days', '90'))
    try:
        summary = build_pair_summary(base, target, days)
        daily_change = get_daily_percentage_change(base, target, days)
        return jsonify({
            'pair': summary['pair'],
            'summary': summary,
            'daily_changes': daily_change['changes'],
            'source': summary['source'],
        })
    except Exception as exc:
        return jsonify({'error': f'Analytics failed: {exc}'}), 502


@currency_bp.route('/api/volatility', methods=['GET'])
def volatility():
    base = (request.args.get('base') or DEFAULT_BASE).upper()
    target = (request.args.get('target') or 'INR').upper()
    days = int(request.args.get('days', '90'))
    try:
        payload = get_historical_rates(base_currency=base, symbols=[target], days=days)
        values = []
        for item in payload['rates']:
            rate_value = item.get('rates', {}).get(target)
            if rate_value is not None:
                values.append(float(rate_value))
        result = compute_volatility(values)
        return jsonify({
            'pair': f'{base}/{target}',
            'days': days,
            'source': payload['source'],
            'volatility': result,
        })
    except Exception as exc:
        return jsonify({'error': f'Volatility calculation failed: {exc}'}), 502


@currency_bp.route('/api/alerts', methods=['GET'])
def alerts():
    return jsonify({'alerts': list_alerts(), 'history': get_alert_history()})


@currency_bp.route('/api/alerts', methods=['POST'])
def create_alert_route():
    payload = request.get_json(silent=True) or {}
    try:
        result = create_alert(payload.get('currency_pair'), payload.get('threshold'), payload.get('direction'), payload.get('enabled', True))
        return jsonify({'success': True, 'alert': result}), 201
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Alert creation failed: {exc}'}), 502


@currency_bp.route('/api/alerts/<int:alert_id>', methods=['PATCH'])
def toggle_alert_route(alert_id):
    payload = request.get_json(silent=True) or {}
    try:
        result = toggle_alert(alert_id, payload.get('enabled', True))
        return jsonify({'success': True, 'alert': result})
    except Exception as exc:
        return jsonify({'error': f'Alert update failed: {exc}'}), 502


@currency_bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert_route(alert_id):
    try:
        result = delete_alert(alert_id)
        return jsonify({'success': True, 'result': result})
    except Exception as exc:
        return jsonify({'error': f'Alert deletion failed: {exc}'}), 502


@currency_bp.route('/api/rate-details', methods=['GET'])
def rate_details():
    base = (request.args.get('base') or DEFAULT_BASE).upper()
    target = (request.args.get('target') or 'INR').upper()
    try:
        snapshot = get_snapshot_for_pair(base, target)
        return jsonify(snapshot)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': f'Failed to fetch rate details: {exc}'}), 502
