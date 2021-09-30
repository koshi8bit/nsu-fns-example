import json
from dotenv import load_dotenv
from nalog_python import NalogRuPython


def request_to_fns(qr_code):
    client = NalogRuPython()
    ticket = client.get_ticket(qr_code)
    answer = str(json.dumps(ticket, indent=4, ensure_ascii=False))
    return answer


if __name__ == '__main__':
    qr_code = 't=20210918T1904&s=110993.00&fn=9280440301369575&i=3273&fp=1326101455&n=1'
    res = request_to_fns(qr_code)
    print(res)


