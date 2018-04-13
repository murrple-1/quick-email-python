import asyncore, asynchat
import ssl
import smtpd
from email.base64mime import encode as encode_base64

class SMTPChannel(smtpd.SMTPChannel):
    def smtp_AUTH(self, arg):
        user = self.__server.auth.get('user')
        password = self.__server.auth.get('password')
        s = encode_base64("\0%s\0%s" % (user, password), eol="")
        if arg == 'PLAIN {}'.format(s):
            self.push('235 Authentication successful')
        else:
            self.push(
                '535 SMTP Authentication unsuccessful/'
                'Bad username or password')

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
        elif self.__greeting:
            self.push('503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            if isinstance(self.__conn,ssl.SSLSocket):
                self.push('250-%s' % self.__fqdn)
                self.push('250 AUTH PLAIN')
            else:
                self.push('250-%s' % self.__fqdn)
                self.push('250 STARTTLS')

    def smtp_STARTTLS(self, arg):
        if arg:
            self.push('501 Syntax error (no parameters allowed)')
        elif self.__server.starttls and not isinstance(self.__conn,ssl.SSLSocket):
            self.push('220 Ready to start TLS')
            self.__conn.settimeout(30)
            self.__conn = self.__server.ssl_ctx.wrap_socket(self.__conn, server_side=True)
            self.__conn.settimeout(None)

            # re-init channel
            asynchat.async_chat.__init__(self, self.__conn)
            self.__line = []
            self.__state = self.COMMAND
            self.__greeting = 0
            self.__mailfrom = None
            self.__rcpttos = []
            self.__data = ''
        else:
            self.push('454 TLS not available due to temporary reason')

class SMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, ssl_ctx=None, starttls=True, auth=False):
        self.ssl_ctx = ssl_ctx
        self.starttls = starttls
        self.auth = auth
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            conn, addr = pair
            if self.ssl_ctx and not self.starttls:
                conn = self.ssl_ctx.wrap_socket(conn, server_side=True)

            channel = SMTPChannel(self, conn, addr)
