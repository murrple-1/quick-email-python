import os
import pprint
import time
import six

import requests

from tests.logger import logger

MASHAPE_KEY = os.environ[u'MASHAPE_KEY']

class PostShift:
    ENDPOINT_URL = u'https://reuleaux-post-shift-v1.p.mashape.com/api.php'
    REQUEST_INTERVAL = 15.0
    LAST_REQUEST_TIME = None

    @staticmethod
    def _headers():
        return {
            u'X-Mashape-Key': MASHAPE_KEY,
            u'Accept': u'application/json',
        }

    def __init__(self):
        self.email_jsons = []

    @classmethod
    def sleep_if_needed(cls):
        if cls.LAST_REQUEST_TIME is not None:
            diff = (time.time() - cls.LAST_REQUEST_TIME)

            logger().debug(u'%s seconds since last request', diff)

            if diff < PostShift.REQUEST_INTERVAL:
                wait = (PostShift.REQUEST_INTERVAL - diff)
                logger().debug(u'sleeping for %s seconds...', wait)
                time.sleep(wait)

    def create(self):
        PostShift.sleep_if_needed()

        r = requests.get(PostShift.ENDPOINT_URL, params={
                u'action': u'new',
                u'type': u'json',
            }, headers=PostShift._headers())

        PostShift.LAST_REQUEST_TIME = time.time()

        _json = r.json()

        logger().debug(u'`create`: %s', pprint.pformat(_json))

        if not isinstance(_json, dict):
            raise RuntimeError(u'bad response')

        if u'email' not in _json or u'key' not in _json:
            raise RuntimeError(u'bad response')

        if not isinstance(_json[u'email'], six.string_types):
            raise RuntimeError(u'bad response')

        if not isinstance(_json[u'key'], six.string_types):
            raise RuntimeError(u'bad response')

        return _json

    def get_list(self, email_key):
        PostShift.sleep_if_needed()

        r = requests.get(PostShift.ENDPOINT_URL, params={
            u'action': u'getlist',
            u'key': email_key,
            u'type': u'json',
        }, headers=PostShift._headers())

        PostShift.LAST_REQUEST_TIME = time.time()

        _json = r.json()

        logger().debug(u'`get_list`: %s', pprint.pformat(_json))

        if not isinstance(_json, list):
            raise RuntimeError(u'bad response')

        for e_json in _json:
            if not isinstance(e_json, dict):
                raise RuntimeError(u'bad response')

            if u'id' not in e_json or u'date' not in e_json or u'subject' not in e_json or u'from' not in e_json:
                raise RuntimeError(u'bad response')

            if not isinstance(e_json[u'id'], int):
                raise RuntimeError(u'bad response')

            if not isinstance(e_json[u'date'], six.string_types):
                raise RuntimeError(u'bad response')

            if not isinstance(e_json[u'subject'], six.string_types):
                raise RuntimeError(u'bad response')

            if not isinstance(e_json[u'from'], six.string_types):
                raise RuntimeError(u'bad response')

        return _json

    def clear(self, email_key):
        PostShift.sleep_if_needed()

        r = requests.get(PostShift.ENDPOINT_URL, params={
            u'action': u'clear',
            u'key': email_key,
            u'type': u'json',
        }, headers=PostShift._headers())

        PostShift.LAST_REQUEST_TIME = time.time()

        _json = r.json()

        logger().debug(u'`clear`: %s', pprint.pformat(_json))

        if not isinstance(_json, dict):
            raise RuntimeError(u'bad response')

        if u'clear' not in _json or u'key' not in _json:
            raise RuntimeError(u'bad response')

        if not isinstance(_json[u'clear'], six.string_types):
            raise RuntimeError(u'bad response')

        if not isinstance(_json[u'key'], six.string_types):
            raise RuntimeError(u'bad response')

        if _json[u'clear'] != u'ok':
            raise RuntimeError(u'bad response')

        return _json
