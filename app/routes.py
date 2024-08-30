from flask import jsonify, request, send_from_directory
from flask.blueprints import Blueprint
from pathlib import Path
import os
# from app.services import fetch_stock_data

from flask import Blueprint, jsonify, request, Response
from .services.finance_data import get_financial_data
from .services.pattern_detection import detect_patterns
from .services.backtesting import perform_backtest

main = Blueprint('main', __name__)
DIR_PATH: Path = Path(__file__).parent.parent


@main.route('/')
def index():
    return '<p>Hello</p>'

@main.route('/quote', methods=['GET'])
def quote():
    '''
    Fetch the financial data for a given stock symbol.
    '''

    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400
    try:
        data = get_financial_data(symbol)
        if 'error' in data:
            return jsonify(data), 400
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/patterns', methods=['POST'])
def patterns():
    
    '''
        Detect stock price patterns for a given stock symbol and pattern type.
    '''
    try:
        data = request.json
        pattern_type = data.get('pattern_type')
        symbol = data.get('symbol')
        if not pattern_type or not symbol:
            return jsonify({'error': 'Pattern type and symbol are required'}), 400    
        result = detect_patterns(data) 
        if 'error' in result:
                return jsonify(result), 400
        return jsonify(result),200   
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/backtest', methods=['POST'])
def backtest():
    '''
        Perform a backtest for a given trading strategy.
    '''
    try:
        data = request.json    
        result = perform_backtest(data)
        
        if 'Error' in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/assets/<filename>')
def my_files(filename):
    print(DIR_PATH)
    response = send_from_directory(f"{DIR_PATH}/assets", filename)
    print(response)
    return response