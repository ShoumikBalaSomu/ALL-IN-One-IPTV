const video = document.getElementById('video');
const channelList = document.getElementById('channelList');
const search = document.getElementById('search');
let hls;

// Mock channels data
const channels = [
    { name: 'Red Bull TV', category: 'Sports', url: 'https://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master.m3u8', logo: 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Red_Bull_TV_logo.svg/1200px-Red_Bull_TV_logo.svg.png' },
    { name: 'NASA TV', category: 'Science', url: 'https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8', logo: 'https://upload.wikimedia.org/wikipedia/commons/e/e5/NASA_logo.svg' }
];

function loadChannel(channel) {
    document.getElementById('currentChannelName').textContent = channel.name;
    document.getElementById('currentCategory').textContent = channel.category;
    
    if (Hls.isSupported()) {
        if (hls) hls.destroy();
        hls = new Hls();
        hls.loadSource(channel.url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = channel.url;
        video.addEventListener('loadedmetadata', () => video.play());
    }
}

function renderChannels(list) {
    channelList.innerHTML = list.map(ch => `
        <div class="channel-item" onclick="loadChannel({name: '${ch.name}', category: '${ch.category}', url: '${ch.url}'})">
            <img src="${ch.logo}" class="channel-icon" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iIzMzMyIvPjwvc3ZnPg=='">
            <div>
                <div style="font-weight: 500">${ch.name}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted)">${ch.category}</div>
            </div>
        </div>
    `).join('');
}

search.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    renderChannels(channels.filter(c => c.name.toLowerCase().includes(q)));
});

// Controls
document.getElementById('btnPip').onclick = () => {
    if (document.pictureInPictureElement) {
        document.exitPictureInPicture();
    } else {
        video.requestPictureInPicture();
    }
};

document.getElementById('btnFull').onclick = () => {
    if (!document.fullscreenElement) {
        video.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
};

document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        video.paused ? video.play() : video.pause();
    } else if (e.code === 'KeyF') {
        document.getElementById('btnFull').click();
    }
});

// Init
renderChannels(channels);
if(channels.length > 0) loadChannel(channels[0]);
