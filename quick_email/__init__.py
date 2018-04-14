from quick_email.builder import build_msg, Attachment
from quick_email.sender import send_msg


def send_email(host, port, send_from, subject, send_to=None, send_cc=None, send_bcc=None, plain_text=None, html_text=None, attachment_list=None, inline_attachment_dict=None, username=None, password=None, require_starttls=False):
    msg = build_msg(send_from, subject, send_to=send_to, send_cc=send_cc, send_bcc=send_bcc, plain_text=plain_text,
                    html_text=html_text, attachment_list=attachment_list, inline_attachment_dict=inline_attachment_dict)
    send_msg(msg, host, port, username=username,
             password=password, require_starttls=require_starttls)

__all__ = [
    'build_msg',
    'Attachment',
    'send_msg',
    'send_email',
]
