import errno
import time
import socket
import asyncore
import asynchat
import ssl
import base64

__version__ = u'Python SMTP proxy version 0.2 - edit'


NEWLINE = b'\n'
EMPTYSTRING = b''


class SMTPChannel(asynchat.async_chat):
    COMMAND = 0
    DATA = 1

    def __init__(self, server, conn, addr):
        asynchat.async_chat.__init__(self, conn)
        self.__server = server
        self.__conn = conn
        self.__addr = addr
        self.__line = []
        self.__state = self.COMMAND
        self.__greeting = 0
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = b''
        self.__fqdn = socket.getfqdn()
        try:
            self.__peer = conn.getpeername()
        except socket.error as err:
            # a race condition  may occur if the other end is closing
            # before we can get the peername
            self.close()
            if err[0] != errno.ENOTCONN:
                raise
            return
        self.push(u'220 {} {}'.format(self.__fqdn, __version__).encode())
        self.set_terminator(b'\r\n')

    # Overrides base class for convenience
    def push(self, msg):
        asynchat.async_chat.push(self, msg + b'\r\n')

    # Implementation of base class abstract method
    def collect_incoming_data(self, data):
        self.__line.append(data)

    # Implementation of base class abstract method
    def found_terminator(self):
        line = EMPTYSTRING.join(self.__line)
        self.__line = []
        if self.__state == self.COMMAND:
            if not line:
                self.push(b'500 Error: bad syntax')
                return
            method = None
            i = line.find(b' ')
            if i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i+1:].strip()
            method = getattr(self, u'smtp_' + command.decode(), None)
            if not method:
                self.push(u'502 Error: command "{}" not implemented'.format(command).encode())
                return
            method(arg)
            return
        else:
            if self.__state != self.DATA:
                self.push(b'451 Internal confusion')
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 821, Section 4.5.2.
            data = []
            for text in line.split(b'\r\n'):
                if text and text[0] == b'.':
                    data.append(text[1:])
                else:
                    data.append(text)
            self.__data = NEWLINE.join(data)
            status = self.__server.process_message(self.__peer,
                                                   self.__mailfrom,
                                                   self.__rcpttos,
                                                   self.__data)
            self.__rcpttos = []
            self.__mailfrom = None
            self.__state = self.COMMAND
            self.set_terminator(b'\r\n')
            if not status:
                self.push(b'250 Ok')
            else:
                self.push(status)

    # SMTP and ESMTP commands
    def smtp_HELO(self, arg):
        if not arg:
            self.push(b'501 Syntax: HELO hostname')
            return
        if self.__greeting:
            self.push(b'503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            self.push(u'250 {}'.format(self.__fqdn).encode())

    def smtp_NOOP(self, arg):
        if arg:
            self.push(b'501 Syntax: NOOP')
        else:
            self.push(b'250 Ok')

    def smtp_QUIT(self, arg):
        # args is ignored
        self.push(b'221 Bye')
        self.close_when_done()

    # factored
    def __getaddr(self, keyword, arg):
        address = None
        keylen = len(keyword)
        if arg[:keylen].upper() == keyword:
            address = arg[keylen:].strip()
            if not address:
                pass
            elif address[0] == b'<' and address[-1] == b'>' and address != b'<>':
                # Addresses can be in the form <person@dom.com> but watch out
                # for null address, e.g. <>
                address = address[1:-1]
        return address

    def smtp_MAIL(self, arg):
        address = self.__getaddr(b'FROM:', arg) if arg else None
        if not address:
            self.push(b'501 Syntax: MAIL FROM:<address>')
            return
        if self.__mailfrom:
            self.push(b'503 Error: nested MAIL command')
            return
        self.__mailfrom = address
        self.push(b'250 Ok')

    def smtp_RCPT(self, arg):
        if not self.__mailfrom:
            self.push(b'503 Error: need MAIL command')
            return
        address = self.__getaddr(b'TO:', arg) if arg else None
        if not address:
            self.push(b'501 Syntax: RCPT TO: <address>')
            return
        self.__rcpttos.append(address)
        self.push(b'250 Ok')

    def smtp_RSET(self, arg):
        if arg:
            self.push(b'501 Syntax: RSET')
            return
        # Resets the sender, recipients, and data, but not the greeting
        self.__mailfrom = None
        self.__rcpttos = []
        self.__data = b''
        self.__state = self.COMMAND
        self.push(b'250 Ok')

    def smtp_DATA(self, arg):
        if not self.__rcpttos:
            self.push(b'503 Error: need RCPT command')
            return
        if arg:
            self.push(b'501 Syntax: DATA')
            return
        self.__state = self.DATA
        self.set_terminator(b'\r\n.\r\n')
        self.push(b'354 End data with <CR><LF>.<CR><LF>')

    # Extensions Start

    def smtp_AUTH(self, arg):
        auth = self.__server._auth
        if isinstance(auth, dict) and u'user' in auth and u'password' in auth:
            user = auth[u'user']
            password = auth[u'password']

            s = base64.stanard_b64encode(u'\0%s\0%s'.format(user, password).encode()).decode()

            if arg == u'PLAIN {}'.format(s).encode():
                self.push(b'235 Authentication successful')
            else:
                self.push(b'535 SMTP Authentication unsuccessful/Bad username or password')
        else:
            self.push(b'454 Temporary authentication failure')

    def smtp_EHLO(self, arg):
        if not arg:
            self.push(b'501 Syntax: HELO hostname')
        elif self.__greeting:
            self.push(b'503 Duplicate HELO/EHLO')
        else:
            self.__greeting = arg
            if isinstance(self.__conn, ssl.SSLSocket):
                self.push(u'250 {}'.format(self.__fqdn).encode())
            else:
                self.push(u'250-{}'.format(self.__fqdn).encode())
                self.push(b'250 STARTTLS')

    def smtp_STARTTLS(self, arg):
        if arg:
            self.push(b'501 Syntax error (no parameters allowed)')
        elif self.__server._starttls and not isinstance(self.__conn, ssl.SSLSocket):
            self.push(b'220 Ready to start TLS')
            self.__conn.settimeout(30)
            self.__conn = self.__server._ssl_ctx.wrap_socket(self.__conn, server_side=True)
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
            self.push(b'454 TLS not available due to temporary reason')


class SMTPServer(asyncore.dispatcher):
    def __init__(self, localaddr, remoteaddr, ssl_ctx=None, starttls=True, auth=None):
        self._localaddr = localaddr
        self._remoteaddr = remoteaddr
        self._ssl_ctx = ssl_ctx
        self._starttls = starttls
        self._auth = auth
        asyncore.dispatcher.__init__(self)
        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            # try to re-use a server port if possible
            self.set_reuse_addr()
            self.bind(localaddr)
            self.listen(5)
        except:
            # cleanup asyncore.socket_map before raising
            self.close()
            raise

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            conn, addr = pair
            if self._ssl_ctx and not self._starttls:
                conn = self._ssl_ctx.wrap_socket(conn, server_side=True)
            channel = SMTPChannel(self, conn, addr)

    def process_message(self, peer, mailfrom, rcpttos, data):
        raise NotImplementedError
