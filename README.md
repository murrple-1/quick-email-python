# quick-email
Quick-and-Dirty Email Sender

[![Build Status](https://travis-ci.org/murrple-1/quick-email-python.svg?branch=master)](https://travis-ci.org/murrple-1/quick-email-python) [![Coverage Status](https://coveralls.io/repos/github/murrple-1/quick-email-python/badge.svg?branch=master)](https://coveralls.io/github/murrple-1/quick-email-python?branch=master) [![PyPI version](https://badge.fury.io/py/quick-email.svg)](https://badge.fury.io/py/quick-email)

Emails are ubiquitous, but not super-straightforward from a programming standpoint. The standards in use (SMTP, MIME) are powerful, but complex if you want to do anything nicer than a simple plain-test email. This library was built and iterated upon for my personal projects, and it might just help you too.

Supports both Python `>=v2.7` and `>=3.3`.

# Installation

`pip install quick-email`

# Usage

## Send Email

### `quick_email.send_email(host, port, send_from, subject[, send_to[, send_cc[, send_bcc[, plain_text[, html_text[, attachment_list[, inline_attachment_dict[, username[, password[, require_starttls]]]]]]]]]])`
My super-useful utility function. Creates and sends an email in one fell swoop. All parameters are passed to the functions below.

## Create Message

### `quick_email.build_msg(send_from, subject[, send_to[, send_cc[, send_bcc[, plain_text[, html_text[, attachment_list[, inline_attachment_dict]]]]]]])`
Creates a `email.message.Message` for deferred sending or additional preparing.

Email addresses can be a string (either of form `example@example.com` or `Example Name <example@example.com>`), or a tuple, as returned by `email.utils.parseaddr`.

`send_from` is a single email address.

`subject` is the Subject string of the email.

`send_to`, `send_cc`, and `send_bcc` are all either singular email addresses, or `list`s of email addresses if you have multiple recipients. At least one address must be present among the parameters, otherwise an `AssertionError` will be raised.

`plain_text` is the plain-text part of the email. `html_text` is the HTML part of the email. You can include one or both, but if no text is present, an `AssertionError` will be raised.

`attachment_list` is an optional `list` of `quick_email.Attachment`s.

`inline_attachment_dict` is an optional `dict` of `str: quick_email.Attachment` form. The key is the CID of your attachment. In many email clients, you can include images inline in the HTML (ie `<img src="...">`). However, if the image you want to display is an attachment (and not at some URL), it's a little trickier. You must give your attachment a Content-ID (CID), and your `img` tag must look like `<img src="cid:my_attachment_cid">`. This may be preferred to the inline-base64 encoding (ie `<img src="data:image/jpeg;base64,...">`).

### `class quick_email.Attachment(filename, bytes)`
`filename` is the filename string.

`bytes` is the bytes-like object of the content.

## Send Message

### `quick_email.send_msg(msg, host, port[, username[, password[, require_starttls]]])`
Sends a `email.message.Message` to its recipients.

`msg` is the `email.message.Message`, which you may have built using `quick_email.build_msg`, or handcrafted youself.

`host` is the host string to connect to. Usually a [FQDN](https://en.wikipedia.org/wiki/Fully_qualified_domain_name), or an IP address.

`port` is the port number to connect to. Usually `25` for un-encrypted email.

`username` is the username of a username/password combo used to authenticate. Leave it off if your service is unauthenticated.

`password` is the password of a username/password combo used to authenticate. Leave it off if your service is unauthenticated.

`require_starttls` is a flag whether to request the message sending be encrypted. Defaults to `False`, but turn it on if you can.
