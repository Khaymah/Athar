سلام، عندي مشكل فـ `MigrationLoader.load_disk` (`django.db.migrations.loader`): كيدير skip للـ migrations module `m` إلا كان `getattr(m, '__file__', None)` falsy.
الهدف ديال هاد le check هو يرفض les namespace packages ديال PEP-420، ولكن حتى les packages العاديين يقدرو يكونو بلا `__file__`. الـ doc ديال l'import ف Python كتقول بلي `__file__` اختياري، و l'import system يقدر يخليه ماشي محطوط (مثلا module متشارجي من database).
هادشي كيضرب les environnements ديال Python frozen لي ماكيحطوش `__file__` على les packages العاديين: الـ migrations لي كاينين ماكيتلقاوش. شوف tickets #30950 و #32177.
راه `__path__` ديال namespace packages هو iterable خاص، ماشي `list` (و `_NamespacePath` ديال CPython غير détail d'implémentation، ماخاصناش نعتامدو عليه).
بغيت نزيدو على le check ديال `__file__` هاد الشرط: `and isinstance(m.__path__, list)`.
الشروط: namespace packages خاصهم يبقاو مرفوضين للـ migrations، والسلوك مايتبدلش ف les environnements العاديين، وماتزيدش حتى شي feature أخرى ديال frozen.
