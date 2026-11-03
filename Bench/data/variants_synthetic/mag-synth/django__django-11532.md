`EmailMessage.message()` كيكراشي ملي الhostname (`DNS_NAME`) فيه حروف ماشي ASCII بحال `正宗` و `email.encoding` ماشي unicode بحال `iso-8859-1`.
الheader `Message-ID` اللي كيتحط ب `make_msgid(domain=DNS_NAME)` ف `django/core/mail/message.py` كيتحاول يتencoda بداك le charset وكيطيح.
باش تعاودها: بدل الhostname ديال الماكينة لشي حاجة ماكايناش ف iso-8859-1 وطلق les tests ديال mail، غادي يطيح `test_unicode_dns` ف `tests/mail/tests.py`.
الtracebacks: الأول `UnicodeEncodeError` [[A2]]، ومن بعد وسط الhandling ديالو كيطلع واحد آخر [[A3]].
هادشي ماشي غير مشكل ديال tests، Django خاصو يencodi le message مزيان.
الاقتراح ديالي: نحولو الdomain ل punycode ف `django.core.mail.utils` ولا `django.core.mail.message` قبل ما نستعملوه.
وهادا le test اللي كنقترح: [[A1]]
