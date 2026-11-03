فيه مشكلة في الـ mask propagation في الـ arithmetic بتاع NDDataRef في astropy 5.3 لما operand واحد مفيهوش mask، وفي 5.2 كان شغال عادي. ده بيحصل مع handle_mask=np.bitwise_or، وبيطلعلي TypeError على الـ | بين int و NoneType.
دي الـ session بتاعتي: الـ mask × constant والـ mask × no-mask بيفشلوا، أما حالات الـ no-mask والـ mask × mask شغالة تمام
[[A1]]
تخميني إن الـ mask اللي مش موجودة بتتعامل كإنها Nones، فالـ bitwise_or بيستلم int و None. اللي المفروض يحصل: لو operand واحد بس عنده mask، ينسخ الـ mask دي للـ output زي ما كان بيعمل في v5.2. ودي الـ version info
[[A2]]
