// ==========================================
// SPA NAVIGATION LOGIC
// ==========================================
function switchView(viewId) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
    
    // Trigger specific view setups
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
// LIVE TV EXPLORER (M3U Parser & HLS)
// ==========================================
const M3U_URL = 'https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u';
let allChannels = [];
let currentFilter = 'All';
let hls = null;

const tvVideo = document.getElementById('tvVideo');
const tvChannelList = document.getElementById('tvChannelList');
const tvCategories = document.getElementById('tvCategories');

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
    renderTvChannels(allChannels);
}

function renderCategories(groups) {
    tvCategories.innerHTML = `<div class="cat-item active" data-group="All"><i class="fas fa-border-all"></i> All Channels</div>`;
    groups.forEach(g => {
        tvCategories.innerHTML += `<div class="cat-item" data-group="${g}"><i class="fas fa-folder"></i> ${g}</div>`;
    });
    
    document.querySelectorAll('.cat-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.cat-item').forEach(el => el.classList.remove('active'));
            item.classList.add('active');
            currentFilter = item.dataset.group;
            document.getElementById('tvCurrentGroup').textContent = currentFilter.toUpperCase();
            filterTvChannels();
        });
    });
}

function renderTvChannels(channels) {
    tvChannelList.innerHTML = '';
    channels.forEach((ch, idx) => {
        const row = document.createElement('div');
        row.className = 'ch-row';
        row.onclick = () => playTvChannel(ch, row);
        row.innerHTML = `
            <span class="ch-num">${String(idx + 1).padStart(3, '0')}</span>
            <img src="${ch.logo}" class="ch-logo" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\'><rect width=\\'100\\' height=\\'100\\' fill=\\'white\\'/></svg>'">
            <div class="ch-info">
                <h4>${ch.name}</h4>
                <p>${ch.group}</p>
            </div>
            <i class="fas fa-volume-up" style="display:none; color:#00FF7F;"></i>
        `;
        tvChannelList.appendChild(row);
    });
}

function filterTvChannels() {
    const query = document.getElementById('tvSearchInput').value.toLowerCase();
    const filtered = allChannels.filter(ch => {
        const mg = currentFilter === 'All' || ch.group === currentFilter;
        const ms = ch.name.toLowerCase().includes(query);
        return mg && ms;
    });
    renderTvChannels(filtered);
}

document.getElementById('tvSearchInput').addEventListener('input', filterTvChannels);

function playTvChannel(channel, rowEl) {
    document.querySelectorAll('.ch-row').forEach(r => {
        r.classList.remove('active');
        r.querySelector('.fa-volume-up').style.display = 'none';
    });
    rowEl.classList.add('active');
    rowEl.querySelector('.fa-volume-up').style.display = 'block';

    document.getElementById('tvOverlay').style.display = 'none';
    document.getElementById('epgTitle').textContent = channel.name;
    document.getElementById('epgGroup').textContent = channel.group;

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
// VOD CINEMA LOGIC
// ==========================================
let vodSetupDone = false;
function setupVOD() {
    if (vodSetupDone) return;
    vodSetupDone = true;

    // Scroll Blur Effect
    const scrollEl = document.getElementById('vodScroll');
    const appbar = document.getElementById('vodAppbar');
    scrollEl.addEventListener('scroll', () => {
        if (scrollEl.scrollTop > 50) appbar.classList.add('scrolled');
        else appbar.classList.remove('scrolled');
    });

    // Populate Mock Data
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
    document.getElementById('carouselTop10').innerHTML = generateItems(10, true);
    document.getElementById('carouselAction').innerHTML = generateItems(10);
}

// ==========================================
// PROXY DASHBOARD LOGIC (Canvas Reactor)
// ==========================================
const rCanvas = document.getElementById('reactorCanvas');
const rCtx = rCanvas.getContext('2d');
let proxyActive = false;
let reactorAngle = 0;
let bwSimInterval;

function drawReactor() {
    rCanvas.width = 280; rCanvas.height = 280;
    rCtx.clearRect(0, 0, rCanvas.width, rCanvas.height);
    const cx = rCanvas.width/2; const cy = rCanvas.height/2; const r = 120;
    
    // Outer static ring
    rCtx.beginPath(); rCtx.arc(cx, cy, r, 0, Math.PI*2);
    rCtx.strokeStyle = 'rgba(255,255,255,0.05)'; rCtx.lineWidth = 2; rCtx.stroke();
    
    // Rotating dashed ring
    rCtx.save();
    rCtx.translate(cx, cy);
    rCtx.rotate(reactorAngle);
    rCtx.beginPath(); rCtx.arc(0, 0, r - 16, 0, Math.PI * 1.5);
    rCtx.strokeStyle = proxyActive ? '#00E5FF' : '#FF0055';
    rCtx.lineWidth = 10;
    rCtx.setLineDash([40, 20]);
    rCtx.lineCap = 'round';
    rCtx.stroke();
    rCtx.restore();
    
    // Core glow
    const grad = rCtx.createRadialGradient(cx, cy, 0, cx, cy, r*0.7);
    grad.addColorStop(0, proxyActive ? 'rgba(0,229,255,0.4)' : 'rgba(255,0,85,0.2)');
    grad.addColorStop(1, 'transparent');
    rCtx.fillStyle = grad;
    rCtx.beginPath(); rCtx.arc(cx, cy, r*0.7, 0, Math.PI*2); rCtx.fill();
    
    reactorAngle += proxyActive ? 0.05 : 0.01;
    requestAnimationFrame(drawReactor);
}
drawReactor();

document.getElementById('btnEngageProxy').addEventListener('click', function() {
    proxyActive = !proxyActive;
    this.classList.toggle('active');
    this.textContent = proxyActive ? "DISENGAGE OPTIMIZER" : "INITIALIZE OPTIMIZER";
    
    const icon = document.getElementById('proxyStatusIcon');
    const text = document.getElementById('proxyStatusText');
    
    if (proxyActive) {
        icon.className = 'fas fa-shield-check'; icon.style.color = '#00E5FF';
        text.textContent = 'ONLINE';
        
        bwSimInterval = setInterval(() => {
            const bw = (Math.random() * 15).toFixed(1);
            document.getElementById('bwText').textContent = bw + ' MB/s';
            document.getElementById('bwFill').style.width = (bw / 15 * 100) + '%';
            
            // Randomly increase folded/blocked
            const sf = document.getElementById('statFolded');
            sf.textContent = (parseInt(sf.textContent.replace(',','')) + Math.floor(Math.random()*5)).toLocaleString();
        }, 1000);
    } else {
        icon.className = 'fas fa-shield-alt'; icon.style.color = '#FF0055';
        text.textContent = 'STANDBY';
        clearInterval(bwSimInterval);
        document.getElementById('bwText').textContent = '0.0 MB/s';
        document.getElementById('bwFill').style.width = '0%';
    }
});

// Start fetching IPTV on load
loadLiveTV();
