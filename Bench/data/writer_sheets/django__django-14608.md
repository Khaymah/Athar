# django__django-14608

**Repo:** `django/django`

## What the request must convey (all units, nothing extra)

1. Forms: non-field errors `ErrorList` gets `nonfield` CSS class; documented under rendering form error messages
2. FormSets: non-form errors get no equivalent CSS class
3. Request: add `nonform` CSS class to FormSet non-form errors
4. Goal: custom `ErrorList` can tell apart field errors, non-field errors (forms), non-form errors (FormSets)
5. Also document the `nonform` class for developers

## Attachments (paste the placeholder where you would paste the block)

_None: the request is prose only._
