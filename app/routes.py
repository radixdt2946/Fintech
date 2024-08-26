from flask import jsonify, request
from flask.blueprints import Blueprint
# from app.services import fetch_stock_data

from flask import Blueprint, jsonify, request
from .services.finance_data import get_financial_data
from .services.pattern_detection import detect_patterns
from .services.backtesting import perform_backtest

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return '<p>Hello</p>'

@main.route('/quote', methods=['GET'])
def quote():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400
    data = get_financial_data(symbol)
    return jsonify(data)



@main.route('/patterns', methods=['GET'])
def patterns():
    pattern_type = request.args.get('pattern_type')
    symbol = request.args.get('symbol')
    if not pattern_type or not symbol:
        return jsonify({'error': 'Pattern type and symbol are required'}), 400    
    result = detect_patterns(symbol, pattern_type)    
    if not result:
        return jsonify({'message': f'No {pattern_type} pattern found for {symbol}'}), 200
    return jsonify({'message': f'{pattern_type} pattern detected', 'file': result}), 200


@main.route('/backtest', methods=['POST'])
def backtest():
    data = request.json    
    result = perform_backtest(data)
    return jsonify(result)

# route_handler = Blueprint(name='api', import_name=__name__, url_prefix='/api')


# @route_handler.route('/')
# def index():
#     return '<p>Hello</p>'


# @route_handler.route('/stock_data', methods=['GET'])
# def get_stock_data():
#     symbol = request.args.get('symbol')
#     period = request.args.get('period', '1d')
#     interval = request.args.get('interval', '1m')
#     data = fetch_stock_data(symbol, period, interval)
#     return jsonify(data)



