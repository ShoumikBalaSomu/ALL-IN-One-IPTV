// Particle Background
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');
let particles = [];

function initCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    particles = [];
    for (let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 0.5,
            speedY: Math.random() * 1 + 0.2,
            speedX: (Math.random() - 0.5) * 0.5
        });
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
    particles.forEach(p => {
        p.y -= p.speedY;
        p.x += p.speedX;
        if (p.y < 0) {
            p.y = canvas.height;
            p.x = Math.random() * canvas.width;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
    });
    requestAnimationFrame(animateParticles);
}

window.addEventListener('resize', initCanvas);
initCanvas();
animateParticles();

// IPTV Logic
const M3U_URL = 'https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u';
let allChannels = [];
let currentFilter = 'All';
let hls = null;

const video = document.getElementById('videoPlayer');
const videoOverlay = document.getElementById('videoOverlay');
const npLogo = document.getElementById('npLogo');
const npTitle = document.getElementById('npTitle');
const channelGrid = document.getElementById('channelGrid');
const categoryList = document.getElementById('categoryList');
const currentGroupName = document.getElementById('currentGroupName');
const channelCount = document.getElementById('channelCount');
const searchInput = document.getElementById('searchInput');

async function loadPlaylist() {
    try {
        const response = await fetch(M3U_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        const text = await response.text();
        parseM3U(text);
    } catch (error) {
        console.error('Failed to load playlist:', error);
        channelCount.textContent = 'Failed to load channels';
    }
}

function parseM3U(data) {
    const lines = data.split('\n');
    let currentChannel = {};
    const groups = new Set();

    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('#EXTINF:')) {
            // Extract logo
            const logoMatch = line.match(/tvg-logo="([^"]+)"/);
            currentChannel.logo = logoMatch ? logoMatch[1] : '';
            
            // Extract group
            const groupMatch = line.match(/group-title="([^"]+)"/);
            const group = groupMatch ? groupMatch[1] : 'Uncategorized';
            currentChannel.group = group;
            groups.add(group);
            
            // Extract name
            const nameSplit = line.split(',');
            currentChannel.name = nameSplit.length > 1 ? nameSplit[1].trim() : 'Unknown Channel';
        } else if (line.startsWith('http')) {
            currentChannel.url = line;
            allChannels.push(currentChannel);
            currentChannel = {}; // Reset for next
        }
    }

    renderGroups(Array.from(groups).sort());
    renderChannels(allChannels);
}

function renderGroups(groups) {
    groups.forEach(group => {
        const li = document.createElement('li');
        li.textContent = group;
        li.dataset.group = group;
        li.addEventListener('click', () => {
            document.querySelectorAll('.category-list li').forEach(el => el.classList.remove('active'));
            li.classList.add('active');
            currentFilter = group;
            currentGroupName.textContent = group;
            filterAndRender();
        });
        categoryList.appendChild(li);
    });
}

function renderChannels(channels) {
    channelGrid.innerHTML = '';
    channelCount.textContent = `${channels.length} Channels`;

    channels.forEach((ch, index) => {
        const card = document.createElement('div');
        card.className = 'channel-card';
        card.onclick = () => playChannel(ch, card);

        const logoHtml = ch.logo 
            ? `<img src="${ch.logo}" onerror="this.outerHTML='<i class=\\'fas fa-tv\\'></i>'">` 
            : `<i class="fas fa-tv"></i>`;

        card.innerHTML = `
            <div class="channel-logo">${logoHtml}</div>
            <div class="channel-info">
                <div class="channel-name">${ch.name}</div>
                <div class="channel-group">${ch.group}</div>
            </div>
            <i class="fas fa-volume-up playing-icon"></i>
        `;
        channelGrid.appendChild(card);
    });
}

function filterAndRender() {
    const query = searchInput.value.toLowerCase();
    const filtered = allChannels.filter(ch => {
        const matchesGroup = currentFilter === 'All' || ch.group === currentFilter;
        const matchesSearch = ch.name.toLowerCase().includes(query);
        return matchesGroup && matchesSearch;
    });
    renderChannels(filtered);
}

function playChannel(channel, cardElement) {
    // UI Updates
    document.querySelectorAll('.channel-card').forEach(c => c.classList.remove('playing'));
    if (cardElement) cardElement.classList.add('playing');
    
    videoOverlay.style.display = 'none';
    npTitle.textContent = channel.name;
    if (channel.logo) {
        npLogo.src = channel.logo;
        npLogo.style.display = 'block';
    } else {
        npLogo.style.display = 'none';
    }

    // Video Playback Logic
    if (Hls.isSupported()) {
        if (hls) hls.destroy();
        hls = new Hls();
        hls.loadSource(channel.url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
            video.play().catch(e => console.log('Autoplay prevented', e));
        });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // For Safari
        video.src = channel.url;
        video.addEventListener('loadedmetadata', () => {
            video.play().catch(e => console.log('Autoplay prevented', e));
        });
    } else {
        alert("Your browser doesn't support HLS video playback.");
    }
}

// Search Listener
searchInput.addEventListener('input', filterAndRender);
document.querySelector('[data-group="All"]').addEventListener('click', function() {
    document.querySelectorAll('.category-list li').forEach(el => el.classList.remove('active'));
    this.classList.add('active');
    currentFilter = 'All';
    currentGroupName.textContent = 'All Channels';
    filterAndRender();
});

// Init
loadPlaylist();
