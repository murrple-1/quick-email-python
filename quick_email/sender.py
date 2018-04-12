import smtplib

from email.utils import COMMASPACE

def send_msg(msg, host, port, username=None, password=None, ssl=False):
    smtp = None
    if not ssl:
        smtp = smtplib.SMTP(host, port)
    else:
        smtp = smtplib.SMTP_SSL(host, port)

    if username and password:
        smtp.login(username, password)

    _all_recipients = all_recipients(msg)

    smtp.sendmail(msg[u'From'], _all_recipients, msg.as_string())
    smtp.quit()


def all_recipients(msg):
    all_recipients = set()

    if u'To' in msg:
        all_recipients.update(msg[u'To'].split(COMMASPACE))

    if u'CC' in msg:
        all_recipients.update(msg[u'CC'].split(COMMASPACE))

    if u'BCC' in msg:
        all_recipients.update(msg[u'BCC'].split(COMMASPACE))

    return all_recipients
