package com.iptv.proxy.server

import android.content.Context
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.HttpStatusCode
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class LocalKtorServer(private val context: Context) {

    private var server: NettyApplicationEngine? = null
    private val streamChecker = StreamChecker()

    fun start() {
        server = embeddedServer(Netty, port = 8080, host = "127.0.0.1") {
            routing {
                
                // Expose dynamic M3U playlists pointing to the proxy
                get("/live.m3u") {
                    val m3uContent = generateLocalM3u()
                    call.respondText(m3uContent, io.ktor.http.ContentType.Text.Plain)
                }

                get("/master.m3u") {
                    val m3uContent = generateLocalM3u()
                    call.respondText(m3uContent, io.ktor.http.ContentType.Text.Plain)
                }

                // Intercept the stream request, ping fallbacks, and redirect to winner
                get("/play/{channelId}") {
                    val channelId = call.parameters["channelId"]
                    if (channelId != null) {
                        // Mocking folded streams (in production this queries Room DB)
                        val fallbackUrls = listOf(
                            "http://example.com/dead_stream.m3u8",
                            "http://202.70.146.135:8000/playlist.m3u", // Mock alive stream
                            "http://example.com/another_dead.ts"
                        )

                        // 1. Run concurrent fast HTTP HEAD pings
                        val fastestAliveUrl = streamChecker.findFastestAliveStream(fallbackUrls)

                        if (fastestAliveUrl != null) {
                            // 2. Instantly redirect the external player to the healthy stream
                            call.respondRedirect(fastestAliveUrl, permanent = false)
                        } else {
                            // 3. Fallback exhausted
                            call.respond(HttpStatusCode.NotFound, "All fallback streams are dead.")
                        }
                    } else {
                        call.respond(HttpStatusCode.BadRequest, "Missing channelId")
                    }
                }
            }
        }.start(wait = true)
    }

    fun stop() {
        server?.stop(1000, 2000)
    }

    private suspend fun generateLocalM3u(): String = withContext(Dispatchers.IO) {
        // Query Room DB for folded channels and generate M3U on the fly
        // Each channel's URL is transformed to point to the local proxy
        """
        #EXTM3U
        #EXTINF:-1 tvg-id="test" tvg-logo="test.png" group-title="Test",Proxy Channel 1
        http://127.0.0.1:8080/play/channel_1
        """.trimIndent()
    }
}
