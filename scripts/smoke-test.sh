#!/usr/bin/env bash
set -euo pipefail

PKG=com.khaymah.athar
APK=app/build/outputs/apk/debug/app-debug.apk

count() {
  adb shell dumpsys notification --noredact | grep -o 'اليوم [0-9]*' | head -1 | grep -o '[0-9]*' || echo 0
}

adb install -r "$APK"
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS
adb shell am start -n "$PKG/.MainActivity" --ez autostart true
sleep 15

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
echo "smoke test passed"
