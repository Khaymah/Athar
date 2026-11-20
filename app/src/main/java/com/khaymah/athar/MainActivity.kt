package com.khaymah.athar

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private val notificationPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            if (!granted) Reliability.openNotificationSettings(this)
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val repository = ZikrRepository(this)
        setContent {
            AtharTheme {
                CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
                    AtharApp(
                        repository = repository,
                        onStart = { ZikrService.start(this) },
                        onRequestNotifications = ::requestNotifications,
                    )
                }
            }
        }
        handleAutostart(intent)
        lifecycleScope.launch { Updater.check(this@MainActivity) }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleAutostart(intent)
    }

    private fun handleAutostart(intent: Intent) {
        if (intent.getBooleanExtra(EXTRA_INSTALL_UPDATE, false)) {
            intent.removeExtra(EXTRA_INSTALL_UPDATE)
            lifecycleScope.launch { Updater.install(this@MainActivity) }
        }
        if (!intent.getBooleanExtra(EXTRA_AUTOSTART, false)) return
        intent.removeExtra(EXTRA_AUTOSTART)
        ZikrService.start(this)
    }

    private fun requestNotifications() {
        val canAsk = Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        if (canAsk) {
            notificationPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        } else {
            Reliability.openNotificationSettings(this)
        }
    }

    companion object {
        const val EXTRA_AUTOSTART = "autostart"
        const val EXTRA_INSTALL_UPDATE = "install_update"
    }
}
