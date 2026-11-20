# أثر

تطبيق Android بيشغّل ذكر صوتي كل كام ثانية (الافتراضي 5) بالترتيب أو عشوائي، وبيفضل شغّال والشاشة مقفولة. شغّال offline بالكامل ومن غير Internet permission.

## التثبيت
1. من صفحة **Releases** نزّل `athar-vX.Y.Z.apk`.
2. افتحه من الموبايل، ووافق على «التثبيت من مصادر غير معروفة» للمتصفح أو مدير الملفات.
3. لو Play Protect قال «تطبيق غير معروف»، اختار **التفاصيل ← التثبيت على أي حال**. ده تحذير عادي لأي APK من برّه المتجر.
4. أول تشغيل: وافق على الإشعارات، واضغط **«اسمح بالعمل بدون قيود»**، ونفّذ إرشاد الـ Autostart اللي ظاهر على الشاشة.

## إزاي بيفضل شغّال
| الحماية | الطريقة |
|---------|---------|
| النظام مايقتلوش | Foreground service نوعه `mediaPlayback` مع notification ثابتة |
| الشاشة مقفولة أو Doze | `PARTIAL_WAKE_LOCK` + إعفاء من battery optimization |
| شركات زي Xiaomi وOppo وHuawei | شاشة إرشاد بتفتح إعدادات الـ Autostart مباشرة |
| النظام قتله برضه | `START_STICKY` بيرجّعه تاني |
| بعد restart الموبايل | Android 14 وأقدم: بيكمّل لوحده. Android 15 وأحدث: notification «اضغط لاستئناف»، لأن النظام بيمنع تشغيل الصوت تلقائياً بعد الـ boot |
| مكالمة | بيسكت لوحده لحد ما المكالمة تخلص |
| موسيقى شغّالة | بيوطّي صوتها لحظة الذكر بدل ما يوقّفها |

الـ CI بيختبر ده على emulator: بيقفل الشاشة، ويدخّل الجهاز Doze بالعافية، ويتأكد إن العدّاد لسه بيزيد.

## تغيير الأصوات
كل عبارة ليها ملف في `app/src/main/res/raw/`:

| الملف | العبارة |
|-------|---------|
| `subhanallah.ogg` | سبحان الله |
| `alhamdulillah.ogg` | الحمد لله |
| `lailaha_illallah.ogg` | لا إله إلا الله |
| `allahu_akbar.ogg` | الله أكبر |
| `astaghfirullah.ogg` | أستغفر الله |
| `subhanallah_wabihamdih.ogg` | سبحان الله وبحمده |
| `subhanallah_alazim.ogg` | سبحان الله العظيم |
| `hawqala.ogg` | لا حول ولا قوة إلا بالله |
| `salawat.ogg` | اللهم صلِّ على محمد |

استبدل الملف بنفس الاسم وحدّث `SOURCES.md`. التحويل من أي صيغة:

```bash
ffmpeg -i input.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5" -ar 44100 -ac 1 -c:a libvorbis -q:a 5 subhanallah.ogg
```

## إصدار نسخة جديدة
```bash
git tag v0.1.0
```
```bash
git push origin v0.1.0
```
الـ workflow بيشغّل الاختبارات والـ emulator، وبعدها بيبني APK موقّع وبيرفعه على Releases.

## التوقيع (مرة واحدة)
النسخ الجديدة مش هتتثبّت فوق القديمة غير لو كلها متوقّعة بنفس المفتاح، فاحتفظ بنسخة احتياطي من الـ keystore.

```bash
keytool -genkeypair -v -keystore athar.jks -alias athar -keyalg RSA -keysize 4096 -validity 36500
```
```bash
base64 -w0 athar.jks > athar.jks.b64
```

في **Settings ← Secrets and variables ← Actions** ضيف:

| Secret | القيمة |
|--------|--------|
| `KEYSTORE_BASE64` | محتوى `athar.jks.b64` |
| `KEYSTORE_PASSWORD` | باسورد الـ keystore |
| `KEY_ALIAS` | `athar` |
| `KEY_PASSWORD` | باسورد المفتاح |

من غير الـ secrets دي، أي push بيطلّع debug APK كـ artifact بس، والـ tag بيفشل عن قصد.

## البناء محلياً
محتاج JDK 17+ وAndroid SDK 36:

```bash
./gradlew testDebugUnitTest assembleDebug
```
