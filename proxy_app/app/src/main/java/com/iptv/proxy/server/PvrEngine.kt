package com.iptv.proxy.server

import kotlinx.coroutines.*
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL

class PvrEngine(private val storageDir: File) {

    private val recordingJobs = mutableMapOf<String, Job>()

    /**
     * Start a background recording of a raw HLS/TS stream and pipe it to disk.
     */
    fun startRecording(channelId: String, streamUrl: String, durationMinutes: Int) {
        if (recordingJobs.containsKey(channelId)) return

        val job = CoroutineScope(Dispatchers.IO).launch {
            try {
                val outputFile = File(storageDir, "${channelId}_${System.currentTimeMillis()}.ts")
                val outputStream = FileOutputStream(outputFile)
                
                println("PVR: Started recording $channelId to ${outputFile.absolutePath}")

                val connection = URL(streamUrl).openConnection() as HttpURLConnection
                connection.connectTimeout = 5000
                connection.readTimeout = 5000
                val inputStream: InputStream = connection.inputStream

                val endTime = System.currentTimeMillis() + (durationMinutes * 60 * 1000)
                val buffer = ByteArray(8192)
                var bytesRead: Int

                // Stream slicing: Continuously read and write chunks until duration is met
                while (System.currentTimeMillis() < endTime && isActive) {
                    bytesRead = inputStream.read(buffer)
                    if (bytesRead == -1) break
                    outputStream.write(buffer, 0, bytesRead)
                }

                outputStream.close()
                inputStream.close()
                println("PVR: Finished recording $channelId")
            } catch (e: Exception) {
                println("PVR: Recording failed for $channelId - ${e.message}")
            } finally {
                recordingJobs.remove(channelId)
            }
        }

        recordingJobs[channelId] = job
    }

    fun stopRecording(channelId: String) {
        recordingJobs[channelId]?.cancel()
        recordingJobs.remove(channelId)
    }
}
