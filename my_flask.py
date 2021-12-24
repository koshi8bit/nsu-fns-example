from flask import Flask, jsonify, abort, request
import logging
from datetime import datetime
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from nalog_python import NalogRuPython


app = Flask(__name__)

@app.route('/HMC/qr', methods=['POST'])
def get_task():
    if not request or not request.json or not 'qr' in request.json or not 'id' in request.json:
        logging.error(f'400')
        return jsonify({'status': 'Not Acceptable'}), 400
    if not some_fun.qr_true(request.json['qr']):
        logging.error(f'422')
        return jsonify({'status': 'Unprocessable Entity'}), 422
    logging.info(f'incoming.. id={request.json["id"]}; qr={request.json["qr"]}')
    # work.add_data(request.json['id'], request.json['qr'])
    logging.info(f'work.add_data ok.. id={request.json["id"]}; qr={request.json["qr"]}')
    return jsonify({'status': 'Ok'}), 200


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')
    logging.info('starting v2..')
    app.run(host='0.0.0.0', port=8190)
