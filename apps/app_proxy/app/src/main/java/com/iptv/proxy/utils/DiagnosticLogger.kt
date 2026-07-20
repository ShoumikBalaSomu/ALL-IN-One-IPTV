package com.iptv.proxy.utils

import android.content.Context
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object DiagnosticLogger {
    
    private const val LOG_FILE_NAME = "proxy_diagnostics.log"

    fun logError(context: Context, category: String, message: String) {
        try {
            val file = File(context.filesDir, LOG_FILE_NAME)
            val timestamp = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US).format(Date())
            val safeMessage = scrubPii(message)
            
            val logEntry = "[$timestamp] [$category] $safeMessage\n"
            file.appendText(logEntry)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun exportLogs(context: Context): String {
        return try {
            val file = File(context.filesDir, LOG_FILE_NAME)
            if (file.exists()) {
                "```text\n${file.readText()}\n```"
            } else {
                "No proxy diagnostics found."
            }
        } catch (e: Exception) {
            "Failed to read logs: ${e.message}"
        }
    }

    private fun scrubPii(message: String): String {
        // Redact standard IP addresses
        var scrubbed = message.replace(Regex("\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"), "[IP_REDACTED]")
        // Redact Xtream codes credentials (username/password)
        scrubbed = scrubbed.replace(Regex("username=[^&]+"), "username=[REDACTED]")
        scrubbed = scrubbed.replace(Regex("password=[^&]+"), "password=[REDACTED]")
        return scrubbed
    }
}
