package com.khaymah.athar

import android.content.Context

data class Voice(val name: String, val clips: Set<String>) {
    fun covers(phrase: Phrase): Boolean = phrase.id in clips

    fun clipFor(phrase: Phrase): String =
        Voices.clipPath(if (covers(phrase)) name else Voices.DEFAULT, phrase)
}

object Voices {
    const val DEFAULT = "Sabry Dawood"
    private const val ROOT = "voices"
    private const val EXTENSION = ".ogg"
    private val legacyIds = mapOf("sabry" to DEFAULT, "hummada" to "Mohammad Alhummada")

    @Volatile
    private var cache: List<Voice>? = null

    fun all(context: Context): List<Voice> = cache ?: load(context).also { cache = it }

    fun find(context: Context, name: String?): Voice {
        val voices = all(context)
        val wanted = resolve(name)
        return voices.firstOrNull { it.name == wanted } ?: voices.first { it.name == DEFAULT }
    }

    fun resolve(name: String?): String = legacyIds[name] ?: name ?: DEFAULT

    fun clipPath(voiceName: String, phrase: Phrase): String = "$ROOT/$voiceName/${phrase.id}$EXTENSION"

    fun sortDefaultFirst(names: List<String>): List<String> =
        names.sortedWith(compareBy<String> { it != DEFAULT }.thenBy { it })

    private fun load(context: Context): List<Voice> {
        val assets = context.applicationContext.assets
        return sortDefaultFirst(assets.list(ROOT).orEmpty().toList()).map { name ->
            val clips = assets.list("$ROOT/$name").orEmpty()
                .filter { it.endsWith(EXTENSION) }
                .map { it.removeSuffix(EXTENSION) }
                .toSet()
            Voice(name, clips)
        }
    }
}
