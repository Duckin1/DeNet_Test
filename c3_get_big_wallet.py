from flask import Flask, jsonify, request
import requests
from web3 import Web3

app = Flask(__name__)

# Ваш API ключ с Polygonscan
api_key = 'Нужно ввести свой API'
token_address = '0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0'

# Подключение к RPC-серверу сети Polygon
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))


@app.route('/get_top_holders/<int:top_n>', methods=['GET'])
def get_top_holders(top_n):
    if top_n <= 0:
        return jsonify({'error': 'top_n must be a positive integer'}), 400

    # URL для вызова API Polygonscan
    url = f'https://api.polygonscan.com/api'
    params = {
        'module': 'token',
        'action': 'tokenholderlist',
        'contractaddress': token_address,
        'apikey': api_key
    }

    try:
        # Отправка запроса к Polygonscan API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверьте наличие ошибок HTTP
        data = response.json()

        if data['status'] == '1':
            holders = data['result']
            sorted_holders = sorted(holders, key=lambda x: int(x['TokenHolderQuantity']), reverse=True)
            top_holders = [(holder['TokenHolderAddress'], int(holder['TokenHolderQuantity'])) for holder in
                           sorted_holders[:top_n]]

            # Преобразование балансов в эфир
            top_holders_eth = [(address, w3.from_wei(balance, 'ether')) for address, balance in top_holders]

            return jsonify(top_holders_eth)
        else:
            return jsonify({'error': 'Ошибка при получении данных с Polygonscan', 'message': data['result']}), 500

    except requests.RequestException as e:
        # Обработка ошибок HTTP
        return jsonify({'error': 'Ошибка при запросе к Polygonscan API', 'message': str(e)}), 500
    except Exception as e:
        # Обработка любых других ошибок
        return jsonify({'error': 'Неизвестная ошибка', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# Отправьте GET запрос к вашему серверу, например, http://localhost:8080/get_top_holders/5