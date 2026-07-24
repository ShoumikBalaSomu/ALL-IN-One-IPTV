package com.iptv.proxy.server

import java.net.InetAddress
import javax.jmdns.JmDNS
import javax.jmdns.ServiceInfo
import kotlinx.coroutines.*

class LanMeshRouter {
    
    private var jmdns: JmDNS? = null
    private val activeStreams = mutableMapOf<String, String>() // ChannelID -> Master Node IP
    private val localIp: String = InetAddress.getLocalHost().hostAddress ?: "127.0.0.1"

    fun initializeDiscovery() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Bind to local loopback/network interface
                jmdns = JmDNS.create(InetAddress.getLocalHost())
                
                // Broadcast that this node exists on the network
                val serviceInfo = ServiceInfo.create(
                    "_iptvmesh._tcp.local.", 
                    "IPTV_Proxy_${localIp}", 
                    8080, 
                    "Local P2P Stream Relay Node"
                )
                jmdns?.registerService(serviceInfo)
                
                println("LAN Mesh Router initialized on $localIp:8080")
            } catch (e: Exception) {
                println("Failed to initialize JmDNS: ${e.message}")
            }
        }
    }

    /**
     * Called when the Proxy receives a request for a stream.
     * Determines if we should fetch from WAN, or relay from a LAN peer.
     */
    fun routeStreamRequest(channelId: String, wanUrl: String): String {
        // 1. Check if another node on the LAN is already streaming this channel
        val masterNodeIp = activeStreams[channelId]
        
        if (masterNodeIp != null && masterNodeIp != localIp) {
            println("LAN Mesh: Redirecting request to Master Node -> $masterNodeIp")
            // Rewrite the URL to pull from the peer's local proxy port
            return "http://$masterNodeIp:8080/relay/$channelId"
        }

        // 2. We are the first to request it. Become the Master Node for this stream.
        println("LAN Mesh: Claiming Master Node status for $channelId. Fetching via WAN.")
        broadcastMasterStatus(channelId)
        
        return wanUrl
    }

    private fun broadcastMasterStatus(channelId: String) {
        // In a real implementation, this would update TXT records in JmDNS 
        // or multicast a UDP packet to notify peers that this IP owns the stream.
        activeStreams[channelId] = localIp
    }

    fun shutdown() {
        jmdns?.unregisterAllServices()
        jmdns?.close()
    }
}
