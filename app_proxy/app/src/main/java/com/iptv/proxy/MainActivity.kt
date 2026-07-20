package com.iptv.proxy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ProxyTheme {
                ProxyControlCenter()
            }
        }
    }
}

@Composable
fun ProxyTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            background = Color(0xFF0F1014),
            surface = Color(0xFF1E1E24),
            primary = Color(0xFF00FF7F),
            onPrimary = Color.Black,
            onBackground = Color.White,
            onSurface = Color.White
        ),
        content = content
    )
}

@Composable
fun ProxyControlCenter() {
    var isProxyRunning by remember { mutableStateOf(false) }
    var foldedChannels by remember { mutableIntStateOf(14502) }
    var deadLinksRemoved by remember { mutableIntStateOf(329) }
    
    // Pulsing animation for active state
    val infiniteTransition = rememberInfiniteTransition()
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = if (isProxyRunning) 1.05f else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    LaunchedEffect(isProxyRunning) {
        if (isProxyRunning) {
            while (true) {
                delay(1500)
                foldedChannels += (1..3).random()
                deadLinksRemoved += (0..1).random()
            }
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize()) {
            // Background ambient glow
            Box(modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.radialGradient(
                        colors = listOf(
                            if (isProxyRunning) Color(0xFF00FF7F).copy(alpha = 0.15f) else Color(0xFFE50914).copy(alpha = 0.15f),
                            Color.Transparent
                        ),
                        radius = 1000f
                    )
                )
            )

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(40.dp))
                
                Text(
                    text = "OPTIMIZER CORE",
                    fontSize = 32.sp,
                    fontWeight = FontWeight.Black,
                    letterSpacing = 4.sp,
                    color = Color.White
                )
                
                Text(
                    text = "Real-time deadlink removal engine",
                    fontSize = 14.sp,
                    color = Color.Gray,
                    modifier = Modifier.padding(top = 8.dp, bottom = 60.dp)
                )

                // Main Status Orb
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier
                        .size(200.dp)
                        .scale(pulseScale)
                        .clip(CircleShape)
                        .background(
                            Brush.sweepGradient(
                                colors = if (isProxyRunning) 
                                    listOf(Color(0xFF00FF7F), Color(0xFF00BFFF), Color(0xFF00FF7F)) 
                                else 
                                    listOf(Color(0xFFE50914), Color(0xFFFF4500), Color(0xFFE50914))
                            )
                        )
                        .border(4.dp, Color.White.copy(alpha = 0.1f), CircleShape)
                ) {
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .size(190.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.background)
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                imageVector = if (isProxyRunning) Icons.Default.CheckCircle else Icons.Default.Warning,
                                contentDescription = null,
                                tint = if (isProxyRunning) Color(0xFF00FF7F) else Color(0xFFE50914),
                                modifier = Modifier.size(48.dp)
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = if (isProxyRunning) "ACTIVE" else "OFFLINE",
                                fontWeight = FontWeight.Bold,
                                fontSize = 24.sp,
                                color = if (isProxyRunning) Color(0xFF00FF7F) else Color(0xFFE50914),
                                letterSpacing = 2.sp
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(60.dp))

                // Stats Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    StatCard("Folded", foldedChannels.toString(), Color(0xFF00BFFF))
                    StatCard("Dead Bypassed", deadLinksRemoved.toString(), Color(0xFFFF4500))
                }

                Spacer(modifier = Modifier.weight(1f))

                // Main Action Button
                Button(
                    onClick = { isProxyRunning = !isProxyRunning },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(65.dp),
                    shape = RoundedCornerShape(20.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isProxyRunning) Color(0xFF1E1E24) else Color(0xFF00FF7F),
                        contentColor = if (isProxyRunning) Color.White else Color.Black
                    ),
                    elevation = ButtonDefaults.buttonElevation(defaultElevation = 10.dp)
                ) {
                    Text(
                        text = if (isProxyRunning) "TERMINATE OPTIMIZER" else "INITIALIZE ENGINE",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Black,
                        letterSpacing = 1.5.sp
                    )
                }
                Spacer(modifier = Modifier.height(20.dp))
            }
        }
    }
}

@Composable
fun StatCard(label: String, value: String, accentColor: Color) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E24).copy(alpha = 0.8f)),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier
            .width(150.dp)
            .border(1.dp, Color.White.copy(alpha = 0.05f), RoundedCornerShape(20.dp))
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(text = value, fontSize = 28.sp, fontWeight = FontWeight.Black, color = accentColor)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = label, fontSize = 12.sp, color = Color.LightGray, fontWeight = FontWeight.SemiBold)
        }
    }
}
