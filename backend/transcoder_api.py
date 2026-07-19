from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI(title="Transcoding Farm Orchestrator")

# Store active FFmpeg processes (StreamID -> Popen)
active_transcodes = {}

@app.get("/transcode/{channel_id}")
def start_transcode(channel_id: str, source_url: str):
    if channel_id in active_transcodes:
        return {"status": "already running", "playlist": f"/output/{channel_id}.m3u8"}

    # Dynamic NVENC FFmpeg command for 720p fallback
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", source_url,
        "-c:v", "h264_nvenc", "-preset", "p6", "-b:v", "2000k", "-maxrate", "2500k",
        "-bufsize", "5000k", "-vf", "scale=1280:720",
        "-c:a", "aac", "-b:a", "128k",
        "-f", "hls", "-hls_time", "4", "-hls_list_size", "5",
        "-hls_flags", "delete_segments",
        f"/app/output/{channel_id}.m3u8"
    ]

    try:
        os.makedirs("/app/output", exist_ok=True)
        # Spin up FFmpeg in the background
        process = subprocess.Popen(ffmpeg_cmd)
        active_transcodes[channel_id] = process
        
        return {"status": "started", "playlist": f"/output/{channel_id}.m3u8"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stop/{channel_id}")
def stop_transcode(channel_id: str):
    if channel_id in active_transcodes:
        active_transcodes[channel_id].terminate()
        del active_transcodes[channel_id]
        return {"status": "stopped"}
    return {"status": "not running"}
