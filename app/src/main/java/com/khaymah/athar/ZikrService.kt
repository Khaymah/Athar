package com.khaymah.athar

import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.IBinder
import android.os.PowerManager
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
    private var lastStats: ZikrStats? = null

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
        mutableState.value = mutableState.value.copy(status = PlaybackStatus.Paused)
        notifyState()
        scope.launch { repository.setRunning(false) }
    }

    private fun stop() {
        loop?.cancel()
        loop = null
        audio.stopCurrent()
        releaseWakeLock()
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
            lastStats = repository.increment()
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
        stats = lastStats,
        paused = mutableState.value.status == PlaybackStatus.Paused,
    )

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

        private val mutableState = MutableStateFlow(PlaybackState())
        val state: StateFlow<PlaybackState> = mutableState.asStateFlow()

        fun intent(context: Context, action: String): Intent =
            Intent(context, ZikrService::class.java).setAction(action)

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
