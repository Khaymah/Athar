سلام، فـ les Forms، الـ `ErrorList` ديال non-field errors كتاخد CSS class سميتها `nonfield`، وهادشي موثق ف la partie ديال rendering form error messages.
ولكن فـ les FormSets، الـ non-form errors ماكتاخد حتى شي CSS class بحالها.
بغيت نزيدو CSS class `nonform` للـ non-form errors ديال FormSet، باش `ErrorList` custom يقدر يفرق بين field errors، و non-field errors (ديال forms)، و non-form errors (ديال FormSets).
وخاص حتى نديرو documentation للـ class `nonform` باش يستعملوها les développeurs.
