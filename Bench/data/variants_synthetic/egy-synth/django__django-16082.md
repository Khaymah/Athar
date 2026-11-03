لما بعمل combine لـ query expressions بالـ `MOD` operator والـ operands أنواعهم مختلفة (Decimal و Integer)، الـ `output_field` مش بيتعمله resolve.
باقي الـ mathematical operators بتعمل resolve للنتيجة بتاعة Decimal + Integer إنها Decimal، إنما الـ MOD لأ. المفروض الـ MOD مع operands Decimal و Integer تطلع Decimal زي باقي الـ operators بالظبط.
