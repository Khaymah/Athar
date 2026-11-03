`Text` بياخد الantialiasing دايما من `rcParams["text.antialiased"]` الglobal مع ان باقى الartists تقدر تتحكم فيها لكل artist لوحده ب `set_antialiased` / `get_antialiased`
عايزين نضيف `get_antialiased` و `set_antialiased` ل `Text` و لو محتاجه نعدل `Annotation` كمان و لازم القيمه دى تتستخدم فعلا وقت الdraw msh bas tet5zn
ع فكره هنحتاج نلمس الbackends عشن بدل ما يقرو `rcParams["text.antialiased"]` على طول ياخدوها من الstate بتاعت `GraphicsContext`
