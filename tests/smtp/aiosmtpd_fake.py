import os
import time
import ssl
import asyncio
from six.moves import _thread

from aiosmtpd.smtp import SMTP as Server
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink as Handler

SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'8080'))


class MyController(Controller):
    def __init__(self, *args, **kwargs):
        Controller.__init__(self, *args, **kwargs)
        self._ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    def factory(self):
        return MyServer(self.handler, tls_context=self._ssl_context)


class MyServer(Server):
    async def smtp_AUTH(self, arg):
        if arg != 'PLAIN':
            await self.push('501 Syntax: AUTH PLAIN')
            return

        await self.push('334')

        second_line = await self._reader.readline()

        try:
            second_line = second_line.rstrip(b'\r\n').decode('ascii')
        except UnicodeDecodeError:
            await self.push('500 Error: Challenge must be ASCII')
            return

        if second_line != '':
            self.authenticated = True
            await self.push('235 Authentication successful')
        else:
            await self.push('535 Invalid credentials')


def _smtp_server_func():
    controller = MyController(Handler(), hostname=u'localhost', port=SMTP_PORT)
    controller.start()

    try:
        while True:
            time.sleep(5.0)
    finally:
        controller.stop()


_smtp_server_thead = None
def smtp_server_start():
    global _smtp_server_thead
    if _smtp_server_thead is None:
        _smtp_server_thead = _thread.start_new_thread(_smtp_server_func, ())
        time.sleep(1.0)
