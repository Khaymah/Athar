package com.khaymah.athar

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.media.MediaMetadataRetriever
import android.media.SoundPool
import androidx.annotation.RawRes
import kotlinx.coroutines.CompletableDeferred

class ZikrAudio(context: Context) {
    private val appContext = context.applicationContext
    private val audioManager = appContext.getSystemService(AudioManager::class.java)

    private val attributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
        .build()

    private val focusRequest = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK)
        .setAudioAttributes(attributes)
        .build()

    private val pool = SoundPool.Builder()
        .setMaxStreams(2)
        .setAudioAttributes(attributes)
        .build()

    private val allSounds = Voices.all.flatMap { voice -> Phrases.all.map(voice::soundFor) }.distinct()
    private val soundIds = mutableMapOf<Int, Int>()
    private val durations = mutableMapOf<Int, Long>()
    private val loaded = CompletableDeferred<Unit>()
    private var pending = allSounds.size
    private var currentStream = 0

    init {
        pool.setOnLoadCompleteListener { _, _, _ ->
            pending--
            if (pending == 0) loaded.complete(Unit)
        }
        allSounds.forEach { sound ->
            soundIds[sound] = pool.load(appContext, sound, 1)
            durations[sound] = measure(sound)
        }
    }

    suspend fun awaitLoaded() = loaded.await()

    fun durationMs(@RawRes sound: Int): Long = durations[sound] ?: DEFAULT_DURATION_MS

    fun play(@RawRes sound: Int, volume: Float): Boolean {
        if (isInCall()) return false
        val id = soundIds[sound] ?: return false
        if (audioManager.requestAudioFocus(focusRequest) != AudioManager.AUDIOFOCUS_REQUEST_GRANTED) return false
        currentStream = pool.play(id, volume, volume, 1, 0, 1f)
        return currentStream != 0
    }

    fun abandonFocus() {
        audioManager.abandonAudioFocusRequest(focusRequest)
    }

    fun stopCurrent() {
        if (currentStream != 0) pool.stop(currentStream)
        currentStream = 0
        abandonFocus()
    }

    fun release() {
        abandonFocus()
        pool.release()
    }

    private fun isInCall(): Boolean = when (audioManager.mode) {
        AudioManager.MODE_IN_CALL, AudioManager.MODE_IN_COMMUNICATION, AudioManager.MODE_RINGTONE -> true
        else -> false
    }

    private fun measure(@RawRes res: Int): Long = runCatching {
        appContext.resources.openRawResourceFd(res).use { fd ->
            val retriever = MediaMetadataRetriever()
            try {
                retriever.setDataSource(fd.fileDescriptor, fd.startOffset, fd.length)
                retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull()
            } finally {
                retriever.release()
            }
        }
    }.getOrNull() ?: DEFAULT_DURATION_MS

    private companion object {
        const val DEFAULT_DURATION_MS = 3_000L
    }
}
