# تطبيق التسبيح (athkar-app): الخطة

> البرانش: `athkar-app` (orphan) جوه `khaymah/athar` · التوزيع: APK على GitHub Releases · الاستخدام: شخصي

## القرارات

| البند | القرار | السبب |
|------|--------|-------|
| Platform | Android بس | iOS من غير متجر مش عملي |
| اللغة | Kotlin native + Jetpack Compose | الـ foreground service أوثق، والـ APK حوالي 3MB، وPlay Protect بيعلّم عليه أقل |
| SDK | `minSdk 26` · `targetSdk 36` | Play Protect بيحذّر من الـ targetSdk القديم |
| التخزين | Jetpack DataStore | الإعدادات والعدّاد بس، من غير DB |
| الصوت | ملفات `.ogg` مدمجة، وكل عبارة ليها ملف | offline، ومصادرها متسجّلة في `SOURCES.md` |
| البناء | GitHub Actions، وكل tag `v*` يطلّع APK موقّع على Releases | من غير متجر |

## ضد القتل من النظام
1. `ForegroundService` نوعه `mediaPlayback`، مع notification ثابتة فيها (إيقاف مؤقت · إيقاف · العدّاد).
2. `PARTIAL_WAKE_LOCK` طول ما الخدمة شغالة.
3. طلب إعفاء من battery optimization أول مرة (`ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`).
4. شاشة إرشاد بتفتح إعدادات الـ Autostart حسب نوع الموبايل (Xiaomi · Oppo · Vivo · Huawei · Samsung).
5. `START_STICKY`، مع إعادة جدولة لو النظام قتل الخدمة.
6. التشغيل بـ `SoundPool` (الكليبات قصيرة، والـ latency شبه صفر)، مع audio focus من نوع `TRANSIENT_MAY_DUCK` عشان الذكر يوطّي صوت الموسيقى بدل ما يوقّفها.

> ⚠️ على Android 15+ ممنوع تبدأ خدمة `mediaPlayback` من `BOOT_COMPLETED`. يعني بعد restart المستخدم يفتح التطبيق مرة. الحل: notification عادية بعد الـ boot فيها زرار "ابدأ".

## ضد حظر Play Protect
- توقيع ثابت بـ release keystore متخزّن في GH Secrets، ومن غيره التحديثات مش هتتثبّت فوق القديم.
- Permissions بالحد الأدنى: `FOREGROUND_SERVICE` · `FOREGROUND_SERVICE_MEDIA_PLAYBACK` · `POST_NOTIFICATIONS` · `WAKE_LOCK` · `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` · `RECEIVE_BOOT_COMPLETED`.
- من غير Internet permission، ولا analytics، ولا Accessibility، ولا Overlay.

## الإعدادات (قابلة للتعديل)
- الـ interval: slider من 3 لـ 60 ثانية (الافتراضي 5).
- العبارات: تفعيل وإلغاء، والترتيب بأزرار ▲▼ بدل السحب.
- الترتيب: تسلسلي (الافتراضي) أو عشوائي.
- مستوى الصوت مستقل عن صوت الميديا.
- عدّاد يومي وإجمالي لكل العبارات مع بعض (مش لكل عبارة لوحدها).

## العبارات الافتراضية
سبحان الله · الحمد لله · لا إله إلا الله · الله أكبر · أستغفر الله · سبحان الله وبحمده · سبحان الله العظيم · لا حول ولا قوة إلا بالله · اللهم صلِّ على محمد

## الصوت
- **المرحلة 1:** كليبات gTTS أولّدها أنا (اتجرّبت وشغالة)، وبنظّفها بـ ffmpeg (قص السكوت + normalize، والتصدير ogg/opus).
- **قابلة للاستبدال:** تحط أي ملف بنفس الاسم في `app/src/main/res/raw/` وتعمل tag جديد.
- `SOURCES.md` فيه مصدر كل ملف.

## الملفات
```
.github/workflows/release.yml
app/build.gradle.kts · settings.gradle.kts · gradle/libs.versions.toml
app/src/main/AndroidManifest.xml
app/src/main/java/.../MainActivity.kt         شاشة التشغيل والعدّاد
app/src/main/java/.../SettingsScreen.kt
app/src/main/java/.../ZikrService.kt          foreground + ticker + SoundPool
app/src/main/java/.../ZikrRepository.kt       DataStore
app/src/main/java/.../Phrases.kt
app/src/main/java/.../BootReceiver.kt
app/src/main/java/.../KillerGuide.kt          إرشاد الـ OEM
app/src/main/res/raw/*.ogg
README.md · SOURCES.md
```

## خطوة مرة واحدة عندك (التوقيع)
توليد keystore، وإضافة 4 secrets: `KEYSTORE_BASE64` · `KEYSTORE_PASSWORD` · `KEY_ALIAS` · `KEY_PASSWORD`. هبعتلك الأوامر جاهزة.

## المهام
- [x] إنشاء البرانش orphan `athkar-app` + Gradle skeleton
- [x] Phrases + ZikrRepository (DataStore)
- [x] ZikrService + notification + wake lock + audio focus
- [x] UI: الرئيسية + الإعدادات (RTL عربي)
- [x] battery exemption + KillerGuide + BootReceiver
- [x] توليد وتنظيف الصوت + SOURCES.md
- [x] android.yml + README (التثبيت والتوقيع)
- [ ] أول run على CI: smoke test على emulator (الشاشة مقفولة + Doze) + build
