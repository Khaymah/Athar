`EmailMessage.message()` بيكراش لو اسم الجهاز `DNS_NAME` مش ASCII زى `正宗` و `email.encoding` مش unicode زى `iso-8859-1`
جربها keda غير الhostname لحاجه مش فى iso-8859-1 وشغل التستات بتاعت الmail هتلاقى `test_unicode_dns` فى `tests/mail/tests.py` بيفشل
اول حاجه `UnicodeEncodeError` [[A2]] وبعدين واحد تانى وهو بيهاندل الاولانى [[A3]]
السبب ان `Message-ID` الى بيتحط ب `make_msgid(domain=DNS_NAME)` جوا `django/core/mail/message.py` بيتعمله encode بالcharset ده فبيضرب
ومش مشكلة تستات bas django لازم يعمل encode للرساله صح
اقتراحى نحول الdomain ل punycode فى `django.core.mail.utils` او `django.core.mail.message` قبل ما يتستخدم والتيست الى مقترحه [[A1]]
