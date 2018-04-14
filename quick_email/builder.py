import mimetypes
import six

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, parseaddr, formataddr


class Attachment(object):
    def __init__(self, filename, bytes):
        self.filename = filename
        self.bytes = bytes


def build_msg(send_from, subject, send_to=None, send_cc=None, send_bcc=None, plain_text=None, html_text=None, attachment_list=None, inline_attachment_dict=None):
    assert send_to or send_cc or send_bcc, u'At least one of send_to, send_cc, or send_bcc must exist'
    assert plain_text or html_text, u'At least one of plain_text or html_text must exist'

    msg = MIMEMultipart(u'mixed')

    msg[u'Subject'] = subject

    msg[u'From'] = to_address_string(send_from)

    if send_to:
        msg[u'To'] = to_address_string_list(send_to)

    if send_cc:
        msg[u'CC'] = to_address_string_list(send_cc)

    if send_bcc:
        msg[u'BCC'] = to_address_string_list(send_bcc)

    text_msg = MIMEMultipart(u'alternative')

    if plain_text:
        if isinstance(plain_text, six.text_type):
            text_msg.attach(MIMEText(plain_text, u'plain', u'utf-8'))
        else:
            text_msg.attach(MIMEText(plain_text.decode(), u'plain'))

    if html_text:
        if isinstance(html_text, six.text_type):
            text_msg.attach(MIMEText(html_text, u'html', u'utf-8'))
        else:
            text_msg.attach(MIMEText(html_text.decode(), u'html'))

    msg.attach(text_msg)

    if attachment_list is not None:
        for attachment in attachment_list:
            type, encoding = mimetypes.guess_type(attachment.filename)
            if type is None or encoding is not None:
                type = u'application/octet-stream'

            main_type, sub_type = type.split(u'/', 1)

            part = None
            if main_type == u'text':
                part = MIMEText(attachment.bytes.decode(), sub_type)
            elif main_type == u'image':
                part = MIMEImage(attachment.bytes, sub_type)
            elif main_type == u'audio':
                part = MIMEAudio(attachment.bytes, sub_type)
            else:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(attachment.bytes)
                encoders.encode_base64(part)

            part.add_header(u'Content-Disposition',
                            u'attachment', filename=attachment.filename)
            msg.attach(part)

    if inline_attachment_dict is not None:
        for content_id, attachment in six.iteritems(inline_attachment_dict):
            type, encoding = mimetypes.guess_type(attachment.filename)
            if type is None or encoding is not None:
                type = u'application/octet-stream'

            main_type, sub_type = type.split('/', 1)

            part = None
            if main_type == u'image':
                part = MIMEImage(attachment.bytes, sub_type)
            else:
                raise RuntimeError(u'inline attachment must be an \'image\'')

            part.add_header(u'Content-Disposition', u'inline',
                            filename=attachment.filename)
            part.add_header(
                u'Content-ID', u'<{content_id}>'.format(content_id=content_id))
            part.add_header(u'X-Attachment-Id', content_id)
            msg.attach(part)

    return msg


def to_address_string(address):
    if isinstance(address, six.string_types):
        return formataddr(parseaddr(address))
    else:
        return formataddr(address)


def to_address_string_list(addresses):
    if isinstance(addresses, (six.string_types, tuple)):
        return to_address_string(addresses)
    else:
        return COMMASPACE.join(to_address_string(addr) for addr in addresses)
