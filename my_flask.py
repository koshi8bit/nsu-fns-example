from flask import Flask, jsonify, abort, request
import logging
import threading
import re
from datetime import datetime
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from nalog_python import NalogRuPython
import requests
import json

app = Flask(__name__)

results = []

@app.route('/HMC/qr', methods=['POST'])
def get_task():
    if not request or not request.json or not 'qr' in request.json or not 'id' in request.json:
        logging.error(f'400')
        return jsonify({'status': 'Not Acceptable'}), 400
    if not validate_qr(request.json['qr']):
        logging.error(f'422')
        return jsonify({'status': 'Unprocessable Entity'}), 422
    logging.info(f'incoming.. id={request.json["id"]}; qr={request.json["qr"]}')


    global results
    results.append(ret)    
    logging.info(f'work.add_data ok..')
    return jsonify({'status': 'Ok'}), 200

def request_to_fns(qr_code):
    client = NalogRuPython()
    ticket = client.get_ticket(qr_code)
    answer = str(json.dumps(ticket, indent=4, ensure_ascii=False))
    return answer

def back_url():
    env_var = os.getenv("URL_TO_BACK")
    if not env_var:
        logging.error("Empty url")
        raise ValueError('Variable "URL_TO_BACK" is not set')

    res =  f'{env_var}hmc/api/v1/fns/qr-code-response'
    logging.info(f'url = {res}')
    print(f'url = {res}')
    return res


def validate_qr(qr_code):
    qr_template = r'^t=\d+T\d+&s=\d+.\d+&fn=\d+&i=\d+&fp=\d+&n=1$'
    qr_is_valid = re.match(qr_template, qr_code)
    if qr_is_valid:
        return True
    return False

def start_timer():
    threading.Timer(5, timer_callback).start()

def timer_callback():
    logging.info(f'timer_callback')
    global back_url
    global results
    for res in results:
        try:
            client = NalogRuPython()
            ticket = client.get_ticket(request.json["qr"])
            print(ticket)

            ret = dict({'id': request.json["id"], "receipt": ticket, 'status': 'OK'})
            logging.info('try ok')
        except Exception as ex:
            ret = dict({'id': request.json["id"], "receipt": '', 'status': 'ERROR'})
            logging.info('try exc')

        resp = requests.post(back_url, json=res)
        # logging.info(str(json.dumps(ticket, indent=4, ensure_ascii=False)))
        logging.info(f'--------------------------------------------')
        logging.info(str(json.dumps(res, indent=4, ensure_ascii=False)))
        logging.info(f'resp: {str(resp)}')
        logging.info(f'resp.text: {str(resp.text)}')
        logging.info(f'resp.status_code: {str(resp.status_code)}')
    #    logging.info(str(json.dumps(resp.json(), indent=4, ensure_ascii=False)))

    start_timer()

if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')
    logging.info('starting v2..')
    back_url = back_url()
    start_timer()
    logging.info('init ok!')
    app.run(host='0.0.0.0', port=8190)