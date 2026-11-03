الـ debug error view اللي في django/views/debug.py مش بيعمل حساب لـ exc.__suppress_context__ (PEP 415). ده view بيطلّع المشكلة، بيرمي ValueError from None وهو بيعمل handle لـ RuntimeError
[[A1]]
الـ debug page لسه بتعرض الـ RuntimeError، عكس الـ traceback بتاع Python نفسه. أنا شايف إن السبب في explicit_or_implicit_cause() اللي جوه get_traceback_frames()، عمرها ما بتشيك على __suppress_context__
[[A2]]
ودي النسخة اللي بقترحها، مبسّطة لـ Python 3
[[A3]]
