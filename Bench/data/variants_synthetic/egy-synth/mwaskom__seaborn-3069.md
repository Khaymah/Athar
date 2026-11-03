عندي اقتراح للـ `so.Nominal` scales (وكمان اللي بتتعمل infer): عايزها تتصرف زي الـ categorical axis بتاع الـ categorical plots في seaborn. يعني 3 حاجات:
1) الـ axis limits تبقى +/- 0.5 حوالين أول وآخر tick، مش بالـ margin logic العادي
2) مفيش grid، حتى لو الـ style الشغال بيرسم grid
3) لو هي على الـ y axis، الـ axis يتعمله invert
ملاحظات: رقم 1 صعبة شوية، الطريقة اللي بقترحها invisible artist بـ sticky edges و margin 0 (hacky شوية)، أو يمكن sticky edges على الـ spine. رقم 2 غالباً مكانها في `Plotter._finalize_figure`، بس لسه مش عارف اليوزر هيعمل force للـ grid من الـ theme إزاي، يمكن الـ grid يتحط على الـ scale. رقم 3 سهلة بس مش متأكد مكانها فين.
