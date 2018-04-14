import unittest

from quick_email import builder
from quick_email.builder import Attachment


class TestBuilder(unittest.TestCase):
    def test_to_address_string(self):
        self.assertEqual(builder.to_address_string(
            u'Test <test@test.com>'), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string(
            (u'Test', u'test@test.com')), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string(
            u'test@test.com'), u'test@test.com')

    def test_to_address_string_list(self):
        self.assertEqual(builder.to_address_string_list(
            u'Test <test@test.com>'), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string_list(
            (u'Test', u'test@test.com')), u'Test <test@test.com>')
        self.assertEqual(builder.to_address_string_list(
            u'test@test.com'), u'test@test.com')
        self.assertEqual(builder.to_address_string_list(
            [u'test@test.com']), u'test@test.com')
        self.assertEqual(builder.to_address_string_list(
            [u'test@test.com', u'test2@test.com']), u'test@test.com, test2@test.com')
        self.assertEqual(builder.to_address_string_list(
            [u'Test <test@test.com>', u'test2@test.com']), u'Test <test@test.com>, test2@test.com')
        self.assertEqual(builder.to_address_string_list(
            [(u'Test', u'test@test.com'), u'test2@test.com']), u'Test <test@test.com>, test2@test.com')
        self.assertEqual(builder.to_address_string_list([(u'Test', u'test@test.com'), (
            u'Test2', u'test2@test.com')]), u'Test <test@test.com>, Test2 <test2@test.com>')

    def test_minimal(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_to=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_cc(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_cc=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_bcc(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_bcc=u'Example <example@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_html_text(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_to=u'Example <example@example.com>', html_text=u'<b>Some Bold Text</b>')
        self.assertIsNotNone(msg)

    def test_both_texts(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>',
                                plain_text=u'Some Text', html_text=u'<b>Some Bold Text</b>')
        self.assertIsNotNone(msg)

    def test_multi_recipients(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>',
                                send_cc=u'Example2 <example2@example.com>', send_bcc=u'Example3 <example3@example.com>', plain_text=u'Some Text')
        self.assertIsNotNone(msg)

    def test_plain_byte_text(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_to=u'Example <example@example.com>', plain_text=b'Some Text')
        self.assertIsNotNone(msg)

    def test_html_byte_text(self):
        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject',
                                send_to=u'Example <example@example.com>', html_text=b'<b>Some Bold Text</b>')
        self.assertIsNotNone(msg)

    def test_attachment_list(self):
        gif_data = None
        with open('tests/test_files/1x1.gif', 'rb') as f:
            gif_data = f.read()

        text_data = None
        with open('tests/test_files/text.txt', 'rb') as f:
            text_data = f.read()

        audio_data = None
        with open('tests/test_files/drip.mp3', 'rb') as f:
            audio_data = f.read()

        arbitary_data = None
        with open('tests/test_files/data', 'rb') as f:
            arbitary_data = f.read()

        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text', attachment_list=[
            Attachment(u'1x1.gif', gif_data),
            Attachment(u'text.txt', text_data),
            Attachment(u'drip.mp3', audio_data),
            Attachment(u'data', arbitary_data)])
        self.assertIsNotNone(msg)

    def test_inline_attachment_list(self):
        gif_data = None
        with open('tests/test_files/1x1.gif', 'rb') as f:
            gif_data = f.read()

        msg = builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text', inline_attachment_dict={
            'content_id_1': Attachment(u'1x1.gif', gif_data),
        })
        self.assertIsNotNone(msg)

    def test_inline_attachment_list_error(self):
        arbitary_data = None
        with open('tests/test_files/data', 'rb') as f:
            arbitary_data = f.read()

        with self.assertRaises(RuntimeError):
            builder.build_msg(u'Test <test@test.com>', u'The Subject', send_to=u'Example <example@example.com>', plain_text=u'Some Text', inline_attachment_dict={
                'content_id_1': Attachment(u'data', arbitary_data),
            })


if __name__ == u'__main__':
    unittest.main()
