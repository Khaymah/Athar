فيه مشكلة في napoleon مع الـ Parameters بتاعة numpy style: الـ numpydoc guide (section 4) بيسمح إنك تجمع كذا param في سطر واحد، بس docstring زي ده
[[A1]]
بيتعرض غلط في الـ HTML، ودي صورة اللي بيطلعلي:
[[A2]]
ولو زوّدت optional كده
[[A3]]
الـ output بيفضل هو هو زي الصورة بالظبط، ومفيش أي حاجة بتقول إنه optional خالص.
المفروض يتعرض تقريبًا كده: x1, x2 (_array_like, optional_) - Input arrays, description of x1, x2.
Sphinx 3.0.3 و Python 3.7.7 على macOS 10.15.5، على Firefox و Safari. والـ extensions:
[[A4]]
