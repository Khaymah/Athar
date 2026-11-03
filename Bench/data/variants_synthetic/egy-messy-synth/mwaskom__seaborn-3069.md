اقتراح: scales ال `so.Nominal` (حتى اللى بتبقا inferred) المفروض تتصرف زى الaxis الcategorical ف plots seaborn الcategorical يعنى 3 حاجات
الlimits تبقا +/- 0.5 حولين اول و اخر tick مش منطق الmargins العادى - مفيش grid حتى لو الstyle الشغال بيرسمها - و لو هيا علي y نقلب الaxis
التنفيذ: الاولانيه صعبه شويا الحل اللى ف دماغي artist مخفى فيه sticky edges و margin 0 bas hacky و ممكن نحط الsticky edges على الspine
التانيه غالبا ف `Plotter._finalize_figure` بس مش عارف ازاى اليوزر يفرض الgrid من الtheme ممكن الgrid يتظبط على الscale نفسها
التالته سهله بس مش واضح مكانها فين
