package com.khaymah.athar

import android.app.AlarmManager
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import android.os.SystemClock
import android.util.Log
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

enum class PlaybackStatus { Stopped, Playing, Paused }

data class PlaybackState(val status: PlaybackStatus = PlaybackStatus.Stopped, val currentId: String? = null)

class ZikrService : Service() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate + CoroutineExceptionHandler { _, _ -> })
    private lateinit var repository: ZikrRepository
    private lateinit var audio: ZikrAudio
    private var loop: Job? = null
    private var stopping: Job? = null
    private var wakeLock: PowerManager.WakeLock? = null
    private var lastPhrase: Phrase? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        repository = ZikrRepository(this)
        audio = ZikrAudio(this)
        ZikrNotifications.ensureChannels(this)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_PAUSE -> pause()
            ACTION_STOP -> {
                stop()
                return START_NOT_STICKY
            }
            ACTION_START -> start()
            else -> scope.launch { if (repository.wasRunning.first()) start() else stopSelf() }
        }
        return START_STICKY
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        if (mutableState.value.status == PlaybackStatus.Playing) scheduleWatchdog(TASK_REMOVED_RESTART_MS)
        super.onTaskRemoved(rootIntent)
    }

    override fun onDestroy() {
        loop?.cancel()
        releaseWakeLock()
        audio.release()
        scope.cancel()
        mutableState.value = PlaybackState()
        super.onDestroy()
    }

    private fun start() {
        stopping?.cancel()
        stopping = null
        if (!promoteToForeground()) return
        ZikrNotifications.cancelResume(this)
        acquireWakeLock()
        scheduleWatchdog(WATCHDOG_MS)
        if (loop?.isActive != true) loop = scope.launch { runLoop() }
        scope.launch { repository.setRunning(true) }
    }

    private fun pause() {
        if (loop == null) {
            stopSelf()
            return
        }
        loop?.cancel()
        loop = null
        audio.stopCurrent()
        releaseWakeLock()
        cancelWatchdog()
        mutableState.value = mutableState.value.copy(status = PlaybackStatus.Paused)
        notifyState()
        scope.launch { repository.setRunning(false) }
    }

    private fun stop() {
        loop?.cancel()
        loop = null
        audio.stopCurrent()
        releaseWakeLock()
        cancelWatchdog()
        mutableState.value = PlaybackState()
        stopping = scope.launch {
            repository.setRunning(false)
            ServiceCompat.stopForeground(this@ZikrService, ServiceCompat.STOP_FOREGROUND_REMOVE)
            stopSelf()
        }
    }

    private suspend fun runLoop() {
        mutableState.value = mutableState.value.copy(status = PlaybackStatus.Playing)
        notifyState()
        audio.awaitLoaded()
        while (scope.isActive) {
            try {
                tick()
            } catch (e: CancellationException) {
                throw e
            } catch (e: Exception) {
                audio.abandonFocus()
                delay(RETRY_DELAY_MS)
            }
        }
    }

    private var index = 0

    private suspend fun tick() {
        val settings = repository.settings.first()
        val intervalMs = settings.intervalSeconds * 1_000L
        val phrases = settings.activePhrases
        if (phrases.isEmpty()) {
            delay(intervalMs)
            return
        }
        val phrase = if (settings.shuffle) pickRandom(phrases) else phrases[index++ % phrases.size]
        val clipMs = audio.durationMs(phrase)
        if (audio.play(phrase, settings.volume)) {
            lastPhrase = phrase
            mutableState.value = PlaybackState(PlaybackStatus.Playing, phrase.id)
            Log.i(LOG_TAG, "played ${phrase.id}")
            notifyState()
        }
        delay(clipMs)
        audio.abandonFocus()
        delay((intervalMs - clipMs).coerceAtLeast(MIN_GAP_MS))
    }

    private fun pickRandom(phrases: List<Phrase>): Phrase {
        val candidates = if (phrases.size > 1) phrases.filter { it != lastPhrase } else phrases
        return candidates.random()
    }

    private fun promoteToForeground(): Boolean = try {
        ServiceCompat.startForeground(
            this,
            ZikrNotifications.SERVICE_ID,
            buildNotification(),
            ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK,
        )
        true
    } catch (e: Exception) {
        ZikrNotifications.showResume(this)
        stopSelf()
        false
    }

    private fun notifyState() {
        getSystemService(NotificationManager::class.java)
            .notify(ZikrNotifications.SERVICE_ID, buildNotification())
    }

    private fun buildNotification() = ZikrNotifications.service(
        context = this,
        phrase = lastPhrase,
        paused = mutableState.value.status == PlaybackStatus.Paused,
    )

    private fun scheduleWatchdog(delayMs: Long) {
        val alarms = getSystemService(AlarmManager::class.java)
        val at = SystemClock.elapsedRealtime() + delayMs
        val exact = Build.VERSION.SDK_INT < Build.VERSION_CODES.S || alarms.canScheduleExactAlarms()
        if (exact) {
            alarms.setExactAndAllowWhileIdle(AlarmManager.ELAPSED_REALTIME_WAKEUP, at, watchdogIntent(this))
        } else {
            alarms.setAndAllowWhileIdle(AlarmManager.ELAPSED_REALTIME_WAKEUP, at, watchdogIntent(this))
        }
    }

    private fun cancelWatchdog() {
        getSystemService(AlarmManager::class.java).cancel(watchdogIntent(this))
    }

    private fun acquireWakeLock() {
        if (wakeLock?.isHeld == true) return
        wakeLock = getSystemService(PowerManager::class.java)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "athar:zikr")
            .apply {
                setReferenceCounted(false)
                acquire()
            }
    }

    private fun releaseWakeLock() {
        wakeLock?.takeIf { it.isHeld }?.release()
        wakeLock = null
    }

    companion object {
        const val ACTION_START = "com.khaymah.athar.START"
        const val ACTION_PAUSE = "com.khaymah.athar.PAUSE"
        const val ACTION_STOP = "com.khaymah.athar.STOP"
        private const val MIN_GAP_MS = 500L
        private const val RETRY_DELAY_MS = 5_000L
        private const val WATCHDOG_MS = 60_000L
        private const val TASK_REMOVED_RESTART_MS = 1_000L
        private const val LOG_TAG = "Athar"

        private val mutableState = MutableStateFlow(PlaybackState())
        val state: StateFlow<PlaybackState> = mutableState.asStateFlow()

        fun intent(context: Context, action: String): Intent =
            Intent(context, ZikrService::class.java).setAction(action)

        private fun watchdogIntent(context: Context): PendingIntent =
            PendingIntent.getForegroundService(
                context,
                20,
                intent(context, ACTION_START),
                PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT,
            )

        fun start(context: Context) {
            ContextCompat.startForegroundService(context, intent(context, ACTION_START))
        }

        fun pause(context: Context) {
            context.startService(intent(context, ACTION_PAUSE))
        }

        fun stop(context: Context) {
            context.startService(intent(context, ACTION_STOP))
        }
    }
}
