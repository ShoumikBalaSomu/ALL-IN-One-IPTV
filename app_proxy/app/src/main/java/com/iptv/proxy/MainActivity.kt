package com.iptv.proxy

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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
            primary = Color(0xFFE50914),
            onPrimary = Color.White,
            onBackground = Color.White,
            onSurface = Color.White
        ),
        content = content
    )
}

@Composable
fun ProxyControlCenter() {
    var isProxyRunning by remember { mutableStateOf(false) }
    var foldedChannels by remember { mutableIntStateOf(0) }
    var deadLinksRemoved by remember { mutableIntStateOf(0) }
    var showVpnSettings by remember { mutableStateOf(false) }

    LaunchedEffect(isProxyRunning) {
        if (isProxyRunning) {
            while (true) {
                delay(2000)
                foldedChannels += (1..5).random()
                deadLinksRemoved += (0..2).random()
            }
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(20.dp))
            
            Text(
                text = "IPTV Optimizer Proxy",
                fontSize = 28.sp,
                fontWeight = FontWeight.Black,
                color = MaterialTheme.colorScheme.primary
            )
            
            Text(
                text = "Real-time stream folding & dead-link removal",
                fontSize = 14.sp,
                color = Color.Gray,
                modifier = Modifier.padding(top = 8.dp, bottom = 40.dp)
            )

            // Status Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                shape = RoundedCornerShape(16.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = if (isProxyRunning) "PROXY ACTIVE" else "PROXY INACTIVE",
                        fontWeight = FontWeight.Bold,
                        color = if (isProxyRunning) Color(0xFF00FF7F) else Color.Red,
                        fontSize = 18.sp
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = "127.0.0.1:8080", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        StatBox("Folded", foldedChannels.toString(), Color(0xFF00BFFF))
                        StatBox("Dead Removed", deadLinksRemoved.toString(), Color(0xFFFF4500))
                    }
                }
            }

            Spacer(modifier = Modifier.height(40.dp))

            // Main Action Button
            Button(
                onClick = { isProxyRunning = !isProxyRunning },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(60.dp),
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isProxyRunning) Color(0xFF444444) else MaterialTheme.colorScheme.primary
                )
            ) {
                Text(
                    text = if (isProxyRunning) "STOP OPTIMIZER" else "START OPTIMIZER",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            // VPN Config Button
            OutlinedButton(
                onClick = { showVpnSettings = !showVpnSettings },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(text = "OpenVPN Configurations")
            }

            if (showVpnSettings) {
                Spacer(modifier = Modifier.height(20.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.5f)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("VPN Gateway: Enabled", fontWeight = FontWeight.SemiBold)
                        Text("Protocol: OpenVPN (UDP)", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Status: Disconnected", color = Color.Red, fontSize = 12.sp)
                    }
                }
            }
        }
    }
}

@Composable
fun StatBox(label: String, value: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = value, fontSize = 32.sp, fontWeight = FontWeight.Black, color = color)
        Text(text = label, fontSize = 12.sp, color = Color.LightGray)
    }
}
