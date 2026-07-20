// ==========================================
// SPA NAVIGATION LOGIC
// ==========================================
function switchView(viewId) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
    if (viewId === 'view-vod') setupVOD();
}

// ==========================================
// PARTICLE BACKGROUND
// ==========================================
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
        p.y -= p.speedY; p.x += p.speedX;
        if (p.y < 0) { p.y = canvas.height; p.x = Math.random() * canvas.width; }
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
    });
    requestAnimationFrame(animateParticles);
}
window.addEventListener('resize', initCanvas);
initCanvas();
animateParticles();

// ==========================================
// STATE MANAGEMENT (Favorites & Parental)
// ==========================================
const SYSTEM_PIN = "0171";
let favorites = JSON.parse(localStorage.getItem('nexus_favorites')) || [];
let unlockedAdult = false;
let pendingCategory = null;

function toggleFavorite(url) {
    if (favorites.includes(url)) {
        favorites = favorites.filter(u => u !== url);
    } else {
        favorites.push(url);
    }
    localStorage.setItem('nexus_favorites', JSON.stringify(favorites));
}

function isAdultGroup(group) {
    const g = group.toLowerCase();
    return g.includes('xxx') || g.includes('adult') || g.includes('18+');
}

// ==========================================
// LIVE TV EXPLORER (M3U Parser & HLS)
// ==========================================
const M3U_URL = 'https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u';
let allChannels = [];
let currentFilter = 'All';
let currentPlayingChannel = null;
let hls = null;

const tvVideo = document.getElementById('tvVideo');
const tvChannelList = document.getElementById('tvChannelList');
const tvCategories = document.getElementById('tvCategories');
const pinModal = document.getElementById('pinModal');
const pinInput = document.getElementById('pinInput');

async function loadLiveTV() {
    try {
        const response = await fetch(M3U_URL);
        if (!response.ok) throw new Error('Network response was not ok');
        const text = await response.text();
        parseM3U(text);
    } catch (e) {
        tvChannelList.innerHTML = '<div style="padding:20px;color:red;">Failed to load M3U archive.</div>';
    }
}

function parseM3U(data) {
    const lines = data.split('\n');
    let ch = {};
    const groups = new Set();
    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('#EXTINF:')) {
            const logoMatch = line.match(/tvg-logo="([^"]+)"/);
            ch.logo = logoMatch ? logoMatch[1] : '';
            const groupMatch = line.match(/group-title="([^"]+)"/);
            ch.group = groupMatch ? groupMatch[1] : 'Uncategorized';
            groups.add(ch.group);
            const nameSplit = line.split(',');
            ch.name = nameSplit.length > 1 ? nameSplit[1].trim() : 'Unknown';
        } else if (line.startsWith('http')) {
            ch.url = line;
            allChannels.push(ch);
            ch = {};
        }
    }
    renderCategories(Array.from(groups).sort());
    filterTvChannels();
}

function renderCategories(groups) {
    tvCategories.innerHTML = '';
    
    // Inject Favorites hardcoded first
    const favCat = document.createElement('div');
    favCat.className = 'cat-item';
    favCat.dataset.group = 'Favorites';
    favCat.innerHTML = `<i class="fas fa-heart" style="color:#FF0055;"></i> Favorites`;
    tvCategories.appendChild(favCat);

    groups.forEach(g => {
        const icon = isAdultGroup(g) ? '<i class="fas fa-lock" style="color:#E50914;"></i>' : '<i class="fas fa-folder"></i>';
        tvCategories.innerHTML += `<div class="cat-item" data-group="${g}">${icon} ${g}</div>`;
    });
    
    document.querySelectorAll('.cat-item').forEach(item => {
        item.addEventListener('click', () => {
            const groupName = item.dataset.group;
            
            // Check Parental Controls
            if (isAdultGroup(groupName) && !unlockedAdult) {
                pendingCategory = groupName;
                pinInput.value = '';
                document.getElementById('pinError').style.display = 'none';
                pinModal.classList.add('active');
                pinInput.focus();
                return;
            }

            document.querySelectorAll('.cat-item').forEach(el => el.classList.remove('active'));
            item.classList.add('active');
            currentFilter = groupName;
            document.getElementById('tvCurrentGroup').textContent = currentFilter.toUpperCase();
            filterTvChannels();
        });
    });
}

function filterTvChannels() {
    const query = document.getElementById('tvSearchInput').value.toLowerCase();
    
    let filtered = allChannels;
    if (currentFilter === 'Favorites') {
        filtered = allChannels.filter(ch => favorites.includes(ch.url));
    } else if (currentFilter !== 'All') {
        filtered = allChannels.filter(ch => ch.group === currentFilter);
    }
    
    filtered = filtered.filter(ch => ch.name.toLowerCase().includes(query));
    
    // If we are on All channels, still hide adult channels unless unlocked
    if (currentFilter === 'All' && !unlockedAdult) {
        filtered = filtered.filter(ch => !isAdultGroup(ch.group));
    }

    renderTvChannels(filtered);
}

document.getElementById('tvSearchInput').addEventListener('input', filterTvChannels);

function renderTvChannels(channels) {
    tvChannelList.innerHTML = '';
    if (channels.length === 0) {
        tvChannelList.innerHTML = '<div style="padding:20px;color:#666;">No channels found.</div>';
        return;
    }
    channels.forEach((ch, idx) => {
        const row = document.createElement('div');
        row.className = 'ch-row';
        if (currentPlayingChannel && currentPlayingChannel.url === ch.url) {
            row.classList.add('active');
        }
        row.onclick = () => playTvChannel(ch, row);
        
        const isFav = favorites.includes(ch.url);
        row.innerHTML = `
            <span class="ch-num">${String(idx + 1).padStart(3, '0')}</span>
            <img src="${ch.logo}" class="ch-logo" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\'><rect width=\\'100\\' height=\\'100\\' fill=\\'white\\'/></svg>'">
            <div class="ch-info">
                <h4>${ch.name}</h4>
                <p>${ch.group}</p>
            </div>
            ${isFav ? '<i class="fas fa-heart" style="color:#FF0055; margin-right: 12px;"></i>' : ''}
            <i class="fas fa-volume-up" style="display:${currentPlayingChannel && currentPlayingChannel.url === ch.url ? 'block' : 'none'}; color:#00FF7F;"></i>
        `;
        tvChannelList.appendChild(row);
    });
}

function playTvChannel(channel, rowEl) {
    currentPlayingChannel = channel;
    
    document.querySelectorAll('.ch-row').forEach(r => {
        r.classList.remove('active');
        const vol = r.querySelector('.fa-volume-up');
        if(vol) vol.style.display = 'none';
    });
    rowEl.classList.add('active');
    const vol = rowEl.querySelector('.fa-volume-up');
    if(vol) vol.style.display = 'block';

    document.getElementById('tvOverlay').style.display = 'none';
    document.getElementById('epgTitle').textContent = channel.name;
    document.getElementById('epgGroup').textContent = channel.group;

    // Update Favorite Button State
    updateFavButtonState();

    if (Hls.isSupported()) {
        if (hls) hls.destroy();
        hls = new Hls();
        hls.loadSource(channel.url);
        hls.attachMedia(tvVideo);
        hls.on(Hls.Events.MANIFEST_PARSED, () => tvVideo.play().catch(e=>console.log(e)));
    } else if (tvVideo.canPlayType('application/vnd.apple.mpegurl')) {
        tvVideo.src = channel.url;
        tvVideo.addEventListener('loadedmetadata', () => tvVideo.play().catch(e=>console.log(e)));
    }
}

// ==========================================
// VIDEO CONTROLS (PiP & Fav)
// ==========================================
const btnFavVideo = document.getElementById('btnFavVideo');
const favIcon = document.getElementById('favIcon');
const btnPip = document.getElementById('btnPip');

function updateFavButtonState() {
    if (!currentPlayingChannel) return;
    const isFav = favorites.includes(currentPlayingChannel.url);
    if (isFav) {
        btnFavVideo.classList.add('active-fav');
        favIcon.className = 'fas fa-heart';
    } else {
        btnFavVideo.classList.remove('active-fav');
        favIcon.className = 'far fa-heart';
    }
}

btnFavVideo.addEventListener('click', () => {
    if (!currentPlayingChannel) return;
    toggleFavorite(currentPlayingChannel.url);
    updateFavButtonState();
    filterTvChannels(); // re-render list to show heart
});

btnPip.addEventListener('click', async () => {
    try {
        if (tvVideo !== document.pictureInPictureElement) {
            await tvVideo.requestPictureInPicture();
        } else {
            await document.exitPictureInPicture();
        }
    } catch (error) {
        alert("Picture-in-Picture is not supported in this browser.");
    }
});

// ==========================================
// PARENTAL CONTROL LOGIC
// ==========================================
document.getElementById('btnPinCancel').addEventListener('click', () => {
    pinModal.classList.remove('active');
    pendingCategory = null;
});

document.getElementById('btnPinSubmit').addEventListener('click', () => {
    if (pinInput.value === SYSTEM_PIN) {
        unlockedAdult = true;
        pinModal.classList.remove('active');
        
        // Select the pending category
        if (pendingCategory) {
            document.querySelectorAll('.cat-item').forEach(el => {
                el.classList.remove('active');
                if (el.dataset.group === pendingCategory) el.classList.add('active');
            });
            currentFilter = pendingCategory;
            document.getElementById('tvCurrentGroup').textContent = currentFilter.toUpperCase();
            filterTvChannels();
            pendingCategory = null;
        }
    } else {
        document.getElementById('pinError').style.display = 'block';
    }
});

// ==========================================
// VOD CINEMA & PROXY DASHBOARD (Truncated for brevity but functional)
// ==========================================
let vodSetupDone = false;
function setupVOD() {
    if (vodSetupDone) return;
    vodSetupDone = true;
    const scrollEl = document.getElementById('vodScroll');
    const appbar = document.getElementById('vodAppbar');
    scrollEl.addEventListener('scroll', () => {
        if (scrollEl.scrollTop > 50) appbar.classList.add('scrolled');
        else appbar.classList.remove('scrolled');
    });

    const generateItems = (count, isTop10 = false) => {
        let html = '';
        for(let i=0; i<count; i++) {
            const seed = Math.floor(Math.random() * 1000);
            html += `<div class="carousel-item" style="background-image: url('https://picsum.photos/300/450?random=${seed}')">`;
            if (isTop10) html += `<div class="t10-num">${i + 1}</div>`;
            html += `</div>`;
        }
        return html;
    };
    document.getElementById('carouselTrending').innerHTML = generateItems(10);
}

// Proxy Reactor code
const rCanvas = document.getElementById('reactorCanvas');
const rCtx = rCanvas.getContext('2d');
let proxyActive = false;
let reactorAngle = 0;
function drawReactor() {
    rCanvas.width = 280; rCanvas.height = 280;
    rCtx.clearRect(0, 0, rCanvas.width, rCanvas.height);
    const cx = rCanvas.width/2; const cy = rCanvas.height/2; const r = 120;
    rCtx.beginPath(); rCtx.arc(cx, cy, r, 0, Math.PI*2);
    rCtx.strokeStyle = 'rgba(255,255,255,0.05)'; rCtx.lineWidth = 2; rCtx.stroke();
    rCtx.save(); rCtx.translate(cx, cy); rCtx.rotate(reactorAngle);
    rCtx.beginPath(); rCtx.arc(0, 0, r - 16, 0, Math.PI * 1.5);
    rCtx.strokeStyle = proxyActive ? '#00E5FF' : '#FF0055'; rCtx.lineWidth = 10;
    rCtx.setLineDash([40, 20]); rCtx.lineCap = 'round'; rCtx.stroke(); rCtx.restore();
    reactorAngle += proxyActive ? 0.05 : 0.01;
    requestAnimationFrame(drawReactor);
}
drawReactor();
document.getElementById('btnEngageProxy').addEventListener('click', function() {
    proxyActive = !proxyActive;
    this.classList.toggle('active');
    document.getElementById('proxyStatusIcon').style.color = proxyActive ? '#00E5FF' : '#FF0055';
});

// Init
loadLiveTV();
