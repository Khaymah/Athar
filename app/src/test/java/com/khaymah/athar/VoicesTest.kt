package com.khaymah.athar

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class VoicesTest {
    private val hawqala = Phrases.byId("hawqala")!!
    private val subhanallah = Phrases.byId("subhanallah")!!

    @Test
    fun voiceWithoutAClipFallsBackToTheDefaultRecording() {
        assertEquals(hawqala.sound, Voices.hummada.soundFor(hawqala))
        assertFalse(Voices.hummada.covers(hawqala))
    }

    @Test
    fun voiceUsesItsOwnClipWhenItHasOne() {
        assertNotEquals(subhanallah.sound, Voices.hummada.soundFor(subhanallah))
        assertTrue(Voices.hummada.covers(subhanallah))
    }

    @Test
    fun unknownOrMissingVoiceIdMeansTheDefaultVoice() {
        assertEquals(Voices.sabry, Voices.byId(null))
        assertEquals(Voices.sabry, Voices.byId("removed"))
        assertTrue(Phrases.all.all(Voices.sabry::covers))
    }
}
