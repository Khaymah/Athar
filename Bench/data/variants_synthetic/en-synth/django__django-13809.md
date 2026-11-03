can we add a --skip-checks option to the runserver management command? would be consistent with the other management commands that run system checks. I only want the checks running in CI/CD, not a 15-20 s wait on every reload while I'm developing.
related StackOverflow: https://stackoverflow.com/questions/41438593/skip-system-checks-on-django-server-in-debug-mode-in-pycharm/41725866
