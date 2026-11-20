package com.khaymah.athar

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class UpdaterTest {
    @Test
    fun comparesVersionsNumericallyWithOrWithoutPrefix() {
        assertTrue(Updater.isNewer("v0.4.0", "0.3.0"))
        assertTrue(Updater.isNewer("v0.10.0", "v0.9.9"))
        assertTrue(Updater.isNewer("v1.0", "0.9.9"))
        assertFalse(Updater.isNewer("v0.3.0", "v0.3.0"))
        assertFalse(Updater.isNewer("v0.3.0", "0.3.1"))
        assertFalse(Updater.isNewer("v0.3", "0.3.0"))
    }

    @Test
    fun picksTheSignedApkAssetAndIgnoresDebugBuilds() {
        val json = """
            {"tag_name":"v0.4.0","assets":[
              {"name":"athar-v0.4.0-debug.apk","browser_download_url":"https://x/debug.apk"},
              {"name":"athar-v0.4.0.apk","browser_download_url":"https://x/release.apk"}
            ]}
        """.trimIndent()
        assertEquals(AppRelease("v0.4.0", "https://x/release.apk"), Updater.parseRelease(json))
    }

    @Test
    fun releaseWithoutApkIsIgnored() {
        assertNull(Updater.parseRelease("""{"tag_name":"v0.4.0","assets":[]}"""))
    }
}
