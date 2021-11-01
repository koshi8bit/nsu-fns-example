import os
import json

import requests

from j_work import Jwork
from my_error import My_error


class NalogRuPython:
    HOST = 'irkkt-mobile.nalog.ru:8888'
    DEVICE_OS = 'iOS'
    CLIENT_VERSION = '2.9.0'
    DEVICE_ID = '7C82010F-16CC-446B-8F66-FC4080C66521'
    ACCEPT = '*/*'
    USER_AGENT = 'billchecker/2.9.0 (iPhone; iOS 13.6; Scale/2.00)'
    ACCEPT_LANGUAGE = 'ru-RU;q=1, en-US;q=0.9'

    def __init__(self):
        self.__session_id = None
        self.inform = Jwork()
        self.set_session_id()

    def set_session_id(self) -> None:
        """
        Authorization using INN and password of user lk nalog.ru
        """
        data = self.inform.get_inf()

        if data is not None:
            url = f'https://{self.HOST}/v2/mobile/users/lkfl/auth'
            payload = {
                'inn': str(data.get_inn()),
                'client_secret': data.get_sec(),
                'password': data.get_pass()
            }
            headers = {
                'Host': self.HOST,
                'Accept': self.ACCEPT,
                'Device-OS': self.DEVICE_OS,
                'Device-Id': self.DEVICE_ID,
                'clientVersion': self.CLIENT_VERSION,
                'Accept-Language': self.ACCEPT_LANGUAGE,
                'User-Agent': self.USER_AGENT,
            }

            resp = requests.post(url, json=payload, headers=headers)
            try:
                self.__session_id = resp.json()['sessionId']
            except Exception as e:
                raise My_error(1)
            return

        # print(data.GetINN())
        # print(data.GetPASS())
        # print(data.GetSEC())
        raise My_error(2)

    def _get_ticket_id(self, qr: str) -> str:
        """
        Get ticker id by info from qr code

        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
        """
        url = f'https://{self.HOST}/v2/ticket'
        data = self.inform.get_inf()
        if data is None:
            self.set_session_id()
            return self._get_ticket_id(qr)
        else:
            payload = {'qr': qr}
            headers = {
                'Host': self.HOST,
                'Accept': self.ACCEPT,
                'Device-OS': self.DEVICE_OS,
                'Device-Id': self.DEVICE_ID,
                'clientVersion': self.CLIENT_VERSION,
                'Accept-Language': self.ACCEPT_LANGUAGE,
                'sessionId': self.__session_id,
                'User-Agent': self.USER_AGENT,
            }
            resp = requests.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                raise My_error(3)
            return resp.json()["id"]

    def get_ticket(self, qr: str) -> dict:
        """
        Get JSON ticket

        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{self.HOST}/v2/tickets/{ticket_id}'
        headers = {
            'Host': self.HOST,
            'sessionId': self.__session_id,
            'Device-OS': self.DEVICE_OS,
            'clientVersion': self.CLIENT_VERSION,
            'Device-Id': self.DEVICE_ID,
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT,
            'Accept-Language': self.ACCEPT_LANGUAGE,
        }

        resp = requests.get(url, headers=headers)

        return resp.json()
