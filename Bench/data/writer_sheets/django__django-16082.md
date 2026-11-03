# django__django-16082

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. Query expressions combined with `MOD` operator: `output_field` not resolved when operand types differ (Decimal and Integer)
2. Other mathematical operators resolve Decimal + Integer result to Decimal; MOD doesn't
3. Expected: MOD with Decimal and Integer operands resolves to Decimal, same as other operators

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
