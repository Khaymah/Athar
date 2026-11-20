#!/usr/bin/env bash
set -euo pipefail

PKG=com.khaymah.athar
APK=app/build/outputs/apk/debug/app-debug.apk

count() {
  adb logcat -d -s Athar:I | grep -c "played" || true
}

adb install -r "$APK"
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS
adb shell am start -n "$PKG/.MainActivity" --ez autostart true
sleep 15

if adb shell dumpsys notification --noredact | grep -q "تحديث أثر متاح"; then
  echo "update check passed: newer release detected"
else
  echo "::warning::update notification not found (GitHub API unreachable or rate limited?)"
fi

adb shell input keyevent KEYCODE_HOME
adb shell input keyevent KEYCODE_SLEEP
adb shell dumpsys battery unplug
adb shell dumpsys deviceidle enable deep
adb shell dumpsys deviceidle force-idle
idle=$(adb shell dumpsys deviceidle get deep | tr -d '\r')
echo "deep idle state: $idle"
[ "$idle" = "IDLE" ]

first=$(count)
sleep 30
second=$(count)
echo "count while idle: $first -> $second"

services=$(adb shell dumpsys activity services "$PKG")
grep -q "isForeground=true" <<<"$services"
[ "$second" -gt "$first" ]
[ $((second - first)) -ge 4 ]
echo "doze check passed"

adb shell dumpsys deviceidle unforce
adb root >/dev/null
adb wait-for-device
pid=$(adb shell pidof "$PKG" | tr -d '\r')
adb shell kill -9 "$pid"
before=$(count)
now=$before
for _ in $(seq 1 30); do
  sleep 5
  now=$(count)
  [ "$now" -gt "$before" ] && break
done
echo "count after process kill: $before -> $now"
[ "$now" -gt "$before" ]
echo "smoke test passed"
