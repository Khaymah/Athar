سلام، ملي كنجمع query expressions بالـ operator `MOD`، الـ `output_field` ماكيتحددش إلا كانو les types ديال les opérandes مختلفين (Decimal و Integer).
les opérateurs الحسابيين الآخرين كيردو نتيجة Decimal + Integer هي Decimal، ولكن MOD لا.
المفروض MOD مع Decimal و Integer يعطي Decimal، بحال باقي les opérateurs.
