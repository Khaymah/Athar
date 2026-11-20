package com.khaymah.athar

import android.annotation.SuppressLint
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import androidx.core.net.toUri
import android.os.Build
import android.os.PowerManager
import android.provider.Settings

object Reliability {
    fun isBatteryExempt(context: Context): Boolean =
        context.getSystemService(PowerManager::class.java).isIgnoringBatteryOptimizations(context.packageName)

    @SuppressLint("BatteryLife")
    fun requestBatteryExemption(context: Context) {
        val direct = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, "package:${context.packageName}".toUri())
        if (!launch(context, direct)) launch(context, Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))
    }

    fun openAutostartSettings(context: Context) {
        val opened = autostartScreens.any { launch(context, Intent().setComponent(it)) }
        if (!opened) {
            launch(context, Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, "package:${context.packageName}".toUri()))
        }
    }

    fun autostartHint(): String = when (Build.MANUFACTURER.lowercase()) {
        "xiaomi", "redmi", "poco" ->
            "الإعدادات ← التطبيقات ← أثر: فعّل «التشغيل التلقائي»، وخلّي «توفير البطارية» على «بلا قيود»."
        "huawei", "honor" ->
            "الإعدادات ← البطارية ← تشغيل التطبيقات ← أثر: اختار «إدارة يدوية» وفعّل الاختيارات الثلاثة."
        "oppo", "realme", "oneplus" ->
            "الإعدادات ← التطبيقات ← أثر ← استخدام البطارية: فعّل «السماح بالنشاط في الخلفية» و«التشغيل التلقائي»."
        "vivo", "iqoo" ->
            "الإعدادات ← البطارية ← استهلاك الطاقة في الخلفية ← أثر: اختار «السماح»، وفعّل التشغيل التلقائي."
        "samsung" ->
            "الإعدادات ← البطارية ← حدود الاستخدام في الخلفية ← التطبيقات غير النائمة أبداً: أضف أثر."
        else ->
            "الإعدادات ← التطبيقات ← أثر ← البطارية: اختار «بلا قيود»."
    } + " وكمان اقفل التطبيق في قائمة التطبيقات الأخيرة (علامة القفل) عشان مايتقفلش لما تمسح الذاكرة."

    private fun launch(context: Context, intent: Intent): Boolean = try {
        context.startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        true
    } catch (e: Exception) {
        false
    }

    private val autostartScreens = listOf(
        ComponentName("com.miui.securitycenter", "com.miui.permcenter.autostart.AutoStartManagementActivity"),
        ComponentName("com.huawei.systemmanager", "com.huawei.systemmanager.startupmgr.ui.StartupNormalAppListActivity"),
        ComponentName("com.huawei.systemmanager", "com.huawei.systemmanager.optimize.process.ProtectActivity"),
        ComponentName("com.hihonor.systemmanager", "com.hihonor.systemmanager.startupmgr.ui.StartupNormalAppListActivity"),
        ComponentName("com.coloros.safecenter", "com.coloros.safecenter.permission.startup.StartupAppListActivity"),
        ComponentName("com.coloros.safecenter", "com.coloros.safecenter.startupapp.StartupAppListActivity"),
        ComponentName("com.oppo.safe", "com.oppo.safe.permission.startup.StartupAppListActivity"),
        ComponentName("com.vivo.permissionmanager", "com.vivo.permissionmanager.activity.BgStartUpManagerActivity"),
        ComponentName("com.iqoo.secure", "com.iqoo.secure.ui.phoneoptimize.BgStartUpManager"),
        ComponentName("com.samsung.android.lool", "com.samsung.android.sm.ui.battery.BatteryActivity"),
        ComponentName("com.asus.mobilemanager", "com.asus.mobilemanager.entry.FunctionActivity"),
        ComponentName("com.letv.android.letvsafe", "com.letv.android.letvsafe.AutobootManageActivity"),
    )
}
