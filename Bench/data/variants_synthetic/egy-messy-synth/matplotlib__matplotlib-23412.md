الoffset في `linestyle` لما يبقي dash tuple ملوش اي تاثير علي ال edge line في الPatch objects عملت repro باتنين `Rectangle` فوق بعض نفس الdash pattern bs offsets مختلفه [[A1]] والdashes طالعه فوق بعض كان الoffset مش موجود [[A2]]
نفس الحكايه في `Ellipse` كمان
المفروض الoffset يزق الdashes زي ما بيحصل في `Line2D` ده الكود [[A3]] ودي النتيجه بتاعته [[A4]] حصلت معايا علي 3.3.4 (macOS و MacOSX backend) وعلي 3.5.0 (Ubuntu 18.04 و agg backend)
