pylint بيعمل فولدر `.pylint.d` للـ data في الـ home بتاعي على طول.
عايزه يمشي على الـ XDG Base Directory Specification. حسب الـ spec الـ data المفروض تتحط في `$HOME/.local/share/<PROGRAM_NAME>`، وكمان الـ spec محدد `$HOME/.cache/<PROGRAM_NAME>` للـ cache و`$HOME/.config/<PROGRAM_NAME>` للـ config.
الهدف إن الـ home يفضل نضيف، وأعتقد كفاية نغيّر الـ variables/constants بتاعة الـ storage path.
