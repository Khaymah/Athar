package com.khaymah.athar

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import androidx.core.app.NotificationCompat

object ZikrNotifications {
    const val SERVICE_ID = 1
    private const val RESUME_ID = 2
    private const val CHANNEL_SERVICE = "zikr"
    private const val CHANNEL_RESUME = "resume"

    fun ensureChannels(context: Context) {
        val manager = context.getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(
            NotificationChannel(CHANNEL_SERVICE, "التسبيح الجاري", NotificationManager.IMPORTANCE_LOW).apply {
                setShowBadge(false)
                setSound(null, null)
            },
        )
        manager.createNotificationChannel(
            NotificationChannel(CHANNEL_RESUME, "استئناف بعد إعادة التشغيل", NotificationManager.IMPORTANCE_DEFAULT),
        )
    }

    fun service(context: Context, phrase: Phrase?, paused: Boolean): Notification {
        val title = when {
            paused -> "متوقف مؤقتاً"
            phrase != null -> phrase.text
            else -> "أثر يعمل"
        }
        val toggle = if (paused) {
            action(context, "استئناف", ZikrService.ACTION_START, 1)
        } else {
            action(context, "إيقاف مؤقت", ZikrService.ACTION_PAUSE, 2)
        }
        return NotificationCompat.Builder(context, CHANNEL_SERVICE)
            .setSmallIcon(R.drawable.ic_stat_zikr)
            .setContentTitle(title)
            .setContentIntent(openApp(context, autostart = false))
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setSilent(true)
            .setCategory(NotificationCompat.CATEGORY_SERVICE)
            .setForegroundServiceBehavior(NotificationCompat.FOREGROUND_SERVICE_IMMEDIATE)
            .addAction(toggle)
            .addAction(action(context, "إيقاف", ZikrService.ACTION_STOP, 3))
            .build()
    }

    fun showResume(context: Context) {
        ensureChannels(context)
        val manager = context.getSystemService(NotificationManager::class.java)
        if (!manager.areNotificationsEnabled()) return
        val notification = NotificationCompat.Builder(context, CHANNEL_RESUME)
            .setSmallIcon(R.drawable.ic_stat_zikr)
            .setContentTitle("أثر")
            .setContentText("اضغط لاستئناف التسبيح")
            .setContentIntent(openApp(context, autostart = true))
            .setAutoCancel(true)
            .build()
        manager.notify(RESUME_ID, notification)
    }

    fun cancelResume(context: Context) {
        context.getSystemService(NotificationManager::class.java).cancel(RESUME_ID)
    }

    private fun action(context: Context, title: String, action: String, requestCode: Int) =
        NotificationCompat.Action(
            0,
            title,
            PendingIntent.getService(
                context,
                requestCode,
                ZikrService.intent(context, action),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            ),
        )

    private fun openApp(context: Context, autostart: Boolean): PendingIntent =
        PendingIntent.getActivity(
            context,
            if (autostart) 11 else 10,
            Intent(context, MainActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                .putExtra(MainActivity.EXTRA_AUTOSTART, autostart),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
        )
}
