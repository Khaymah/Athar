`IterativeImputer` مفيهوش `fill_value` خالص مع ان الdocs بتقول `initial_strategy="constant"` زى strategy بتاعت `SimpleImputer` بس مفيش طرقه تختار الconstant
ف `SimpleImputer.fill_value` بتتستخدم مع `strategy="constant"` و الdefault بتاعها 0 للnumeric و `"missing_value"` للstr/object
عايزين `fill_value` يتضاف ل `IterativeImputer` و يتستخدم لما `initial_strategy="constant"` و كمان يقبل `np.nan` ك `fill_value` 3ashan الestimators اللى decision tree-based
