import mimetypes
import six

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE

class Attachment(object):
    def __init__(self, filename, bytes):
        self.filename = filename
        self.bytes = bytes

def build_msg(send_from, send_to, send_cc, send_bcc, subject, plain_text, html_text, attachment_list=None, inline_attachment_dict=None):
    msg = MIMEMultipart('mixed')

    if isinstance(send_from, six.string_types):
        msg['From'] = send_from
    else:
        msg['From'] = '"{0}" <{1}>'.format(send_from[0], send_from[1])

    if send_to:
        if isinstance(send_to, six.string_types):
            msg['To'] = send_to
        else:
            msg['To'] = COMMASPACE.join(send_to)

    if send_cc:
        if isinstance(send_cc, six.string_types):
            msg['CC'] = send_cc
        else:
            msg['CC'] = COMMASPACE.join(send_cc)

    if send_bcc:
        if isinstance(send_bcc, six.string_types):
            msg['BCC'] = send_bcc
        else:
            msg['BCC'] = COMMASPACE.join(send_bcc)

    msg['Subject'] = subject

    text_msg = MIMEMultipart('alternative')

    if plain_text:
        if isinstance(plain_text, six.text_type):
            text_msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
        else:
            text_msg.attach(MIMEText(plain_text, 'plain'))

    if html_text:
        if isinstance(html_text, six.text_type):
            text_msg.attach(MIMEText(html_text, 'html', 'utf-8'))
        else:
            text_msg.attach(MIMEText(html_text, 'html'))

    msg.attach(text_msg)

    if attachment_list is not None:
        for attachment in attachment_list:
            type, encoding = mimetypes.guess_type(attachment.filename)
            if type is None or encoding is not None:
                type = 'application/octet-stream'

            main_type, sub_type = type.split('/', 1)

            part = None
            if main_type == 'text':
                part = MIMEText(attachment.bytes, sub_type)
            elif main_type == 'image':
                part = MIMEImage(attachment.bytes, sub_type)
            elif main_type == 'audio':
                part = MIMEAudio(attachment.bytes, sub_type)
            else:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(attachment.bytes)
                encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            msg.attach(part)

    if inline_attachment_dict is not None:
        for content_id, attachment in inline_attachment_dict.iteritems():
            type, encoding = mimetypes.guess_type(attachment.filename)
            if type is None or encoding is not None:
                type = 'application/octet-stream'

            main_type, sub_type = type.split('/', 1)

            part = None
            if main_type == 'image':
                part = MIMEImage(attachment.bytes, sub_type)
            else:
                raise RuntimeError('inline attachment must be an \'image\'')

            part.add_header('Content-Disposition', 'inline', filename=attachment.filename)
            part.add_header('Content-ID', '<{content_id}>'.format(content_id=content_id))
            part.add_header('X-Attachment-Id', content_id)
            msg.attach(part)

    return msg
