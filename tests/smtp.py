import os

SMTP_HOST = os.environ[u'SMTP_HOST']
SMTP_PORT = int(os.environ.get(u'SMTP_PORT', u'25'))
SMTP_USERNAME = os.environ[u'SMTP_USERNAME']
SMTP_PASSWORD = os.environ[u'SMTP_PASSWORD']
SMTP_RATE_LIMIT_SECONDS = float(os.environ.get(u'SMTP_RATE_LIMIT_SECONDS', u'10.0'))
