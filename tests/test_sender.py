import unittest
import os
import sys
import logging
import pprint
import time
import random

import requests

from quick_email import builder, sender

SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = int(os.environ['SMTP_PORT'])
SMTP_USER = os.environ['SMTP_USER']
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']
SMTP_IS_TLS = os.environ.get('SMTP_IS_TLS') == 'true'
SMTP_SENDER = os.environ['SMTP_SENDER']

MASHAPE_KEY = os.environ['MASHAPE_KEY']

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

_logger = None
def logger():
    global _logger

    if _logger is None:
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.getLevelName(LOG_LEVEL))

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s (%(levelname)s): %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'))
        _logger.addHandler(stream_handler)

    return _logger


class PostShift:
    ENDPOINT_URL = 'https://reuleaux-post-shift-v1.p.mashape.com/api.php'
    MIN_SLEEP_SECONDS = 5.0
    MAX_SLEEP_SECONDS = 15.0

    @classmethod
    def sleep(cls):
        seconds = (random.random() * (cls.MAX_SLEEP_SECONDS - cls.MIN_SLEEP_SECONDS)) + cls.MIN_SLEEP_SECONDS
        time.sleep(seconds)

    @classmethod
    def create(cls):
        r = requests.get(PostShift.ENDPOINT_URL, params={
                'action': 'new',
                'type': 'json',
            }, headers={
                'X-Mashape-Key': MASHAPE_KEY,
                'Accept': 'application/json',
            })

        cls.sleep()

        _json = r.json()

        logger().debug(pprint.pformat(_json))

        return _json

    @classmethod
    def get_list(cls, email_key):
        r = requests.get(PostShift.ENDPOINT_URL, params={
            'action': 'getlist',
            'key': email_key,
            'type': 'json',
        }, headers={
            'X-Mashape-Key': MASHAPE_KEY,
            'Accept': 'application/json',
        })

        cls.sleep()

        _json = r.json()

        logger().debug(pprint.pformat(_json))

        return _json

    @classmethod
    def clear(cls, email_key):
        r = requests.get(PostShift.ENDPOINT_URL, params={
            'action': 'clear',
            'key': email_key,
            'type': 'json',
        }, headers={
            'X-Mashape-Key': MASHAPE_KEY,
            'Accept': 'application/json',
        })

        cls.sleep()

        _json = r.json()

        logger().debug(pprint.pformat(_json))

class TestSender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        PostShift.sleep()

        _json = PostShift.create()

        cls.test_email = _json['email']
        cls.postshift_key = _json['key']

    def tearDown(self):
        PostShift.clear(TestSender.postshift_key)

    # TODO write test suite
    def test_send_msg(self):
        msg = builder.build_msg(SMTP_SENDER, TestSender.test_email, None, None, 'The Subject', 'Some Text', '<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        sender.send_msg(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_IS_TLS, SMTP_SENDER, msg)

        # wait for email to arrive
        time.sleep(30.0)

        _json = PostShift.get_list(TestSender.postshift_key)

        self.assertIsInstance(_json, list)
        self.assertEqual(len(_json), 1)


if __name__ == '__main__':
    unittest.main()
