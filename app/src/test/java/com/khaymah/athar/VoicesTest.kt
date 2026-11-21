package com.khaymah.athar

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

class VoicesTest {
    private val hawqala = Phrases.byId("hawqala")!!
    private val voicesDir = File("src/main/assets/voices")

    @Test
    fun missingClipFallsBackToTheDefaultVoiceFolder() {
        val partial = Voice("Someone", setOf("subhanallah"))
        assertEquals("voices/Sabry Dawood/hawqala.ogg", partial.clipFor(hawqala))
        assertEquals("voices/Someone/subhanallah.ogg", partial.clipFor(Phrases.byId("subhanallah")!!))
    }

    @Test
    fun legacyIdsFromV050MapToFolderNames() {
        assertEquals("Sabry Dawood", Voices.resolve("sabry"))
        assertEquals("Mohammad Alhummada", Voices.resolve("hummada"))
        assertEquals("Sabry Dawood", Voices.resolve(null))
    }

    @Test
    fun defaultVoiceIsListedFirst() {
        assertEquals(listOf("Sabry Dawood", "A", "Z"), Voices.sortDefaultFirst(listOf("Z", "Sabry Dawood", "A")))
    }

    @Test
    fun defaultVoiceFolderHasEveryPhraseSoFallbackNeverMisses() {
        val clips = File(voicesDir, Voices.DEFAULT).list().orEmpty().toSet()
        Phrases.all.forEach { assertTrue("missing ${it.id}", "${it.id}.ogg" in clips) }
    }

    @Test
    fun everyClipInEveryVoiceFolderIsAKnownPhrase() {
        voicesDir.listFiles().orEmpty().forEach { voice ->
            voice.list().orEmpty().forEach { name ->
                assertTrue("${voice.name}/$name", Phrases.byId(name.removeSuffix(".ogg")) != null)
            }
        }
    }
}
