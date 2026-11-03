الـ EmailMessage.message() بتضرب crash لما الـ hostname (DNS_NAME) يبقى non-ASCII زي 正宗 والـ email.encoding يبقى non-unicode زي iso-8859-1. الـ Message-ID بيتحط بـ make_msgid(domain=DNS_NAME) في django/core/mail/message.py وبعدين بيتعمله encode للـ charset ده فبيفشل.
عشان تشوفها: غيّر الـ hostname بتاع الجهاز لحاجة مش iso-8859-1 وشغّل الـ mail tests، هتلاقي test_unicode_dns في tests/mail/tests.py بيفشل. الأول بيطلع UnicodeEncodeError
[[A2]]
وبعدين وهو بيعمل handle للأولاني بيطلع واحد تاني
[[A3]]
ودي مش مشكلة test وبس، Django المفروض يعمل encode للـ message صح. اقتراحي نحوّل الـ domain لـ punycode في django.core.mail.utils أو django.core.mail.message قبل ما نستخدمه. وده الـ test اللي بقترحه
[[A1]]
