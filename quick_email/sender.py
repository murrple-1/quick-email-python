import smtplib

def send_msg(host, port, username, password, is_tls, send_from, msg):
    smtp = smtplib.SMTP(host, port)
    if is_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to_all, msg.as_string())
    smtp.quit()
