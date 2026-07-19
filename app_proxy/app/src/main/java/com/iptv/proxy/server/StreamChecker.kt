package com.iptv.proxy.server

import kotlinx.coroutines.*
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
     * Returns the first URL that responds with an HTTP 2xx or 3xx status.
     */
    suspend fun findFastestAliveStream(urls: List<String>): String? = coroutineScope {
        if (urls.isEmpty()) return@coroutineScope null
        if (urls.size == 1) return@coroutineScope urls.first() // Fast path

        val deferredResults = urls.map { url ->
            async(Dispatchers.IO) {
                checkUrl(url)
            }
        }

        // Wait for the fastest successful response, ignoring failures until all finish
        for (deferred in deferredResults) {
            val resultUrl = deferred.await()
            if (resultUrl != null) {
                // Cancel remaining requests to save bandwidth and battery
                coroutineContext.cancelChildren()
                return@coroutineScope resultUrl
            }
        }

        // All failed
        null
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
