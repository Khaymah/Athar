في الـ Patch objects الـ offset اللي في الـ dash-tuple بتاع الـ `linestyle` مالوش أي تأثير على الـ edge line.
ده repro فيه اتنين `Rectangle` فوق بعض بنفس الـ dash pattern بس offsets مختلفة:
[[A1]]
الـ dashes بتاعة الـ edge بتيجي فوق بعض بالظبط والـ offset متجاهَل: [[A2]]
المفروض الـ offset يزحلق الـ dashes زي ما بيحصل في `Line2D`، ده كود الـ Line2D [[A3]] ودي النتيجة بتاعته [[A4]]
ونفس المشكلة بتحصل مع الـ `Ellipse` patch. شفتها على 3.3.4 (macOS بالـ MacOSX backend) وعلى 3.5.0 (Ubuntu 18.04 بالـ agg backend)
