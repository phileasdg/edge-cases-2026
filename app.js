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
        hubRadius: 5.5,
        colors: ['#e56b6f', '#eaac8b', '#b5838d', '#6d597a', '#508484', '#355070'], // Creative palette
        edgeColor: 'rgba(140, 130, 122, 0.12)', // Muted warm grey lines
        labelColor: '#2b2623'   // Espresso
    };

    // Mouse tracking for interactive network physics
    const mouse = { x: null, y: null, active: false };
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
        mouse.active = true;
    });
    canvas.addEventListener('mouseleave', () => {
        mouse.active = false;
    });

    async function loadData() {
        try {
            const [themesRes, speakersRes, networkRes, agendaRes, settingsRes] = await Promise.all([
                fetch('data/themes.json'),
                fetch('data/speakers.json'),
                fetch('data/network.json'),
                fetch('data/agenda.json'),
                fetch('data/settings.json')
            ]);

            const themes = await themesRes.json();
            const speakers = await speakersRes.json();
            const agenda = await agendaRes.json();
            const settings = await settingsRes.json();
            cachedNetworkData = await networkRes.json();
            cachedHubLabels = themes.map(t => t.title);

            renderThemes(themes);
            renderSpeakers(speakers, settings);
            renderAgenda(agenda);
            initNetwork(cachedNetworkData, cachedHubLabels);

        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    function renderThemes(themes) {
        const grid = document.getElementById('themes-grid');
        if (!grid) return;
        const colors = CONFIG.colors;
        const rgbVals = {
            '#e56b6f': '229, 107, 111',
            '#eaac8b': '234, 172, 139',
            '#b5838d': '181, 131, 141',
            '#6d597a': '109, 89, 122',
            '#508484': '80, 132, 132',
            '#355070': '53, 80, 112'
        };
        grid.innerHTML = themes.map((theme, index) => {
            const color = colors[index % colors.length];
            const rgb = rgbVals[color] || '80, 132, 132';
            return `
                <div class="theme-card" data-reveal style="--theme-color: ${color}; border-top: 4px solid ${color}; background-color: rgba(${rgb}, 0.045);">
                    <div class="mono" style="color: ${color}; font-weight: 700;">${theme.id}</div>
                    <h3>${theme.title}</h3>
                    <p style="color: var(--muted-text);">${theme.description}</p>
                </div>
            `;
        }).join('');
        observeReveals();
    }

    function getInitials(name) {
        if (!name) return '??';
        const parts = name.trim().split(/\s+/);
        if (parts.length >= 2) {
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }
        return name.slice(0, 2).toUpperCase();
    }

    function renderSpeakers(speakers, settings) {
        const container = document.getElementById('speakers-container');
        if (!container) return;

        const showPlaceholder = settings && settings.showPlaceholderOnMissingImage;
        const colors = CONFIG.colors;

        if (speakers && speakers.length > 0) {
            // Show real speaker lineup
            container.innerHTML = `
                <h2 data-reveal>Featured Contributors</h2>
                <div class="grid" id="speakers-grid" style="margin-top: var(--space-md);">
                    ${speakers.map((speaker, index) => {
                        const hasImage = !!speaker.image;
                        const c1 = colors[index % colors.length];
                        const c2 = colors[(index + 2) % colors.length];
                        const gradientStyle = `background: linear-gradient(135deg, ${c1}, ${c2}); box-shadow: 0 4px 15px rgba(43, 38, 35, 0.12);`;
                        
                        return `
                            <div class="speaker-card ${hasImage ? 'has-image' : 'no-image'}" data-reveal style="--theme-color: ${c1};">
                                ${hasImage ? `
                                    <div class="speaker-image">
                                        <img src="${speaker.image}" 
                                             alt="${speaker.name}"
                                             onerror="this.parentElement.className='speaker-image-placeholder'; this.parentElement.style='${gradientStyle}'; this.parentElement.innerHTML='${getInitials(speaker.name)}';">
                                    </div>
                                ` : `
                                    <div class="speaker-image-placeholder" style="${gradientStyle}">
                                        ${getInitials(speaker.name)}
                                    </div>
                                `}
                                <div class="speaker-info">
                                    <h3>${speaker.name}</h3>
                                    <div class="affiliation">${speaker.affiliation}</div>
                                    <p class="topic">${speaker.topic}</p>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        } else {
            // Show teaser/placeholder
            container.innerHTML = `
                <h2 data-reveal>Featured Contributors</h2>
                <div style="margin-top: var(--space-md); text-align: center; padding: 4rem 2rem; background: rgba(0,0,0,0.02); border-radius: var(--radius-lg); border: 2px dashed var(--border-color);">
                    <h3 style="margin-bottom: 1rem; font-size: 1.5rem; color: var(--primary-dark);">Speaker Lineup</h3>
                    <p style="font-size: 1.1rem; opacity: 0.8; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                        <strong>More information coming soon.</strong>
                    </p>
                    <div style="margin-top: 2rem;">
                        <a href="https://www.wolframcloud.com/obj/phileasd/EdgeCases2026_Submission" target="_blank"
                            class="primary-cta" style="display: inline-flex; justify-content: center;">
                            Submit a Proposal
                            <svg class="arrow-circle-icon" width="24" height="14" viewBox="-395 256 24 14" style="margin-left: 0.5rem;">
                                <path fill="none" d="M-377 263h-17.6m15.4-2.2l2.2 2.2-2.2 2.2" stroke="currentColor" stroke-width="1.5" />
                                <circle fill="none" cx="-378.1" cy="263" r="6.8" stroke="currentColor" stroke-width="1.5" />
                            </svg>
                        </a>
                    </div>
                </div>
            `;
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
            label: null,
            color: CONFIG.colors[Math.floor(Math.random() * CONFIG.colors.length)]
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

        // Mouse interaction: nodes clear out slightly when the mouse is near
        if (mouse.active) {
            nodes.forEach(node => {
                const dx = node.x - mouse.x;
                const dy = node.y - mouse.y;
                const distSq = dx * dx + dy * dy || 1;
                const dist = Math.sqrt(distSq);
                if (dist < 150) {
                    const force = (150 - dist) * 0.06;
                    node.vx += (dx / dist) * force;
                    node.vy += (dy / dist) * force;
                }
            });
        }

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
            ctx.fillStyle = node.color;
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
