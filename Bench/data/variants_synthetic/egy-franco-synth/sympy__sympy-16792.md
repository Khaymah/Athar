el autowrap bel backend='cython' bybooz lama ykoon feeh array argument msh mawgood fel expr elly ba3melo wrap. da el repro, el x 3obara 3an MatrixSymbol('x', 2, 1) wel expr = 1.0, ya3ni el mafrood el call yrag3 1.0:
[[A1]]
bas badal keda bytal3li:
[[A2]]
el moshkla en el C function elly btetwalled el signature bta3ha ghalat, el x el mafrood tb2a `double *` msh `double`:
[[A3]]
law el expr me3tamed 3ala kol el arguments (zay expr = x[0,0]) byshtghal 3adi:
[[A4]]
ana me7tag da 3shan feeh external libs (numerical integration masalan) 3ayza signature sabet 7atta law feeh args msh mesta5dama. w shakek en el bug fel codegen.
