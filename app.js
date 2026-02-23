document.addEventListener('DOMContentLoaded', () => {
    // 1. Reveal animations on scroll
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.1 });

    function observeReveals() {
        document.querySelectorAll('[data-reveal]').forEach(el => {
            revealObserver.observe(el);
        });
    }

    /**
     * 2. Edge Cases: Complex Topic Network Visualization
     */
    const canvas = document.getElementById('networkCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height, dpr;
    let nodes = [];
    let links = [];
    let cachedNetworkData = null;
    let cachedHubLabels = null;

    // Configuration
    const CONFIG = {
        nodeCount: 70,
        m: 2,
        repulsion: 150,
        springLength: 70,
        springStrength: 0.04,
        centerStrength: 0.06,
        damping: 0.9,
        nodeRadius: 2.5,
        hubRadius: 5,
        activeColor: '#00a9b7',
        edgeColor: 'rgba(0, 61, 91, 0.15)',
        labelColor: 'rgba(26, 26, 26, 0.8)'
    };

    async function loadData() {
        try {
            const [themesRes, speakersRes, networkRes, agendaRes] = await Promise.all([
                fetch('data/themes.json'),
                fetch('data/speakers.json'),
                fetch('data/network.json'),
                fetch('data/agenda.json')
            ]);

            const themes = await themesRes.json();
            const speakers = await speakersRes.json();
            const agenda = await agendaRes.json();
            cachedNetworkData = await networkRes.json();
            cachedHubLabels = themes.map(t => t.title);

            renderThemes(themes);
            renderSpeakers(speakers);
            renderAgenda(agenda);
            initNetwork(cachedNetworkData, cachedHubLabels);

        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    function renderThemes(themes) {
        const grid = document.getElementById('themes-grid');
        if (!grid) return;
        grid.innerHTML = themes.map(theme => `
            <div class="theme-card" data-reveal>
                <div class="mono">${theme.id}</div>
                <h3>${theme.title}</h3>
                <p>${theme.description}</p>
            </div>
        `).join('');
        observeReveals();
    }

    function renderSpeakers(speakers) {
        // Update Teaser Text
        const teaserText = document.getElementById('teaser-text');
        if (teaserText) {
            teaserText.innerHTML = `<strong>${speakers.length} researchers</strong> have expressed interest or tentatively accepted an invitation.<br><br><strong>More information coming soon.</strong>`;
        }

        const grid = document.getElementById('speakers-grid');
        if (!grid) return;
        grid.innerHTML = speakers.map(speaker => `
            <div class="speaker-card" data-reveal>
                <h3>${speaker.name}</h3>
                <div class="affiliation">${speaker.affiliation}</div>
                <p class="topic">${speaker.topic}</p>
            </div>
        `).join('');

        // Handle Login Logic
        const loginLink = document.getElementById('login-link');
        const speakersSection = document.getElementById('speakers-full');
        const teaserSection = document.getElementById('speakers-teaser');

        if (loginLink) {
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                const p = prompt('Please enter the password to view this website:');
                if (p === 'edgecases2026secrets') {
                    unlockSite();
                } else if (p !== null) {
                    alert('Incorrect password.');
                }
            });
        }

        function unlockSite() {
            if (speakersSection) speakersSection.style.display = 'block';
            if (teaserSection) teaserSection.style.display = 'none';
        }

        observeReveals();
    }

    function renderAgenda(agenda) {
        const list = document.getElementById('agenda-list');
        if (!list) return;

        // Render Details Header
        let html = '';
        if (agenda.details) {
            html += `
                <div class="agenda-header" data-reveal style="margin-bottom: 3rem; opacity: 0.8; font-size: 0.9rem;">
                    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                        <div><strong>Duration:</strong> ${agenda.details.duration}</div>
                        <div><strong>Speaker Goal:</strong> ${agenda.details.speakerGoal}</div>
                        <div><strong>Structure:</strong> ${agenda.details.structure}</div>
                    </div>
                </div>
            `;
        }

        // Render Items
        html += agenda.items.map(item => `
            <div class="agenda-item" data-reveal>
                <div class="time">${item.time}</div>
                <div class="details">
                    <h3>${item.title} ${item.duration ? `<span style="font-size: 0.8rem; opacity: 0.5; font-weight: 400; margin-left: 0.5rem;">(${item.duration})</span>` : ''}</h3>
                    ${item.description ? `<p>${item.description}</p>` : ''}
                </div>
            </div>
        `).join('');

        // Render Notes
        if (agenda.notes) {
            html += `
                <div class="agenda-notes" data-reveal style="margin-top: 4rem; padding: 2rem; background: rgba(0,0,0,0.03); border-radius: 8px; font-size: 0.9rem; border-left: 4px solid var(--accent-color);">
                    <h4 style="margin-bottom: 1rem;">Provisional Scaling & Extensions</h4>
                    ${agenda.notes.map(note => `<p style="margin-bottom: 0.5rem; opacity: 0.8;">• ${note}</p>`).join('')}
                </div>
            `;
        }

        list.innerHTML = html;
        observeReveals();
    }

    function initNetwork(data, hubLabels) {
        dpr = window.devicePixelRatio || 1;
        width = window.innerWidth;
        height = window.innerHeight;

        canvas.width = width * dpr;
        canvas.height = height * dpr;
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;
        ctx.scale(dpr, dpr);

        nodes = data.nodes.map(n => ({
            ...n,
            x: width / 2 + (Math.random() - 0.5) * 400,
            y: height / 2 + (Math.random() - 0.5) * 400,
            vx: 0,
            vy: 0,
            links: 0,
            label: null
        }));

        links = data.links.map(l => ({
            source: nodes.find(n => n.id === l.source),
            target: nodes.find(n => n.id === l.target)
        }));

        links.forEach(l => {
            if (l.source && l.target) {
                l.source.links++;
                l.target.links++;
            }
        });

        const sortedNodes = [...nodes].sort((a, b) => b.links - a.links);
        hubLabels.forEach((label, i) => {
            if (sortedNodes[i]) sortedNodes[i].label = label;
        });

        for (let i = 0; i < 200; i++) {
            physicsUpdate();
        }

        draw();
    }

    function physicsUpdate() {
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const n1 = nodes[i];
                const n2 = nodes[j];
                const dx = n2.x - n1.x;
                const dy = n2.y - n1.y;
                const distSq = dx * dx + dy * dy || 1;
                const force = CONFIG.repulsion / distSq;
                n1.vx -= dx * force;
                n1.vy -= dy * force;
                n2.vx += dx * force;
                n2.vy += dy * force;
            }
        }

        links.forEach(link => {
            if (!link.source || !link.target) return;
            const dx = link.target.x - link.source.x;
            const dy = link.target.y - link.source.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const force = (dist - CONFIG.springLength) * CONFIG.springStrength;
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            link.source.vx += fx;
            link.source.vy += fy;
            link.target.vx -= fx;
            link.target.vy -= fy;
        });

        nodes.forEach(node => {
            node.vx += (width / 2 - node.x) * CONFIG.centerStrength * 0.01;
            node.vy += (height / 2 - node.y) * CONFIG.centerStrength * 0.01;
            node.vx += (Math.random() - 0.5) * 0.015;
            node.vy += (Math.random() - 0.5) * 0.015;
            node.x += node.vx * 0.5;
            node.y += node.vy * 0.5;
            node.vx *= CONFIG.damping;
            node.vy *= CONFIG.damping;
        });
    }

    function draw() {
        ctx.clearRect(0, 0, width, height);

        const centerX = width / 2;
        const centerY = height / 2;
        // Stronger mask radius (55% of view)
        const maskRadius = Math.min(width, height) * 0.55;
        const MAX_ALPHA = 0.8; // Cap max opacity

        links.forEach(link => {
            if (!link.source || !link.target) return;
            const midX = (link.source.x + link.target.x) / 2;
            const midY = (link.source.y + link.target.y) / 2;
            const dx = midX - centerX;
            const dy = midY - centerY;
            const dist = Math.sqrt(dx * dx + dy * dy);

            // Sharper quartic curve for cleaner center
            let maskAlpha = Math.pow(Math.min(1, dist / maskRadius), 4);

            ctx.strokeStyle = CONFIG.edgeColor;
            ctx.lineWidth = 0.7;
            ctx.globalAlpha = maskAlpha * MAX_ALPHA;
            ctx.beginPath();
            ctx.moveTo(link.source.x, link.source.y);
            ctx.lineTo(link.target.x, link.target.y);
            ctx.stroke();
        });

        nodes.forEach(node => {
            const dx = node.x - centerX;
            const dy = node.y - centerY;
            const dist = Math.sqrt(dx * dx + dy * dy);

            let maskAlpha = Math.pow(Math.min(1, dist / maskRadius), 4);
            const isHub = node.label !== null;

            // Hubs still slightly more prominent but capped
            const baseAlpha = isHub ? Math.min(MAX_ALPHA, maskAlpha + 0.2) : maskAlpha * MAX_ALPHA;

            ctx.globalAlpha = baseAlpha;
            ctx.fillStyle = isHub ? CONFIG.activeColor : '#bbb';
            ctx.beginPath();
            ctx.arc(node.x, node.y, isHub ? CONFIG.hubRadius : CONFIG.nodeRadius, 0, Math.PI * 2);
            ctx.fill();

            if (isHub && maskAlpha > 0.1) {
                ctx.fillStyle = CONFIG.labelColor;
                ctx.globalAlpha = Math.min(MAX_ALPHA, maskAlpha);
                ctx.font = '600 12px "Outfit", sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(node.label, node.x, node.y + 20);
            }
        });

        ctx.globalAlpha = 1.0;
        physicsUpdate();
        requestAnimationFrame(draw);
    }

    // 3. Hamburger Logic
    const burger = document.getElementById('mobileBurger');
    const menu = document.getElementById('mobileMenu');
    if (burger && menu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('active');
            menu.classList.toggle('active');
            document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
        });
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                burger.classList.remove('active');
                menu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // 4. Scroll Highlight
    window.addEventListener('scroll', () => {
        let current = '';
        document.querySelectorAll('section').forEach(section => {
            if (pageYOffset >= (section.offsetTop - 100)) {
                current = section.getAttribute('id');
            }
        });
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.toggle('active', link.getAttribute('href').includes(current));
        });
    });

    window.addEventListener('resize', () => {
        if (cachedNetworkData) {
            initNetwork(cachedNetworkData, cachedHubLabels);
        }
    });

    loadData();
});
