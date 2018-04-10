import unittest
import os

import requests

from quick_email import builder, sender

SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = int(os.environ['SMTP_PORT'])
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
SMTP_IS_TLS = os.environ.get('SMTP_IS_TLS') == 'true'
SMTP_SENDER = os.environ['SMTP_SENDER']

MASHAPE_KEY = os.environ['MASHAPE_KEY']

class PostShift:
    ENDPOINT_URL = 'https://reuleaux-post-shift-v1.p.mashape.com/api.php'
    @staticmethod
    def create():
        r = requests.get(PostShift.ENDPOINT_URL, params={
                'action': 'new',
                'type': 'json',
            }, headers={
                'X=Mashape-Key': MASHAPE_KEY,
                'Accept': 'application/json',
            })

        _json = r.json()

        return _json

    @staticmethod
    def get_list(email_key):
        r = requests.get(PostShift.ENDPOINT_URL, params={
            'action': 'getlist',
            'key': email_key,
            'type': 'json',
        }, headers={
            'X=Mashape-Key': MASHAPE_KEY,
            'Accept': 'application/json',
        })

        _json = r.json()

        return _json

    @staticmethod
    def clear(email_key):
        requests.get(PostShift.ENDPOINT_URL, params={
            'action': 'clear',
            'key': email_key,
            'type': 'json',
        }, headers={
            'X=Mashape-Key': MASHAPE_KEY,
            'Accept': 'application/json',
        })

class TestSender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _json = PostShift.create()

        cls.test_email = _json['email']
        cls.postshift_key = _json['key']

    def tearDown(self):
        PostShift.clear(TestSender.postshift_key)

    # TODO write test suite
    def test_send_msg(self):
        msg = builder.build_msg(SMTP_SENDER, TestSender.test_email, None, None, 'The Subject', 'Some Text', '<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        sender.send_msg(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_IS_TLS, SMTP_SENDER, msg)

        _json = PostShift.get_list(TestSender.postshift_key)

        self.assertEquals(len(_json), 1)


if __name__ == '__main__':
    unittest.main()
