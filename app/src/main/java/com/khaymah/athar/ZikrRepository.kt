package com.khaymah.athar

import android.content.Context
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.core.handlers.ReplaceFileCorruptionHandler
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

data class ZikrSettings(
    val intervalSeconds: Int,
    val order: List<String>,
    val enabled: Set<String>,
    val shuffle: Boolean,
    val volume: Float,
) {
    val activePhrases: List<Phrase>
        get() = order.filter { it in enabled }.mapNotNull(Phrases::byId)
}

private val Context.dataStore by preferencesDataStore(
    name = "athar",
    corruptionHandler = ReplaceFileCorruptionHandler { emptyPreferences() },
)

class ZikrRepository(context: Context) {
    private val store = context.applicationContext.dataStore

    val settings: Flow<ZikrSettings> = store.data.map { p ->
        ZikrSettings(
            intervalSeconds = (p[Keys.interval] ?: DEFAULT_INTERVAL).coerceIn(MIN_INTERVAL, MAX_INTERVAL),
            order = orderOf(p),
            enabled = enabledOf(p),
            shuffle = p[Keys.shuffle] ?: false,
            volume = p[Keys.volume] ?: 1f,
        )
    }

    val wasRunning: Flow<Boolean> = store.data.map { it[Keys.running] ?: false }

    val autostartOpened: Flow<Boolean> = store.data.map { it[Keys.autostartOpened] ?: false }

    suspend fun markAutostartOpened() {
        store.edit { it[Keys.autostartOpened] = true }
    }

    suspend fun setRunning(running: Boolean) {
        store.edit { it[Keys.running] = running }
    }

    suspend fun setInterval(seconds: Int) {
        store.edit { it[Keys.interval] = seconds.coerceIn(MIN_INTERVAL, MAX_INTERVAL) }
    }

    suspend fun setShuffle(shuffle: Boolean) {
        store.edit { it[Keys.shuffle] = shuffle }
    }

    suspend fun setVolume(volume: Float) {
        store.edit { it[Keys.volume] = volume.coerceIn(0f, 1f) }
    }

    suspend fun toggle(id: String) {
        store.edit { p ->
            val enabled = enabledOf(p)
            p[Keys.enabled] = if (id in enabled) enabled - id else enabled + id
        }
    }

    suspend fun move(id: String, delta: Int) {
        store.edit { p ->
            val order = orderOf(p).toMutableList()
            val from = order.indexOf(id)
            val to = from + delta
            if (from < 0 || to !in order.indices) return@edit
            order.add(to, order.removeAt(from))
            p[Keys.order] = order.joinToString(",")
        }
    }

    private fun orderOf(p: Preferences): List<String> {
        val saved = p[Keys.order]?.split(',')?.filter { Phrases.byId(it) != null }.orEmpty()
        return saved + Phrases.all.map { it.id }.filterNot { it in saved }
    }

    private fun enabledOf(p: Preferences): Set<String> =
        p[Keys.enabled] ?: Phrases.all.map { it.id }.toSet()

    private object Keys {
        val interval = intPreferencesKey("interval_seconds")
        val order = stringPreferencesKey("order")
        val enabled = stringSetPreferencesKey("enabled")
        val shuffle = booleanPreferencesKey("shuffle")
        val volume = floatPreferencesKey("volume")
        val autostartOpened = booleanPreferencesKey("autostart_opened")
        val running = booleanPreferencesKey("running")
    }

    companion object {
        const val DEFAULT_INTERVAL = 5
        const val MIN_INTERVAL = 3
        const val MAX_INTERVAL = 60
    }
}
