# مصادر الأصوات

الاستخدام شخصي وغير تجاري.

| الملف | المصدر | ملاحظات |
|-------|--------|---------|
| ملفات `app/src/main/res/raw/*.ogg` من غير بادئة (من v0.3.0) | صوت Sabry Dawood: تسجيلات بعتها المالك (9 عبارات) | معالجة «دافي»: إزالة الضوضاء + EQ دافي (بيزوّد الباص)، وبعدها اتشال السكوت من الأول والآخر، ومستوى الصوت اتظبط (`loudnorm -16 LUFS`)، والتحويل لـ Ogg Vorbis 44.1kHz mono |
| (v0.1.0 لحد v0.2.0) | Google Translate TTS عن طريق [gTTS](https://github.com/pndurette/gTTS) | اتستبدلت بالتسجيلات |
| `app/src/main/res/raw/hummada_*.ogg` (من v0.5.0) | تسجيلات Mohammad Alhummada بعتها المالك (8 عبارات، مفيش «لا حول ولا قوة إلا بالله») | اتشال السكوت من الأول والآخر، ومستوى الصوت اتظبط (`loudnorm -16 LUFS`)، والتحويل لـ Ogg Vorbis 44.1kHz mono، من غير EQ |

## مصادر اتفحصت واترفضت
| المصدر | سبب الرفض |
|--------|-----------|
| [1O1x/Azkar](https://github.com/1O1x/Azkar) | مقطع واحد مدته 148 ثانية، متصل من غير فواصل بين العبارات |
| [akaban01/azkar-web](https://github.com/akaban01/azkar-web) | أذكار طويلة (صباح ومساء)، والتسجيلات من غير رخصة |
| [archive.org](https://archive.org/details/keagunganzikirini) و [archive.org](https://archive.org/download/SubhanallahWalhamdulillah) | أناشيد ومحاضرات طويلة، مفيش فيهم عبارات قصيرة منفصلة |
| [Wikimedia Commons: Category:Zikr](https://commons.wikimedia.org/wiki/Category:Zikr) | فيه صور بس، مفيش تسجيلات صوتية |

لما تستبدل ملف، ضيف سطر هنا بالمصدر الجديد.
