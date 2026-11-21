package com.khaymah.athar

data class Phrase(val id: String, val text: String)

object Phrases {
    val all = listOf(
        Phrase("subhanallah", "سُبْحَانَ اللَّهِ"),
        Phrase("alhamdulillah", "الْحَمْدُ لِلَّهِ"),
        Phrase("lailaha_illallah", "لَا إِلَٰهَ إِلَّا اللَّهُ"),
        Phrase("allahu_akbar", "اللَّهُ أَكْبَرُ"),
        Phrase("astaghfirullah", "أَسْتَغْفِرُ اللَّهَ"),
        Phrase("subhanallah_wabihamdih", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ"),
        Phrase("subhanallah_alazim", "سُبْحَانَ اللَّهِ الْعَظِيمِ"),
        Phrase("hawqala", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ"),
        Phrase("salawat", "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ"),
    )

    private val byId = all.associateBy { it.id }

    fun byId(id: String): Phrase? = byId[id]
}
