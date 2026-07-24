// ALL-IN-One IPTV - AGI-Era Cyber Web Application & Particle Matrix Engine

let allChannels = [];
let filteredChannels = [];
let isPinUnlocked = false;
let hlsPlayer = null;

const M3U_FEED_URL = "https://raw.githubusercontent.com/ShoumikBalaSomu/ALL-IN-One-IPTV/main/output/checked_combined_by_country.m3u";

document.addEventListener("DOMContentLoaded", () => {
    initAGIMatrixCanvas();
    setupTabNavigation();
    setupSearchAndFilter();
    setupPinModal();
    loadChannels();
});

// AGI Particle Matrix Background Animation
function initAGIMatrixCanvas() {
    const canvas = document.getElementById("agiMatrixCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = 60;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8,
            radius: Math.random() * 2 + 1,
            color: Math.random() > 0.5 ? "#00f0ff" : "#7000ff"
        });
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particleCount; i++) {
            let p1 = particles[i];
            p1.x += p1.vx;
            p1.y += p1.vy;

            if (p1.x < 0 || p1.x > width) p1.vx *= -1;
            if (p1.y < 0 || p1.y > height) p1.vy *= -1;

            ctx.beginPath();
            ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
            ctx.fillStyle = p1.color;
            ctx.fill();

            for (let j = i + 1; j < particleCount; j++) {
                let p2 = particles[j];
                let dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(0, 240, 255, ${1 - dist / 120})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
}

// Tab Navigation
function setupTabNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const tabContents = document.querySelectorAll(".tab-content");

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetTab = item.getAttribute("data-tab");
            
            navItems.forEach(nav => nav.classList.remove("active"));
            tabContents.forEach(tab => tab.classList.remove("active"));

            item.classList.add("active");
            document.getElementById(`tab-${targetTab}`).classList.add("active");
        });
    });
}

// Load and Parse M3U
async function loadChannels() {
    const listContainer = document.getElementById("channelListContainer");
    try {
        const response = await fetch(M3U_FEED_URL);
        const text = await response.text();
        allChannels = parseM3U(text);
        filteredChannels = [...allChannels];

        document.getElementById("channelCountBadge").innerText = `${allChannels.length} Channels`;
        renderChannelList(filteredChannels);

        // Auto-play first channel if available
        if (allChannels.length > 0) {
            playChannel(allChannels[0]);
        }
    } catch (err) {
        console.error("Failed to load M3U feed:", err);
        listContainer.innerHTML = `<div class="error-msg">Failed to load channels feed.</div>`;
    }
}

// M3U Parser Helper
function parseM3U(content) {
    const lines = content.split('\n');
    const channels = [];
    let currentCh = {};

    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('#EXTINF:')) {
            const nameMatch = line.match(/,(.*)$/);
            const logoMatch = line.match(/tvg-logo="(.*?)"/);
            const groupMatch = line.match(/group-title="(.*?)"/);

            currentCh = {
                name: nameMatch ? nameMatch[1].trim() : 'Unknown Channel',
                logo: logoMatch ? logoMatch[1] : 'assets/app_icon.png',
                group: groupMatch ? groupMatch[1] : 'General'
            };
        } else if (line.startsWith('http://') || line.startsWith('https://')) {
            currentCh.url = line;
            if (currentCh.name) {
                channels.push({ ...currentCh });
                currentCh = {};
            }
        }
    }
    return channels;
}

// Render Channel List
function renderChannelList(channels) {
    const listContainer = document.getElementById("channelListContainer");
    listContainer.innerHTML = "";

    if (channels.length === 0) {
        listContainer.innerHTML = `<div class="empty-msg">No channels found.</div>`;
        return;
    }

    channels.slice(0, 150).forEach(ch => {
        const card = document.createElement("div");
        card.className = "channel-card";
        card.innerHTML = `
            <img src="${ch.logo}" class="channel-logo" onerror="this.src='assets/app_icon.png'">
            <div class="channel-info">
                <h4>${ch.name}</h4>
                <p>${ch.group}</p>
            </div>
        `;

        card.addEventListener("click", () => {
            document.querySelectorAll(".channel-card").forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            playChannel(ch);
        });

        listContainer.appendChild(card);
    });
}

// HLS Stream Player Integration
function playChannel(channel) {
    const video = document.getElementById("videoPlayer");
    document.getElementById("activeStreamTitle").innerText = channel.name;

    if (Hls.isSupported() && channel.url.includes(".m3u8")) {
        if (hlsPlayer) {
            hlsPlayer.destroy();
        }
        hlsPlayer = new Hls();
        hlsPlayer.loadSource(channel.url);
        hlsPlayer.attachMedia(video);
        hlsPlayer.on(Hls.Events.MANIFEST_PARSED, () => {
            video.play().catch(e => console.log("Autoplay blocked:", e));
        });
    } else {
        video.src = channel.url;
        video.play().catch(e => console.log("Playback error:", e));
    }
}

// Search and Category Chips
function setupSearchAndFilter() {
    const searchInput = document.getElementById("channelSearch");
    const chips = document.querySelectorAll(".chip");

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        filterChannels(query, null);
    });

    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            chips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            const group = chip.getAttribute("data-group");
            filterChannels("", group);
        });
    });
}

function filterChannels(query, group) {
    filteredChannels = allChannels.filter(ch => {
        const matchesQuery = !query || ch.name.toLowerCase().includes(query) || ch.group.toLowerCase().includes(query);
        const matchesGroup = !group || group === 'all' || ch.group.toLowerCase().includes(group.toLowerCase()) || ch.name.toLowerCase().includes(group.toLowerCase());
        return matchesQuery && matchesGroup;
    });
    renderChannelList(filteredChannels);
}

// PIN Modal Setup
function setupPinModal() {
    const btn = document.getElementById("pinUnlockBtn");
    btn.addEventListener("click", () => {
        document.getElementById("pinModal").style.display = "flex";
    });
}

function closePinModal() {
    document.getElementById("pinModal").style.display = "none";
}

function verifyPin() {
    const pin = document.getElementById("pinInput").value;
    if (pin === "0171") {
        isPinUnlocked = true;
        document.getElementById("pinStatusText").innerText = "PIN Unlocked";
        document.getElementById("pinUnlockBtn").classList.replace("btn-secondary", "btn-primary");
        alert("Parental Control Unlocked!");
        closePinModal();
    } else {
        alert("Invalid PIN!");
    }
}
