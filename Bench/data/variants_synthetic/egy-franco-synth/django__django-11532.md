el EmailMessage.message() btedrab crash lama el hostname (DNS_NAME) yeb2a non-ASCII zay 正宗 wel email.encoding yeb2a non-unicode zay iso-8859-1. el Message-ID byet7at b make_msgid(domain=DNS_NAME) fi django/core/mail/message.py w ba3deen byet3amalo encode lel charset da fa byefshal.
3shan tshoofha: ghayar el hostname bta3 el gehaz l 7aga msh iso-8859-1 w shaghal el mail tests, hatla2i test_unicode_dns fi tests/mail/tests.py byefshal. el awel byetla3 UnicodeEncodeError
[[A2]]
w ba3deen w howa bey3mel handle lel awalani byetla3 wa7ed tani
[[A3]]
w di msh moshklet test w bas, Django el mafrood ye3mel encode lel message sa7. e2tera7i n7awel el domain l punycode fi django.core.mail.utils aw django.core.mail.message 2abl ma nesta5demo. w da el test elli ba2tere7o
[[A1]]
