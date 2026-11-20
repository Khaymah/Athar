package com.khaymah.athar

import org.junit.Assert.assertEquals
import org.junit.Test

class ZikrSettingsTest {
    private fun settings(order: List<String>, enabled: Set<String>) =
        ZikrSettings(intervalSeconds = 5, order = order, enabled = enabled, shuffle = false, volume = 1f)

    @Test
    fun activePhrasesFollowOrderAndSkipDisabledOrUnknown() {
        val active = settings(
            order = listOf("allahu_akbar", "unknown", "subhanallah", "alhamdulillah"),
            enabled = setOf("subhanallah", "allahu_akbar", "unknown"),
        ).activePhrases

        assertEquals(listOf("allahu_akbar", "subhanallah"), active.map { it.id })
    }

    @Test
    fun noEnabledPhrasesMeansNothingToPlay() {
        assertEquals(emptyList<Phrase>(), settings(Phrases.all.map { it.id }, emptySet()).activePhrases)
    }

    @Test
    fun everyPhraseHasAUniqueId() {
        assertEquals(Phrases.all.size, Phrases.all.map { it.id }.toSet().size)
    }
}
