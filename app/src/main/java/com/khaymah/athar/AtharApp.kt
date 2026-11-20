package com.khaymah.athar

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.LifecycleResumeEffect
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

private enum class Screen { Home, Settings }

private data class PermissionItem(val title: String, val granted: Boolean, val onFix: () -> Unit)

@Composable
fun AtharTheme(content: @Composable () -> Unit) {
    val scheme = if (isSystemInDarkTheme()) {
        darkColorScheme(primary = Color(0xFF7FD1A8), secondary = Color(0xFF9CCFB6))
    } else {
        lightColorScheme(primary = Color(0xFF2E7D5B), secondary = Color(0xFF4F7A66))
    }
    MaterialTheme(colorScheme = scheme, content = content)
}

@Composable
fun AtharApp(repository: ZikrRepository, onStart: () -> Unit, onRequestNotifications: () -> Unit) {
    var screen by rememberSaveable { mutableStateOf(Screen.Home) }
    val settings by repository.settings.collectAsState(initial = null)
    val playback by ZikrService.state.collectAsState()
    val permissions = rememberPermissions(repository, onRequestNotifications)

    BackHandler(enabled = screen == Screen.Settings) { screen = Screen.Home }

    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        val current = settings ?: return@Surface
        Column(
            modifier = Modifier
                .safeDrawingPadding()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            when (screen) {
                Screen.Home -> HomeScreen(current, playback, permissions, onStart) { screen = Screen.Settings }
                Screen.Settings -> SettingsScreen(current, permissions, repository) { screen = Screen.Home }
            }
        }
    }
}

@Composable
private fun rememberPermissions(repository: ZikrRepository, onRequestNotifications: () -> Unit): List<PermissionItem> {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val autostartOpened by repository.autostartOpened.collectAsState(initial = false)
    var refresh by remember { mutableIntStateOf(0) }
    LifecycleResumeEffect(Unit) {
        refresh++
        onPauseOrDispose { }
    }
    return remember(refresh, autostartOpened) {
        buildList {
            add(PermissionItem("الإشعارات", Reliability.notificationsEnabled(context), onRequestNotifications))
            add(PermissionItem("العمل بدون قيود البطارية", Reliability.isBatteryExempt(context)) {
                Reliability.requestBatteryExemption(context)
            })
            if (Reliability.needsAutostart()) {
                add(PermissionItem("التشغيل التلقائي في الخلفية", autostartOpened) {
                    Reliability.openAutostartSettings(context)
                    scope.launch { repository.markAutostartOpened() }
                })
            }
        }
    }
}

@Composable
private fun HomeScreen(
    settings: ZikrSettings,
    playback: PlaybackState,
    permissions: List<PermissionItem>,
    onStart: () -> Unit,
    onOpenSettings: () -> Unit,
) {
    val context = LocalContext.current

    Text("أثر", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)

    Card(modifier = Modifier.fillMaxWidth()) {
        val status = when (playback.status) {
            PlaybackStatus.Playing -> "شغّال · كل ${settings.intervalSeconds} ثانية"
            PlaybackStatus.Paused -> "متوقف مؤقتاً"
            PlaybackStatus.Stopped -> "متوقف"
        }
        Text(
            status,
            modifier = Modifier.fillMaxWidth().padding(28.dp),
            fontSize = 24.sp,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.primary,
        )
    }

    val hasPhrases = settings.activePhrases.isNotEmpty()
    when (playback.status) {
        PlaybackStatus.Stopped -> Button(onClick = onStart, enabled = hasPhrases, modifier = Modifier.fillMaxWidth()) {
            Text(if (hasPhrases) "تشغيل" else "اختار عبارة واحدة على الأقل من الإعدادات")
        }
        PlaybackStatus.Playing, PlaybackStatus.Paused -> Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            val paused = playback.status == PlaybackStatus.Paused
            Button(
                onClick = { if (paused) onStart() else ZikrService.pause(context) },
                modifier = Modifier.weight(1f),
            ) { Text(if (paused) "استئناف" else "إيقاف مؤقت") }
            OutlinedButton(onClick = { ZikrService.stop(context) }, modifier = Modifier.weight(1f)) { Text("إيقاف") }
        }
    }

    val missing = permissions.filterNot { it.granted }
    if (missing.isNotEmpty()) {
        Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("صلاحيات ناقصة عشان التطبيق مايتقفلش", fontWeight = FontWeight.Bold)
                missing.forEach { PermissionRow(it) }
            }
        }
    }

    OutlinedButton(onClick = onOpenSettings, modifier = Modifier.fillMaxWidth()) { Text("الإعدادات") }
}

@Composable
private fun PermissionRow(item: PermissionItem) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Text(if (item.granted) "✓" else "✗", color = if (item.granted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error)
        Spacer(Modifier.width(8.dp))
        Text(item.title, modifier = Modifier.weight(1f))
        TextButton(onClick = item.onFix) { Text(if (item.granted) "فتح" else "اسمح") }
    }
}

@Composable
private fun SettingsScreen(
    settings: ZikrSettings,
    permissions: List<PermissionItem>,
    repository: ZikrRepository,
    onBack: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var interval by remember(settings.intervalSeconds) { mutableFloatStateOf(settings.intervalSeconds.toFloat()) }
    var volume by remember(settings.volume) { mutableFloatStateOf(settings.volume) }

    Row(verticalAlignment = Alignment.CenterVertically) {
        TextButton(onClick = onBack) { Text("→ رجوع") }
        Spacer(Modifier.width(8.dp))
        Text("الإعدادات", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
    }

    Text("الفاصل: ${interval.roundToInt()} ثانية", fontWeight = FontWeight.Bold)
    Slider(
        value = interval,
        onValueChange = { interval = it },
        onValueChangeFinished = { scope.launch { repository.setInterval(interval.roundToInt()) } },
        valueRange = ZikrRepository.MIN_INTERVAL.toFloat()..ZikrRepository.MAX_INTERVAL.toFloat(),
        steps = ZikrRepository.MAX_INTERVAL - ZikrRepository.MIN_INTERVAL - 1,
    )

    Text("مستوى الصوت: ${(volume * 100).roundToInt()}%", fontWeight = FontWeight.Bold)
    Slider(
        value = volume,
        onValueChange = { volume = it },
        onValueChangeFinished = { scope.launch { repository.setVolume(volume) } },
        valueRange = 0.1f..1f,
    )

    Row(verticalAlignment = Alignment.CenterVertically) {
        Text("ترتيب عشوائي", modifier = Modifier.weight(1f), fontWeight = FontWeight.Bold)
        Switch(checked = settings.shuffle, onCheckedChange = { scope.launch { repository.setShuffle(it) } })
    }

    Text("العبارات", fontWeight = FontWeight.Bold)
    settings.order.forEachIndexed { index, id ->
        val phrase = Phrases.byId(id) ?: return@forEachIndexed
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = id in settings.enabled, onCheckedChange = { scope.launch { repository.toggle(id) } })
            Text(phrase.text, modifier = Modifier.weight(1f))
            TextButton(onClick = { scope.launch { repository.move(id, -1) } }, enabled = index > 0) { Text("▲") }
            TextButton(onClick = { scope.launch { repository.move(id, 1) } }, enabled = index < settings.order.lastIndex) { Text("▼") }
        }
    }

    HorizontalDivider()
    Text("الصلاحيات", fontWeight = FontWeight.Bold)
    permissions.forEach { PermissionRow(it) }
}
