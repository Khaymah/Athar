package com.khaymah.athar

import androidx.annotation.RawRes

data class Voice(val id: String, val name: String, private val sounds: Map<String, Int>) {
    @RawRes
    fun soundFor(phrase: Phrase): Int = sounds[phrase.id] ?: phrase.sound

    fun covers(phrase: Phrase): Boolean = sounds.isEmpty() || phrase.id in sounds
}

object Voices {
    val sabry = Voice("sabry", "Sabry Dawood", emptyMap())

    val hummada = Voice(
        "hummada",
        "Mohammad Alhummada",
        mapOf(
            "subhanallah" to R.raw.hummada_subhanallah,
            "alhamdulillah" to R.raw.hummada_alhamdulillah,
            "lailaha_illallah" to R.raw.hummada_lailaha_illallah,
            "allahu_akbar" to R.raw.hummada_allahu_akbar,
            "astaghfirullah" to R.raw.hummada_astaghfirullah,
            "subhanallah_wabihamdih" to R.raw.hummada_subhanallah_wabihamdih,
            "subhanallah_alazim" to R.raw.hummada_subhanallah_alazim,
            "salawat" to R.raw.hummada_salawat,
        ),
    )

    val all = listOf(sabry, hummada)

    fun byId(id: String?): Voice = all.firstOrNull { it.id == id } ?: sabry
}
