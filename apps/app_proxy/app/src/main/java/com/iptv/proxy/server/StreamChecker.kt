package com.iptv.proxy.server

import kotlinx.coroutines.*
import kotlinx.coroutines.channels.Channel
import okhttp3.OkHttpClient
import okhttp3.Request
import java.util.concurrent.TimeUnit

class StreamChecker {

    // Aggressive timeout under 2 seconds to prevent buffering on the external player
    private val client = OkHttpClient.Builder()
        .connectTimeout(1500, TimeUnit.MILLISECONDS)
        .readTimeout(1500, TimeUnit.MILLISECONDS)
        .build()

    /**
     * Rapidly pings multiple fallback URLs concurrently.
     * Returns the first URL that responds with an HTTP 2xx or 3xx status instantly.
     */
    suspend fun findFastestAliveStream(urls: List<String>): String? = coroutineScope {
        if (urls.isEmpty()) return@coroutineScope null
        if (urls.size == 1) return@coroutineScope urls.first() // Fast path

        val resultChannel = Channel<String?>(Channel.CONFLATED)

        // Launch all checks concurrently
        val jobs = urls.map { url ->
            launch(Dispatchers.IO) {
                val isAlive = checkUrl(url)
                if (isAlive != null) {
                    // Instantly push the first successful result
                    resultChannel.trySend(isAlive)
                }
            }
        }

        // A fallback coroutine to close the channel when all jobs finish failing
        launch {
            jobs.joinAll()
            resultChannel.trySend(null)
        }

        // Wait for the absolutely first message in the channel
        val fastestUrl = resultChannel.receive()

        // Cancel all pending network requests since we already found a winner
        coroutineContext.cancelChildren()

        return@coroutineScope fastestUrl
    }

    private fun checkUrl(url: String): String? {
        return try {
            // Using HEAD request to save bandwidth (doesn't download the video stream)
            val request = Request.Builder()
                .url(url)
                .head()
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful || response.isRedirect) {
                    url
                } else {
                    null
                }
            }
        } catch (e: Exception) {
            null
        }
    }
}
