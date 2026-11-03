lama ba3mel IsolationForest.fit() 3ala pd.DataFrame byetla3li el warning da:
[[A1]]
w da byes7al bas lama el contamination tb2a qeema gher el default, ya3ni msh "auto". el warning ghalat aslan, el X feeha feature names saleema, w howa tale3 men fit() nafsaha msh men predict 3ala ndarray.
ana shakek en lama contamination != "auto" el fit btnady predict 3ala el training data 3ashan te7seb offset_ (fe sklearn/ensemble/_iforest.py 7awaleen L337).
el repro:
[[A2]]
el mafrood mayetla3sh el warning da 5ales wa2t el fit. ana 3ala sklearn 1.2.1 w pandas 1.5.3, w el versions kollaha hena:
[[A3]]
