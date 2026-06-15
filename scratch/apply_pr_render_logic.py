import os

pr_path = "/Users/phileasdazeleygaist/Desktop/My Websites/edge-cases-2026/pr.html"

with open(pr_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
for idx, line in enumerate(lines):
    if "function renderDynamicPR(speakers)" in line:
        start_idx = idx
        break

if start_idx == -1:
    print("Error: renderDynamicPR function start not found!")
    exit(1)

# Find the end of the function. The script tag ends right after.
end_idx = -1
for idx in range(start_idx, len(lines)):
    if "</script>" in lines[idx]:
        # The closing brace of renderDynamicPR is the line right before </script> or close to it.
        # Let's find the line with just a closing brace "        }" or "        }\n"
        for search_idx in range(idx - 1, start_idx, -1):
            if lines[search_idx].strip() == "}":
                end_idx = search_idx
                break
        break

if end_idx == -1:
    print("Error: renderDynamicPR function end not found!")
    exit(1)

print(f"Replacing renderDynamicPR from line {start_idx+1} to {end_idx+1}")

new_function_code = """        function renderDynamicPR(speakers, settings) {
            const landscapeSvgBg = document.getElementById('svg-bg-landscape').innerHTML;
            const squareSvgBg = document.getElementById('svg-bg-square').innerHTML;

            const isReleaseMode = (settings && settings.releaseMode === true) || window.location.search.includes('releaseMode=true');

            // Process speakers: conditionally anonymize if releaseMode is true
            const processedSpeakers = speakers.map(s => {
                const needsUpdate = !s.image || !s.bio || !s.topic || !s.abstract || s.note;
                const isAnonymous = isReleaseMode && needsUpdate && !s.publishAnyway;
                if (isAnonymous) {
                    return {
                        ...s,
                        name: "To Be Announced",
                        affiliation: "Mystery Contributor",
                        topic: "Coming soon",
                        abstract: "More details coming soon.",
                        bio: "",
                        image: "",
                        isAnonymous: true
                    };
                }
                return { ...s, isAnonymous: false };
            });

            // Sort speakers in release mode
            if (isReleaseMode) {
                processedSpeakers.sort((a, b) => {
                    const aAnon = a.isAnonymous;
                    const bAnon = b.isAnonymous;
                    
                    if (aAnon && !bAnon) return 1;
                    if (!aAnon && bAnon) return -1;
                    
                    const aNeeds = (!a.image || !a.bio || !a.topic || !a.abstract || !!a.note);
                    const bNeeds = (!b.image || !b.bio || !b.topic || !b.abstract || !!b.note);
                    
                    if (aNeeds && !bNeeds) return 1;
                    if (!aNeeds && bNeeds) return -1;
                    
                    return 0;
                });
            }

            // 1. Populating Tab 2 (Speaker Banners)
            const bannersGrid = document.getElementById('speaker-banners-grid');
            if (bannersGrid) {
                bannersGrid.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const photoHTML = speaker.isAnonymous ? 
                        `<div class="photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 48px; height: 48px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` : 
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);
                    
                    const reasons = [];
                    if (!speaker.image) reasons.push('image');
                    if (!speaker.bio) reasons.push('bio');
                    if (!speaker.topic) reasons.push('topic');
                    if (!speaker.abstract) reasons.push('abstract');
                    if (speaker.note) reasons.push('note');
                    const needsUpdate = reasons.length > 0;
                    const draftBadge = (needsUpdate && !speaker.isAnonymous) ? `<span style="color: #eaac8b; font-size: 0.8rem; margin-left: 0.5rem; border: 1px solid #eaac8b; padding: 0.1rem 0.4rem; border-radius: 4px; font-family: var(--font-mono); font-weight: 700; text-transform: uppercase;">DRAFT</span>` : '';

                    return `
                        <div class="card-container-wrapper">
                            <div class="card-label">
                                <div>Speaker: ${speaker.name}${draftBadge}<span class="dimensions">1200 x 630</span></div>
                                <div class="card-actions">
                                    <button class="card-action-btn" onclick="previewCard('${speaker.id}-banner')">👁️ Preview</button>
                                    <button class="card-action-btn" onclick="saveCard('${speaker.id}-banner')">💾 Save PNG</button>
                                </div>
                            </div>
                            <div class="preview-scale-wrapper size-banner-wrapper">
                                <div class="card-export-container size-banner" id="${speaker.id}-banner">
                                    ${landscapeSvgBg}
                                    <div class="card-content">
                                        <div class="card-header-meta">Wednesday, Oct 14 @ Lecture Hall 10, Binghamton University | <span style="white-space: nowrap;">2:30 PM – 5:45 PM</span></div>
                                        <div class="template-speaker-banner">
                                            <div class="speaker-left">
                                                <div class="photo-frame">
                                                    ${photoHTML}
                                                </div>
                                                <h3>${speaker.name}</h3>
                                                <p class="affiliation">${speaker.affiliation || ''}</p>
                                            </div>
                                            <div class="speaker-right">
                                                <span class="section-tag">Featured Presentation</span>
                                                <h2 class="talk-title">${speaker.topic || 'Coming soon'}</h2>
                                                <p class="talk-abstract">${speaker.abstract || 'Presentation details coming soon.'}</p>
                                            </div>
                                        </div>
                                        <div class="card-footer">
                                            <div class="card-footer-logo">
                                                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <line x1="6" y1="24" x2="14" y2="20" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="6" y1="24" x2="10" y2="12" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="14" y1="20" x2="10" y2="12" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.5" stroke-dasharray="2.5 2.5" />
                                                    <circle cx="6" cy="24" r="3" fill="#508484" />
                                                    <circle cx="10" cy="12" r="3" fill="#6d597a" />
                                                    <circle cx="14" cy="20" r="3" fill="#355070" />
                                                    <circle cx="26" cy="8" r="4.5" fill="#e56b6f" stroke="#ffffff" stroke-width="1" />
                                                </svg>
                                                <span>Edge Cases</span>
                                            </div>
                                            <div class="card-footer-web">edgecases2026.org</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // 2. Populating Tab 3 (Speaker Squares)
            const squaresGrid = document.getElementById('speaker-squares-grid');
            if (squaresGrid) {
                squaresGrid.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const photoHTML = speaker.isAnonymous ? 
                        `<div class="photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 48px; height: 48px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` : 
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);
                    
                    const reasons = [];
                    if (!speaker.image) reasons.push('image');
                    if (!speaker.bio) reasons.push('bio');
                    if (!speaker.topic) reasons.push('topic');
                    if (!speaker.abstract) reasons.push('abstract');
                    if (speaker.note) reasons.push('note');
                    const needsUpdate = reasons.length > 0;
                    const draftBadge = (needsUpdate && !speaker.isAnonymous) ? `<span style="color: #eaac8b; font-size: 0.8rem; margin-left: 0.5rem; border: 1px solid #eaac8b; padding: 0.1rem 0.4rem; border-radius: 4px; font-family: var(--font-mono); font-weight: 700; text-transform: uppercase;">DRAFT</span>` : '';

                    return `
                        <div class="card-container-wrapper">
                            <div class="card-label">
                                <div>Speaker: ${speaker.name}${draftBadge}<span class="dimensions">1080 x 1080</span></div>
                                <div class="card-actions">
                                    <button class="card-action-btn" onclick="previewCard('${speaker.id}-square')">👁️ Preview</button>
                                    <button class="card-action-btn" onclick="saveCard('${speaker.id}-square')">💾 Save PNG</button>
                                </div>
                            </div>
                            <div class="preview-scale-wrapper size-square-wrapper">
                                <div class="card-export-container size-square" id="${speaker.id}-square">
                                    ${squareSvgBg}
                                    <div class="card-content">
                                        <div class="card-header-meta large">Wednesday, Oct 14 @ Lecture Hall 10, Binghamton University | <span style="white-space: nowrap;">2:30 PM – 5:45 PM</span></div>
                                        <div class="template-speaker-square">
                                            <div class="speaker-square-left">
                                                <div class="photo-frame">
                                                    ${photoHTML}
                                                </div>
                                                <h3>${speaker.name}</h3>
                                                <p class="affiliation">${speaker.affiliation || ''}</p>
                                            </div>
                                            <div class="speaker-square-right">
                                                <span class="section-tag">Featured Presentation</span>
                                                <h2 class="talk-title">${speaker.topic || 'Coming soon'}</h2>
                                                <p class="talk-abstract">${speaker.abstract || 'Presentation details coming soon.'}</p>
                                            </div>
                                        </div>
                                        <div class="card-footer">
                                            <div class="card-footer-logo">
                                                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <line x1="6" y1="24" x2="14" y2="20" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="6" y1="24" x2="10" y2="12" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="14" y1="20" x2="10" y2="12" stroke="#8c827a" stroke-width="1.2" />
                                                    <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.5" stroke-dasharray="2.5 2.5" />
                                                    <circle cx="6" cy="24" r="3" fill="#508484" />
                                                    <circle cx="10" cy="12" r="3" fill="#6d597a" />
                                                    <circle cx="14" cy="20" r="3" fill="#355070" />
                                                    <circle cx="26" cy="8" r="4.5" fill="#e56b6f" stroke="#ffffff" stroke-width="1" />
                                                </svg>
                                                <span>Edge Cases</span>
                                            </div>
                                            <div class="card-footer-web">edgecases2026.org</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // 3. Populating Tab 4 (Wildcard Lineups)
            const bannerSpeakersContainer = document.getElementById('wildcard-banner-speakers');
            if (bannerSpeakersContainer) {
                if (processedSpeakers.length > 6) {
                    bannerSpeakersContainer.style.gap = '1rem 2rem';
                    bannerSpeakersContainer.style.height = 'auto';
                } else {
                    bannerSpeakersContainer.style.gap = '';
                    bannerSpeakersContainer.style.height = '';
                }
                bannerSpeakersContainer.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const wPhotoHTML = speaker.isAnonymous ? 
                        `<div class="wildcard-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 20px; height: 20px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` :
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;wildcard-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="wildcard-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);
                    
                    return `
                        <div class="wildcard-speaker-row">
                            <div class="wildcard-photo">
                                ${wPhotoHTML}
                            </div>
                            <div class="wildcard-speaker-info">
                                <h4>${speaker.name}</h4>
                                <p>${getShortAffiliation(speaker.affiliation)}</p>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            const squareSpeakersContainer = document.getElementById('wildcard-square-speakers');
            if (squareSpeakersContainer) {
                if (processedSpeakers.length > 6) {
                    squareSpeakersContainer.classList.add('compact-grid');
                } else {
                    squareSpeakersContainer.classList.remove('compact-grid');
                }
                squareSpeakersContainer.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const wPhotoHTML = speaker.isAnonymous ? 
                        `<div class="wildcard-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 20px; height: 20px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` :
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;wildcard-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="wildcard-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);
                    
                    return `
                        <div class="wildcard-speaker-row">
                            <div class="wildcard-photo">
                                ${wPhotoHTML}
                            </div>
                            <div class="wildcard-speaker-info">
                                <h4>${speaker.name}</h4>
                                <p>${getShortAffiliation(speaker.affiliation)}</p>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // 4. Populating Tab 5 (Creative Wildcards)
            // Divide speakers into Session A and Session B
            const half = Math.ceil(processedSpeakers.length / 2);
            const sessionASpeakers = processedSpeakers.slice(0, half);
            const sessionBSpeakers = processedSpeakers.slice(half);

            const sessionATimes = getSessionATimes(sessionASpeakers.length);
            const sessionBTimes = getSessionBTimes(sessionBSpeakers.length);

            // Construct timeline HTML
            let timelineHTML = `
                <div class="timeline-item">
                    <div class="timeline-time">14:30</div>
                    <div class="timeline-content">
                        <h4>Welcome & Introduction</h4>
                    </div>
                </div>
            `;

            sessionASpeakers.forEach((speaker, index) => {
                const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                const tPhotoHTML = speaker.isAnonymous ? 
                    `<div class="timeline-speaker-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                        <svg viewBox="0 0 24 24" fill="currentColor" style="width: 20px; height: 20px; opacity: 0.85;">
                            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                        </svg>
                     </div>` :
                    (speaker.image ? 
                        `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;timeline-speaker-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                        `<div class="timeline-speaker-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);

                timelineHTML += `
                    <div class="timeline-item">
                        <div class="timeline-time">${sessionATimes[index]}</div>
                        <div class="timeline-speaker-photo">
                            ${tPhotoHTML}
                        </div>
                        <div class="timeline-content">
                            <h4>${speaker.name}</h4>
                            <p>${speaker.topic || 'Coming soon'} (${getShortAffiliation(speaker.affiliation)})</p>
                        </div>
                    </div>
                `;
            });

            timelineHTML += `
                <div class="timeline-item break">
                    <div class="timeline-time">16:00</div>
                    <div class="timeline-content">
                        <h4>Coffee & Networking Break</h4>
                    </div>
                </div>
            `;

            sessionBSpeakers.forEach((speaker, index) => {
                const globalIndex = half + index;
                const c1 = CONFIG_COLORS[globalIndex % CONFIG_COLORS.length];
                const c2 = CONFIG_COLORS[(globalIndex + 2) % CONFIG_COLORS.length];
                const tPhotoHTML = speaker.isAnonymous ? 
                    `<div class="timeline-speaker-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                        <svg viewBox="0 0 24 24" fill="currentColor" style="width: 20px; height: 20px; opacity: 0.85;">
                            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                        </svg>
                     </div>` :
                    (speaker.image ? 
                        `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;timeline-speaker-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                        `<div class="timeline-speaker-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);

                timelineHTML += `
                    <div class="timeline-item">
                        <div class="timeline-time">${sessionBTimes[index]}</div>
                        <div class="timeline-speaker-photo">
                            ${tPhotoHTML}
                        </div>
                        <div class="timeline-content">
                            <h4>${speaker.name}</h4>
                            <p>${speaker.topic || 'Coming soon'} (${getShortAffiliation(speaker.affiliation)})</p>
                        </div>
                    </div>
                `;
            });

            timelineHTML += `
                <div class="timeline-item">
                    <div class="timeline-time">17:15</div>
                    <div class="timeline-content">
                        <h4>Group Discussion & Q&A</h4>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-time">17:35</div>
                    <div class="timeline-content">
                        <h4>Closing Remarks</h4>
                    </div>
                </div>
            `;

            const scheduleBannerTimeline = document.getElementById('schedule-banner-timeline');
            if (scheduleBannerTimeline) {
                if (processedSpeakers.length > 5) {
                    scheduleBannerTimeline.classList.add('compact-timeline');
                } else {
                    scheduleBannerTimeline.classList.remove('compact-timeline');
                }
                scheduleBannerTimeline.innerHTML = timelineHTML;
            }

            const scheduleSquareTimeline = document.getElementById('schedule-square-timeline');
            if (scheduleSquareTimeline) {
                if (processedSpeakers.length > 5) {
                    scheduleSquareTimeline.classList.add('compact-timeline-square');
                } else {
                    scheduleSquareTimeline.classList.remove('compact-timeline-square');
                }
                scheduleSquareTimeline.innerHTML = timelineHTML;
            }

            // Columns layout (Stripe Columns Banner)
            const stripesBannerCols = document.getElementById('stripes-banner-cols');
            if (stripesBannerCols) {
                if (processedSpeakers.length > 5) {
                    stripesBannerCols.classList.add('compact-stripes');
                    stripesBannerCols.style.gridTemplateColumns = '';
                } else {
                    stripesBannerCols.classList.remove('compact-stripes');
                    stripesBannerCols.style.gridTemplateColumns = `repeat(${processedSpeakers.length}, 1fr)`;
                }
                stripesBannerCols.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const sPhotoHTML = speaker.isAnonymous ? 
                        `<div class="stripe-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 24px; height: 24px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` :
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;stripe-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="stripe-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);

                    return `
                        <div class="stripe-column">
                            <div class="stripe-photo">
                                ${sPhotoHTML}
                            </div>
                            <div class="stripe-info">
                                <h4>${speaker.name}</h4>
                                <p class="affiliation">${getShortAffiliation(speaker.affiliation)}</p>
                                <p class="topic">${speaker.topic || 'Coming soon'}</p>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Columns layout (Stripe Columns Square)
            const stripesSquareCols = document.getElementById('stripes-square-cols');
            if (stripesSquareCols) {
                if (processedSpeakers.length > 4) {
                    stripesSquareCols.classList.add('compact-stripes-square');
                    stripesSquareCols.style.gap = '';
                    stripesSquareCols.style.height = '';
                    stripesSquareCols.style.margin = '';
                } else {
                    stripesSquareCols.classList.remove('compact-stripes-square');
                    stripesSquareCols.style.gap = '1.25rem 2rem';
                    stripesSquareCols.style.height = 'auto';
                    stripesSquareCols.style.margin = '1rem 0';
                }
                stripesSquareCols.innerHTML = processedSpeakers.map((speaker, index) => {
                    const c1 = CONFIG_COLORS[index % CONFIG_COLORS.length];
                    const c2 = CONFIG_COLORS[(index + 2) % CONFIG_COLORS.length];
                    const sPhotoHTML = speaker.isAnonymous ? 
                        `<div class="stripe-photo-placeholder" style="background: #f4f3f2; border: 1.5px dashed #d1cecb; color: #beb9b5; display: flex; align-items: center; justify-content: center;">
                            <svg viewBox="0 0 24 24" fill="currentColor" style="width: 24px; height: 24px; opacity: 0.85;">
                                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                            </svg>
                         </div>` :
                        (speaker.image ? 
                            `<img src="${speaker.image}" alt="${speaker.name}" onerror="this.outerHTML='<div class=&quot;stripe-photo-placeholder&quot; style=&quot;background: linear-gradient(135deg, ${c1}, ${c2})&quot;>${getInitials(speaker.name)}</div>';">` :
                            `<div class="stripe-photo-placeholder" style="background: linear-gradient(135deg, ${c1}, ${c2})">${getInitials(speaker.name)}</div>`);

                    return `
                        <div class="stripe-column">
                            <div class="stripe-photo">
                                ${sPhotoHTML}
                            </div>
                            <div class="stripe-info">
                                <h4>${speaker.name}</h4>
                                <p class="affiliation">${speaker.affiliation || ''}</p>
                                <p class="topic">${speaker.topic || 'Coming soon'}</p>
                            </div>
                        </div>
                    `;
                }).join('');
            }

            // Typographic list (Typographic Poster Banner)
            const typoBannerList = document.getElementById('typo-banner-list');
            if (typoBannerList) {
                if (processedSpeakers.length > 5) {
                    typoBannerList.classList.add('compact-typo-list');
                } else {
                    typoBannerList.classList.remove('compact-typo-list');
                }
                typoBannerList.innerHTML = processedSpeakers.map(speaker => `
                    <div class="typo-speaker-item">
                        <h3>${speaker.name}</h3>
                        <p class="topic">${speaker.topic || 'Coming soon'}</p>
                        <p class="affiliation">${speaker.affiliation || ''}</p>
                    </div>
                `).join('');
            }

            // Typographic grid (Typographic Poster Square)
            const typoSquareGrid = document.getElementById('typo-square-grid');
            if (typoSquareGrid) {
                if (processedSpeakers.length > 4) {
                    typoSquareGrid.classList.add('compact-typo-grid-square');
                    typoSquareGrid.style.gap = '';
                    typoSquareGrid.style.margin = '';
                    typoSquareGrid.style.padding = '';
                } else {
                    typoSquareGrid.classList.remove('compact-typo-grid-square');
                    typoSquareGrid.style.gap = '1.5rem 2rem';
                    typoSquareGrid.style.margin = '1rem 0';
                    typoSquareGrid.style.padding = '1.5rem 0';
                }
                typoSquareGrid.innerHTML = processedSpeakers.map(speaker => `
                    <div class="typo-speaker-item">
                        <h3>${speaker.name}</h3>
                        <p class="topic">${speaker.topic || 'Coming soon'}</p>
                        <p class="affiliation">${speaker.affiliation || ''}</p>
                    </div>
                `).join('');
            }
        }"""

# Slice replacement in Python
new_lines = lines[:start_idx] + [new_function_code + "\n"] + lines[end_idx+1:]

with open(pr_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Part 2 (Render logic) applied successfully!")
