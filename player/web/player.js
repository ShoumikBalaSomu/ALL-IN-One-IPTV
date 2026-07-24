document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video-player');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const muteBtn = document.getElementById('mute-btn');
    const volumeSlider = document.getElementById('volume-slider');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const pipBtn = document.getElementById('pip-btn');
    const channelList = document.getElementById('channel-list');
    const searchInput = document.getElementById('channel-search');
    
    let hls = null;
    let currentChannelIndex = 0;

    // Mock channel data
    const channels = [
        { name: "News 24 Live", url: "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", tags: ["HD", "News"] },
        { name: "Sports Extra", url: "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", tags: ["4K", "Sports"] },
        { name: "Movie Classics", url: "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", tags: ["FHD", "Movies"] },
        { name: "Nature Doc", url: "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", tags: ["HD", "Doc"] },
    ];

    function renderChannels(filter = '') {
        channelList.innerHTML = '';
        channels.forEach((ch, index) => {
            if (ch.name.toLowerCase().includes(filter.toLowerCase())) {
                const li = document.createElement('li');
                li.className = `channel-item ${index === currentChannelIndex ? 'active' : ''}`;
                li.innerHTML = `
                    <div class="channel-info">
                        <span class="channel-name">${ch.name}</span>
                        <div class="channel-tags">
                            ${ch.tags.map(t => `<span class="tag">${t}</span>`).join('')}
                        </div>
                    </div>
                    <span>⭐</span>
                `;
                li.addEventListener('click', () => loadChannel(index));
                channelList.appendChild(li);
            }
        });
    }

    function loadChannel(index) {
        currentChannelIndex = index;
        const channel = channels[index];
        renderChannels(searchInput.value);
        
        if (Hls.isSupported()) {
            if (hls) hls.destroy();
            hls = new Hls();
            hls.loadSource(channel.url);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, () => {
                video.play();
                playPauseBtn.innerText = '⏸';
            });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = channel.url;
            video.addEventListener('loadedmetadata', () => {
                video.play();
                playPauseBtn.innerText = '⏸';
            });
        }
        
        // Mock EPG Update
        document.getElementById('epg-title').innerText = `Current Show on ${channel.name}`;
        document.getElementById('epg-time').innerText = `12:00 PM - 2:00 PM`;
        document.getElementById('epg-progress').style.width = `${Math.random() * 100}%`;
    }

    searchInput.addEventListener('input', (e) => renderChannels(e.target.value));

    // Controls
    playPauseBtn.addEventListener('click', () => {
        if (video.paused) {
            video.play();
            playPauseBtn.innerText = '⏸';
        } else {
            video.pause();
            playPauseBtn.innerText = '▶';
        }
    });

    muteBtn.addEventListener('click', () => {
        video.muted = !video.muted;
        muteBtn.innerText = video.muted ? '🔇' : '🔊';
        if (video.muted) volumeSlider.value = 0;
        else volumeSlider.value = 1;
    });

    volumeSlider.addEventListener('input', (e) => {
        video.volume = e.target.value;
        if (video.volume > 0) {
            video.muted = false;
            muteBtn.innerText = '🔊';
        } else {
            video.muted = true;
            muteBtn.innerText = '🔇';
        }
    });

    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.getElementById('video-container').requestFullscreen().catch(err => {
                console.error(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    });

    pipBtn.addEventListener('click', async () => {
        if (document.pictureInPictureElement) {
            await document.exitPictureInPicture();
        } else {
            if (document.pictureInPictureEnabled) {
                await video.requestPictureInPicture();
            }
        }
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        // Only if not typing in search
        if (document.activeElement === searchInput) return;
        
        switch(e.key.toLowerCase()) {
            case ' ':
                e.preventDefault();
                playPauseBtn.click();
                break;
            case 'f':
                fullscreenBtn.click();
                break;
            case 'm':
                muteBtn.click();
                break;
            case 'arrowup':
                e.preventDefault();
                if (currentChannelIndex > 0) loadChannel(currentChannelIndex - 1);
                break;
            case 'arrowdown':
                e.preventDefault();
                if (currentChannelIndex < channels.length - 1) loadChannel(currentChannelIndex + 1);
                break;
        }
    });

    // Init
    renderChannels();
    if (channels.length > 0) loadChannel(0);
});
