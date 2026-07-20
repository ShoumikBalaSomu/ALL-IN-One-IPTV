package com.iptv.proxy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawWithCache
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ProxyTheme {
                ProxyDashboard()
            }
        }
    }
}

@Composable
fun ProxyTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            background = Color(0xFF090A0F),
            surface = Color(0xFF14151E),
            primary = Color(0xFF00E5FF),
            secondary = Color(0xFFB900FF),
            tertiary = Color(0xFFFF0055),
            onBackground = Color.White,
            onSurface = Color.White
        ),
        content = content
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProxyDashboard() {
    var isProxyActive by remember { mutableStateOf(false) }
    var foldedCount by remember { mutableIntStateOf(14502) }
    var blockedCount by remember { mutableIntStateOf(329) }
    var bandwidth by remember { mutableFloatStateOf(0f) }
    
    val showVpnSheet = remember { mutableStateOf(false) }

    // Simulation loop
    LaunchedEffect(isProxyActive) {
        if (isProxyActive) {
            while (true) {
                delay(800)
                foldedCount += (0..5).random()
                blockedCount += (0..2).random()
                bandwidth = (10..150).random().toFloat() / 10f
            }
        } else {
            bandwidth = 0f
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        floatingActionButton = {
            FloatingActionButton(
                onClick = { showVpnSheet.value = true },
                containerColor = MaterialTheme.colorScheme.surface,
                contentColor = MaterialTheme.colorScheme.primary,
                shape = CircleShape
            ) {
                Icon(Icons.Default.Lock, contentDescription = "VPN Settings")
            }
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize()) {
            // Background grid & cyber aesthetic
            CyberBackground(isActive = isProxyActive)

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(horizontal = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(40.dp))
                
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "NEXUS CORE",
                            fontSize = 32.sp,
                            fontWeight = FontWeight.Black,
                            letterSpacing = 4.sp,
                            color = Color.White
                        )
                        Text(
                            text = "v2.0.4 // REAL-TIME OPTIMIZER",
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.primary.copy(alpha = 0.7f),
                            letterSpacing = 2.sp,
                            fontFamily = FontFamily.Monospace
                        )
                    }
                    Icon(
                        imageVector = Icons.Default.Refresh,
                        contentDescription = null,
                        tint = if (isProxyActive) MaterialTheme.colorScheme.primary else Color.Gray,
                        modifier = Modifier.size(32.dp)
                    )
                }

                Spacer(modifier = Modifier.height(60.dp))

                // The Core Reactor (Animated)
                CoreReactor(isActive = isProxyActive)

                Spacer(modifier = Modifier.height(60.dp))

                // Data Cards
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    CyberStatCard(
                        modifier = Modifier.weight(1f),
                        title = "FOLDED",
                        value = String.format("%,d", foldedCount),
                        accent = MaterialTheme.colorScheme.primary,
                        icon = Icons.Default.Share
                    )
                    CyberStatCard(
                        modifier = Modifier.weight(1f),
                        title = "BLOCKED",
                        value = String.format("%,d", blockedCount),
                        accent = MaterialTheme.colorScheme.tertiary,
                        icon = Icons.Default.Warning
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                // Bandwidth meter
                BandwidthMeter(bandwidth = bandwidth, isActive = isProxyActive)

                Spacer(modifier = Modifier.weight(1f))

                // Engage Button
                EngageButton(isActive = isProxyActive) {
                    isProxyActive = !isProxyActive
                }
                
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
        
        if (showVpnSheet.value) {
            ModalBottomSheet(
                onDismissRequest = { showVpnSheet.value = false },
                containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f),
                scrimColor = Color.Black.copy(alpha = 0.6f)
            ) {
                VpnSettingsSheet()
            }
        }
    }
}

@Composable
fun CyberBackground(isActive: Boolean) {
    val infiniteTransition = rememberInfiniteTransition()
    val alphaAnim by infiniteTransition.animateFloat(
        initialValue = 0.2f,
        targetValue = 0.5f,
        animationSpec = infiniteRepeatable(tween(4000), RepeatMode.Reverse)
    )

    Box(modifier = Modifier.fillMaxSize()) {
        // Gradient blobs
        Canvas(modifier = Modifier.fillMaxSize().blur(80.dp)) {
            val color = if (isActive) Color(0xFF00E5FF) else Color(0xFFFF0055)
            drawCircle(
                color = color.copy(alpha = alphaAnim * 0.3f),
                radius = size.width * 0.7f,
                center = Offset(0f, 0f)
            )
            drawCircle(
                color = Color(0xFFB900FF).copy(alpha = 0.1f),
                radius = size.width * 0.8f,
                center = Offset(size.width, size.height)
            )
        }
    }
}

@Composable
fun CoreReactor(isActive: Boolean) {
    val infiniteTransition = rememberInfiniteTransition()
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(tween(if (isActive) 3000 else 20000, easing = LinearEasing))
    )
    
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0.95f,
        targetValue = 1.05f,
        animationSpec = infiniteRepeatable(tween(if (isActive) 800 else 3000, easing = FastOutSlowInEasing), RepeatMode.Reverse)
    )

    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier.size(240.dp)
    ) {
        Canvas(modifier = Modifier.fillMaxSize().scale(pulse)) {
            val radius = size.width / 2
            val center = Offset(radius, radius)
            
            // Outer ring
            drawCircle(
                color = Color.White.copy(alpha = 0.05f),
                radius = radius,
                style = Stroke(width = 2.dp.toPx())
            )
            
            // Spinning dashed ring
            rotate(rotation, center) {
                drawArc(
                    brush = Brush.sweepGradient(
                        listOf(Color.Transparent, if (isActive) Color(0xFF00E5FF) else Color(0xFFFF0055), Color.Transparent)
                    ),
                    startAngle = 0f,
                    sweepAngle = 270f,
                    useCenter = false,
                    style = Stroke(
                        width = 8.dp.toPx(),
                        cap = StrokeCap.Round,
                        pathEffect = PathEffect.dashPathEffect(floatArrayOf(40f, 20f))
                    ),
                    topLeft = Offset(16.dp.toPx(), 16.dp.toPx()),
                    size = androidx.compose.ui.geometry.Size(size.width - 32.dp.toPx(), size.height - 32.dp.toPx())
                )
            }
            
            // Inner glowing core
            drawCircle(
                brush = Brush.radialGradient(
                    colors = if (isActive) listOf(Color(0xFF00E5FF).copy(alpha = 0.4f), Color.Transparent)
                             else listOf(Color(0xFFFF0055).copy(alpha = 0.2f), Color.Transparent)
                ),
                radius = radius * 0.7f
            )
        }
        
        // Center Status
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(
                imageVector = if (isActive) Icons.Default.Lock else Icons.Default.Clear,
                contentDescription = null,
                tint = if (isActive) Color(0xFF00E5FF) else Color(0xFFFF0055),
                modifier = Modifier.size(48.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = if (isActive) "ONLINE" else "STANDBY",
                fontWeight = FontWeight.Black,
                fontSize = 20.sp,
                color = Color.White,
                letterSpacing = 4.sp
            )
        }
    }
}

@Composable
fun CyberStatCard(modifier: Modifier = Modifier, title: String, value: String, accent: Color, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Box(
        modifier = modifier
            .height(110.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.6f))
            .border(1.dp, Color.White.copy(alpha = 0.1f), RoundedCornerShape(16.dp))
    ) {
        // Accent line
        Box(modifier = Modifier.fillMaxHeight().width(4.dp).background(accent).align(Alignment.CenterStart))
        
        Column(
            modifier = Modifier.padding(start = 20.dp, top = 16.dp, bottom = 16.dp, end = 16.dp),
            horizontalAlignment = Alignment.Start
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(icon, contentDescription = null, tint = accent.copy(alpha = 0.8f), modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(6.dp))
                Text(text = title, fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            }
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = value,
                fontSize = 28.sp,
                fontWeight = FontWeight.Black,
                color = Color.White,
                fontFamily = FontFamily.Monospace
            )
        }
    }
}

@Composable
fun BandwidthMeter(bandwidth: Float, isActive: Boolean) {
    val animatedBandwidth by animateFloatAsState(targetValue = bandwidth, animationSpec = tween(500))
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.6f))
            .padding(16.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color.Gray)
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("TRAFFIC THROUGHPUT", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    Text(if (isActive) "${String.format("%.1f", animatedBandwidth)} MB/s" else "0.0 MB/s", fontSize = 12.sp, color = MaterialTheme.colorScheme.primary, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(8.dp))
                // Progress bar
                Box(modifier = Modifier.fillMaxWidth().height(4.dp).background(Color.White.copy(alpha = 0.1f), CircleShape)) {
                    Box(modifier = Modifier.fillMaxHeight().fillMaxWidth(fraction = (animatedBandwidth / 20f).coerceIn(0f, 1f)).background(
                        Brush.horizontalGradient(listOf(MaterialTheme.colorScheme.secondary, MaterialTheme.colorScheme.primary)), CircleShape
                    ))
                }
            }
        }
    }
}

@Composable
fun EngageButton(isActive: Boolean, onClick: () -> Unit) {
    val accent = if (isActive) Color(0xFFFF0055) else Color(0xFF00E5FF)
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(64.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(
                Brush.horizontalGradient(
                    colors = listOf(accent.copy(alpha = 0.2f), accent.copy(alpha = 0.05f))
                )
            )
            .border(2.dp, accent.copy(alpha = 0.5f), RoundedCornerShape(20.dp))
            .clickable { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = if (isActive) "DISENGAGE OPTIMIZER" else "INITIALIZE OPTIMIZER",
            color = accent,
            fontSize = 16.sp,
            fontWeight = FontWeight.Black,
            letterSpacing = 2.sp
        )
    }
}

@Composable
fun VpnSettingsSheet() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(24.dp)
    ) {
        Text("VPN GATEWAY", fontSize = 20.sp, fontWeight = FontWeight.Black, color = Color.White)
        Text("Route proxy traffic securely", fontSize = 12.sp, color = Color.Gray)
        Spacer(modifier = Modifier.height(24.dp))
        
        OutlinedTextField(
            value = "",
            onValueChange = {},
            label = { Text("OpenVPN Profile (.ovpn)") },
            modifier = Modifier.fillMaxWidth(),
            trailingIcon = { Icon(Icons.Default.Settings, contentDescription = null) },
            colors = OutlinedTextFieldDefaults.colors(
                unfocusedBorderColor = Color.White.copy(alpha = 0.2f),
                focusedBorderColor = MaterialTheme.colorScheme.primary
            )
        )
        Spacer(modifier = Modifier.height(16.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Kill Switch", color = Color.White, fontWeight = FontWeight.SemiBold)
            Switch(checked = true, onCheckedChange = {})
        }
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = { },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary, contentColor = Color.Black)
        ) {
            Text("CONNECT VPN", fontWeight = FontWeight.Black)
        }
        Spacer(modifier = Modifier.height(24.dp))
    }
}
