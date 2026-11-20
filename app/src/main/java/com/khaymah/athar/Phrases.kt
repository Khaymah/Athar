package com.khaymah.athar

import androidx.annotation.RawRes

data class Phrase(val id: String, val text: String, @RawRes val sound: Int)

object Phrases {
    val all = listOf(
        Phrase("subhanallah", "سُبْحَانَ اللَّهِ", R.raw.subhanallah),
        Phrase("alhamdulillah", "الْحَمْدُ لِلَّهِ", R.raw.alhamdulillah),
        Phrase("lailaha_illallah", "لَا إِلَٰهَ إِلَّا اللَّهُ", R.raw.lailaha_illallah),
        Phrase("allahu_akbar", "اللَّهُ أَكْبَرُ", R.raw.allahu_akbar),
        Phrase("astaghfirullah", "أَسْتَغْفِرُ اللَّهَ", R.raw.astaghfirullah),
        Phrase("subhanallah_wabihamdih", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", R.raw.subhanallah_wabihamdih),
        Phrase("subhanallah_alazim", "سُبْحَانَ اللَّهِ الْعَظِيمِ", R.raw.subhanallah_alazim),
        Phrase("hawqala", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", R.raw.hawqala),
        Phrase("salawat", "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ", R.raw.salawat),
    )

    private val byId = all.associateBy { it.id }

    fun byId(id: String): Phrase? = byId[id]
}
