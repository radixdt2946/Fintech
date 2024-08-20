from flask import jsonify, request
from flask.blueprints import Blueprint
# from app.services import fetch_stock_data

from flask import Blueprint, jsonify, request
from .services.finance_data import get_financial_data



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



