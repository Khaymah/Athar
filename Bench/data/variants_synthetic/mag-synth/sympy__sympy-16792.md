`autowrap` مع `backend='cython'` ماخدامش ملي شي argument ديال array ماكاينش فـ الـ `expr` لي كنديرو ليه wrap.
الـ repro: `MatrixSymbol('x', 2, 1)` كـ argument و `expr = 1.0`، الـ call خاصو يرجع `1.0`:
[[A1]]
ولكن كيطلع ليا هاد l'erreur (`TypeError: only size-1 arrays can be converted to Python scalars`):
[[A2]]
السبب هو la fonction C لي كتتولد عندها signature غالطة، `x` خاصو يكون `double *` ماشي `double`:
[[A3]]
إلا كان `expr` كيعتمد على كاع les arguments، بحال `expr = x[0,0]`، كولشي خدام مزيان:
[[A4]]
علاش مهم؟ حيت بعض les libs الخارجية (بحال numerical integration) خاصهم signature ثابتة واخا شي arguments ماكيتستعملوش. وكنشك بلي le bug كاين فـ `codegen`.
