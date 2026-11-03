pylint كيصاوب واحد الدوسي ديال data سميتو `.pylint.d` نيشان فـ الـ home ديال الـ user.
بغيتو يحترم XDG Base Directory Specification.
حسب la spec، الـ data خاصها تمشي لـ `$HOME/.local/share/<PROGRAM_NAME>`، و la spec فيها حتى `$HOME/.cache/<PROGRAM_NAME>` لـ cache و `$HOME/.config/<PROGRAM_NAME>` لـ config.
الهدف هو الـ home يبقى نقي، وكنظن غير تبدل les variables/constantes ديال الـ path فين كيتخزن هادشي يكفي.
