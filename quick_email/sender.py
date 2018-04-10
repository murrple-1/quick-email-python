import smtplib

def send_msg(host, port, username, password, is_tls, send_from, msg):
    smtp = smtplib.SMTP(host, port)
    if is_tls:
        smtp.starttls()
    smtp.login(username, password)

    _all_recipients = all_recipients(msg)

    smtp.sendmail(send_from, _all_recipients, msg.as_string())
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
