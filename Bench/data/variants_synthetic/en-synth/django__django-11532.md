EmailMessage.message() crashes when the hostname (DNS_NAME) is non-ASCII, e.g. 正宗, and email.encoding is non-unicode like iso-8859-1. the Message-ID is set via make_msgid(domain=DNS_NAME) in django/core/mail/message.py, gets encoded to that charset and fails.
repro: set your machine hostname to something that isn't iso-8859-1 and run the mail tests, test_unicode_dns in tests/mail/tests.py fails. first there's a UnicodeEncodeError:
[[A2]]
then during handling of that, a second one:
[[A3]]
this isn't just a test problem, Django should encode the message properly. my suggestion: convert the domain to punycode in django.core.mail.utils or django.core.mail.message before using it. test I'd propose:
[[A1]]
