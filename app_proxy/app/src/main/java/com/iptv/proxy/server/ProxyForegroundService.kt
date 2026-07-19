package com.iptv.proxy.server

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat

class ProxyForegroundService : Service() {

    private val CHANNEL_ID = "IPTVProxyChannel"
    private lateinit var ktorServer: LocalKtorServer

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        ktorServer = LocalKtorServer(applicationContext)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification: Notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("IPTV Proxy Server Running")
            .setContentText("Listening on http://127.0.0.1:8080")
            //.setSmallIcon(R.drawable.ic_proxy) // Un-comment when icon is added
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

        // Start the service in the foreground to prevent OS kills
        startForeground(1, notification)

        // Launch the Ktor server on a background thread
        Thread {
            ktorServer.start()
        }.start()

        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        ktorServer.stop()
    }

    override fun onBind(intent: Intent): IBinder? {
        return null // Not bound, started
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val serviceChannel = NotificationChannel(
                CHANNEL_ID,
                "IPTV Proxy Service Channel",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(serviceChannel)
        }
    }
}
