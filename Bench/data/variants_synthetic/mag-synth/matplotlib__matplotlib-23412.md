سلام، فـ les objets Patch، l'offset ديال `linestyle` ملي كيكون dash tuple ماعندو حتى تأثير على الخط ديال edge.
هادا le repro: جوج `Rectangle` فوق بعضياتهم، نفس الـ dash pattern ولكن offsets مختلفين [[A1]]
النتيجة: les dashes ديال edge كيطلعو فوق بعضياتهم، l'offset مكيتحسبش، شوف [[A2]]
المفروض l'offset يزحزح les dashes بحال `Line2D`، هادا le code ديال `Line2D` [[A3]] وهادا الـ output ديالو [[A4]]
نفس المشكل كاين حتى ف `Ellipse`.
شفتو ف 3.3.4 (macOS، backend MacOSX) و 3.5.0 (Ubuntu 18.04، backend agg).
