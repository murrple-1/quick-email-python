import unittest
import os
import time

from quick_email import builder, sender

from tests.postshift import PostShift

SMTP_HOST = os.environ[u'SMTP_HOST']
SMTP_PORT = int(os.environ[u'SMTP_PORT'])
SMTP_USER = os.environ[u'SMTP_USER']
SMTP_PASSWORD = os.environ[u'SMTP_PASSWORD']
SMTP_IS_TLS = os.environ.get(u'SMTP_IS_TLS') == u'true'
SMTP_SENDER = os.environ[u'SMTP_SENDER']


class TestSender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.postshift = PostShift()

        for i in range(6):
            cls.postshift.create()

    def test_send_msg(self):
        test_email_json = TestSender.postshift.email_jsons[0]

        msg = builder.build_msg(SMTP_SENDER, test_email_json[u'email'], None, None, u'The Subject', u'Some Text', u'<b>Some Bold Text</b>', attachment_list=None, inline_attachment_dict=None)
        sender.send_msg(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_IS_TLS, SMTP_SENDER, msg)

        # wait for email to arrive
        time.sleep(30.0)

        _json = TestSender.postshift.get_list(test_email_json[u'key'])

        self.assertIsInstance(_json, list)
        self.assertEqual(len(_json), 1)


if __name__ == u'__main__':
    unittest.main()
