from quick_email.builder import build_msg, Attachment
from quick_email.sender import send_msg

def send_email(host, port, username, password, is_tls, send_from, send_to, send_cc, send_bcc, subject, plain_text, html_text, attachment_list=None, inline_attachment_dict=None):
    msg = build_msg(send_from, send_to, send_cc, send_bcc, subject, plain_text, html_text, attachment_list=attachment_list, inline_attachment_dict=inline_attachment_dict)
    send_msg(host, port, username, password, is_tls, send_from, msg)
