import smtplib

from email.utils import COMMASPACE

def send_msg(msg, host, port, username=None, password=None, is_tls=False):
    smtp = smtplib.SMTP(host, port)
    if is_tls:
        smtp.starttls()

    if username and password:
        smtp.login(username, password)

    _all_recipients = all_recipients(msg)

    smtp.sendmail(msg['From'], _all_recipients, msg.as_string())
    smtp.quit()


def all_recipients(msg):
    all_recipients = set()

    if 'To' in msg:
        all_recipients.update(msg['To'].split(COMMASPACE))

    if 'CC' in msg:
        all_recipients.update(msg['CC'].split(COMMASPACE))

    if 'BCC' in msg:
        all_recipients.update(msg['BCC'].split(COMMASPACE))

    return all_recipients
