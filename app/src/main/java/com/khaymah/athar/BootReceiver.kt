package com.khaymah.athar

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val afterBoot = intent.action == Intent.ACTION_BOOT_COMPLETED
        if (!afterBoot && intent.action != Intent.ACTION_MY_PACKAGE_REPLACED) return
        val result = goAsync()
        CoroutineScope(Dispatchers.Default).launch {
            try {
                if (ZikrRepository(context).wasRunning.first()) resume(context, afterBoot)
            } finally {
                result.finish()
            }
        }
    }

    private fun resume(context: Context, afterBoot: Boolean) {
        if (afterBoot && Build.VERSION.SDK_INT >= Build.VERSION_CODES.VANILLA_ICE_CREAM) {
            ZikrNotifications.showResume(context)
            return
        }
        runCatching { ZikrService.start(context) }
            .onFailure { ZikrNotifications.showResume(context) }
    }
}
