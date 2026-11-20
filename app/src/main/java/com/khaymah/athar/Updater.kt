package com.khaymah.athar

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import android.os.Build
import android.provider.Settings
import androidx.core.app.NotificationCompat
import androidx.core.net.toUri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

data class AppRelease(val tag: String, val apkUrl: String)

enum class UpdateStatus { Idle, Downloading, WaitingForUser, Failed }

object Updater {
    private const val LATEST_URL = "https://api.github.com/repos/Khaymah/Athar/releases/latest"
    private const val CHANNEL = "updates"
    private const val NOTIFICATION_ID = 3
    private const val CHECK_EVERY_MS = 24 * 60 * 60 * 1000L
    private const val PREFS = "updater"
    private const val KEY_LAST_CHECK = "last_check"
    private const val KEY_LAST_ATTEMPT = "last_attempt"
    private const val RETRY_AFTER_MS = 15 * 60 * 1000L
    private const val KEY_NOTIFIED = "notified_tag"
    private const val TIMEOUT_MS = 15_000

    private val mutableAvailable = MutableStateFlow<AppRelease?>(null)
    val available: StateFlow<AppRelease?> = mutableAvailable.asStateFlow()

    private val mutableStatus = MutableStateFlow(UpdateStatus.Idle)
    val status: StateFlow<UpdateStatus> = mutableStatus.asStateFlow()

    suspend fun check(context: Context, force: Boolean = false): AppRelease? {
        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val now = System.currentTimeMillis()
        if (!force && now - prefs.getLong(KEY_LAST_CHECK, 0) < CHECK_EVERY_MS) return mutableAvailable.value
        if (!force && now - prefs.getLong(KEY_LAST_ATTEMPT, 0) < RETRY_AFTER_MS) return mutableAvailable.value
        prefs.edit().putLong(KEY_LAST_ATTEMPT, now).apply()
        val latest = runCatching { fetchLatest() }.getOrNull() ?: return mutableAvailable.value
        prefs.edit().putLong(KEY_LAST_CHECK, now).apply()
        val newer = latest.takeIf { isNewer(it.tag, currentVersion(context)) }
        mutableAvailable.value = newer
        if (newer != null && prefs.getString(KEY_NOTIFIED, null) != newer.tag && notify(context, newer)) {
            prefs.edit().putString(KEY_NOTIFIED, newer.tag).apply()
        }
        return newer
    }

    suspend fun install(context: Context) {
        val release = mutableAvailable.value ?: check(context, force = true) ?: return
        if (!context.packageManager.canRequestPackageInstalls()) {
            context.startActivity(
                Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, "package:${context.packageName}".toUri())
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
            )
            return
        }
        val previous = mutableStatus.value
        if (previous == UpdateStatus.Downloading || !mutableStatus.compareAndSet(previous, UpdateStatus.Downloading)) return
        val ok = runCatching { downloadAndCommit(context, release) }.isSuccess
        mutableStatus.value = if (ok) UpdateStatus.WaitingForUser else UpdateStatus.Failed
    }

    fun isNewer(remote: String, current: String): Boolean {
        val r = parts(remote)
        val c = parts(current)
        for (i in 0 until maxOf(r.size, c.size)) {
            val a = r.getOrElse(i) { 0 }
            val b = c.getOrElse(i) { 0 }
            if (a != b) return a > b
        }
        return false
    }

    internal fun parseRelease(json: String): AppRelease? {
        val root = JSONObject(json)
        val tag = root.optString("tag_name").takeIf { it.isNotBlank() } ?: return null
        val assets = root.optJSONArray("assets") ?: return null
        for (i in 0 until assets.length()) {
            val asset = assets.getJSONObject(i)
            val name = asset.optString("name")
            if (name.endsWith(".apk") && !name.contains("debug")) {
                return AppRelease(tag, asset.getString("browser_download_url"))
            }
        }
        return null
    }

    private fun parts(version: String): List<Int> =
        version.trim().removePrefix("v").substringBefore('-').split('.').map { it.toIntOrNull() ?: 0 }

    private fun currentVersion(context: Context): String =
        context.packageManager.getPackageInfo(context.packageName, 0).versionName ?: "0"

    private suspend fun fetchLatest(): AppRelease? = withContext(Dispatchers.IO) {
        val connection = open(LATEST_URL).apply { setRequestProperty("Accept", "application/vnd.github+json") }
        try {
            if (connection.responseCode != HttpURLConnection.HTTP_OK) return@withContext null
            parseRelease(connection.inputStream.bufferedReader().use { it.readText() })
        } finally {
            connection.disconnect()
        }
    }

    private suspend fun downloadAndCommit(context: Context, release: AppRelease) = withContext(Dispatchers.IO) {
        val installer = context.packageManager.packageInstaller
        val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL).apply {
            setAppPackageName(context.packageName)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                setRequireUserAction(PackageInstaller.SessionParams.USER_ACTION_NOT_REQUIRED)
            }
        }
        val sessionId = installer.createSession(params)
        val session = installer.openSession(sessionId)
        try {
            val connection = open(release.apkUrl)
            try {
                check(connection.responseCode == HttpURLConnection.HTTP_OK)
                connection.inputStream.use { input ->
                    session.openWrite("athar.apk", 0, connection.contentLengthLong).use { output ->
                        input.copyTo(output)
                        session.fsync(output)
                    }
                }
            } finally {
                connection.disconnect()
            }
            val callback = PendingIntent.getBroadcast(
                context,
                sessionId,
                Intent(context, InstallResultReceiver::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_MUTABLE,
            )
            session.commit(callback.intentSender)
        } catch (e: Exception) {
            session.abandon()
            throw e
        } finally {
            session.close()
        }
    }

    private fun open(url: String): HttpURLConnection =
        (URL(url).openConnection() as HttpURLConnection).apply {
            connectTimeout = TIMEOUT_MS
            readTimeout = TIMEOUT_MS
            instanceFollowRedirects = true
        }

    private fun notify(context: Context, release: AppRelease): Boolean {
        val manager = updatesChannel(context)
        if (!manager.areNotificationsEnabled()) return false
        val open = PendingIntent.getActivity(
            context,
            20,
            Intent(context, MainActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                .putExtra(MainActivity.EXTRA_INSTALL_UPDATE, true),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
        )
        val notification = NotificationCompat.Builder(context, CHANNEL)
            .setSmallIcon(R.drawable.ic_stat_zikr)
            .setContentTitle("تحديث أثر متاح: ${release.tag}")
            .setContentText("اضغط للتحديث")
            .setContentIntent(open)
            .setAutoCancel(true)
            .build()
        manager.notify(NOTIFICATION_ID, notification)
        return true
    }

    internal fun onInstallResult(context: Context, intent: Intent) {
        when (intent.getIntExtra(PackageInstaller.EXTRA_STATUS, PackageInstaller.STATUS_FAILURE)) {
            PackageInstaller.STATUS_PENDING_USER_ACTION -> {
                val confirm = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    intent.getParcelableExtra(Intent.EXTRA_INTENT, Intent::class.java)
                } else {
                    @Suppress("DEPRECATION")
                    intent.getParcelableExtra(Intent.EXTRA_INTENT)
                }
                val intentToConfirm = confirm ?: return
                val launched = runCatching {
                    context.startActivity(intentToConfirm.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                }.isSuccess
                if (!launched) notifyConfirm(context, intentToConfirm)
            }
            PackageInstaller.STATUS_SUCCESS, PackageInstaller.STATUS_FAILURE_ABORTED -> mutableStatus.value = UpdateStatus.Idle
            else -> mutableStatus.value = UpdateStatus.Failed
        }
    }

    private fun updatesChannel(context: Context): NotificationManager {
        val manager = context.getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(
            NotificationChannel(CHANNEL, "التحديثات", NotificationManager.IMPORTANCE_DEFAULT),
        )
        return manager
    }

    private fun notifyConfirm(context: Context, confirm: Intent) {
        val manager = updatesChannel(context)
        if (!manager.areNotificationsEnabled()) return
        val pending = PendingIntent.getActivity(
            context,
            21,
            confirm,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
        )
        val notification = NotificationCompat.Builder(context, CHANNEL)
            .setSmallIcon(R.drawable.ic_stat_zikr)
            .setContentTitle("التحديث جاهز")
            .setContentText("اضغط لتأكيد التثبيت")
            .setContentIntent(pending)
            .setAutoCancel(true)
            .build()
        manager.notify(4, notification)
    }
}

class InstallResultReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        Updater.onInstallResult(context, intent)
    }
}
