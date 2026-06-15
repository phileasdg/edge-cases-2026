import os

pr_path = "/Users/phileasdazeleygaist/Desktop/My Websites/edge-cases-2026/pr.html"

with open(pr_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
for idx, line in enumerate(lines):
    if "<!-- 6.7 CCS Circular Logo (Light) -->" in line:
        start_idx = idx
        break

modal_idx = -1
for idx, line in enumerate(lines):
    if "<!-- Fullscreen Isolated Preview Modal Dialog -->" in line:
        modal_idx = idx
        break

if start_idx == -1 or modal_idx == -1:
    print("Error: start or modal index not found!")
    exit(1)

# Design of the four logos
logos_html = """                <!-- 6.7 CCS Circular Logo (Light) -->
                <div class="card-container-wrapper">
                    <div class="card-label">
                        <div>CCS Circular Logo (Light)<span class="dimensions">1080 x 1080</span></div>
                        <div class="card-actions">
                            <button class="card-action-btn" onclick="previewCard('logo-ccs-circle-light')">👁️ Preview</button>
                            <button class="card-action-btn" onclick="saveCard('logo-ccs-circle-light')">💾 Save PNG</button>
                        </div>
                    </div>
                    <div class="preview-scale-wrapper size-square-wrapper checkerboard-light">
                        <div class="card-export-container size-square transparent-bg" id="logo-ccs-circle-light" style="padding: 20px;">
                            <div class="card-content" style="justify-content: center; align-items: center; background: transparent;">
                                <div style="width: 1040px; height: 1040px; border-radius: 50%; background: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(43, 38, 35, 0.1); border: 24px solid #2b2623; position: relative; overflow: hidden;">
                                    <!-- Network Watermark Background -->
                                    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; color: #8c827a;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                        <line x1="15" y1="20" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="15" y1="20" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="35" y1="45" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="35" y1="45" x2="55" y2="85" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="55" y1="85" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="80" y1="65" x2="90" y2="25" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="90" y1="25" x2="65" y2="15" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="65" y1="15" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="65" y1="15" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <circle cx="35" cy="45" r="6" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="80" cy="65" r="8" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="65" cy="15" r="5" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="15" cy="20" r="1.2" fill="currentColor" opacity="0.15" />
                                        <circle cx="35" cy="45" r="1.8" fill="currentColor" opacity="0.2" />
                                        <circle cx="10" cy="75" r="1.5" fill="currentColor" opacity="0.15" />
                                        <circle cx="55" cy="85" r="1.6" fill="currentColor" opacity="0.15" />
                                        <circle cx="80" cy="65" r="2" fill="currentColor" opacity="0.2" />
                                        <circle cx="90" cy="25" r="1.2" fill="currentColor" opacity="0.15" />
                                        <circle cx="65" cy="15" r="1.6" fill="currentColor" opacity="0.2" />
                                    </svg>
                                    
                                    <svg width="520" height="520" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: -30px; position: relative; z-index: 2;">
                                        <line x1="6" y1="24" x2="14" y2="20" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="6" y1="24" x2="10" y2="12" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="14" y1="20" x2="10" y2="12" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.8" stroke-dasharray="2.5 2.5" />
                                        <circle cx="6" cy="24" r="3.2" fill="#508484" />
                                        <circle cx="10" cy="12" r="3.2" fill="#6d597a" />
                                        <circle cx="14" cy="20" r="3.2" fill="#355070" />
                                        <circle cx="26" cy="8" r="4.8" fill="#e56b6f" stroke="#ffffff" stroke-width="1.2" />
                                    </svg>
                                    <div style="font-family: var(--font-heading); font-size: 7.2rem; font-weight: 800; color: #2b2623; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 30px; text-align: center; line-height: 1.1; user-select: none; position: relative; z-index: 2;">
                                        Edge Cases
                                        <div style="font-size: 4.2rem; font-weight: 700; color: #e56b6f; letter-spacing: 0.16em; margin-top: 10px;">2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 6.8 CCS Circular Logo (Dark) -->
                <div class="card-container-wrapper">
                    <div class="card-label">
                        <div>CCS Circular Logo (Dark)<span class="dimensions">1080 x 1080</span></div>
                        <div class="card-actions">
                            <button class="card-action-btn" onclick="previewCard('logo-ccs-circle-dark')">👁️ Preview</button>
                            <button class="card-action-btn" onclick="saveCard('logo-ccs-circle-dark')">💾 Save PNG</button>
                        </div>
                    </div>
                    <div class="preview-scale-wrapper size-square-wrapper checkerboard-dark">
                        <div class="card-export-container size-square transparent-bg" id="logo-ccs-circle-dark" style="padding: 20px;">
                            <div class="card-content" style="justify-content: center; align-items: center; background: transparent;">
                                <div style="width: 1040px; height: 1040px; border-radius: 50%; background: #2b2623; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); border: 24px solid #faf9f5; position: relative; overflow: hidden;">
                                    <!-- Network Watermark Background -->
                                    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; color: #faf9f5;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                        <line x1="15" y1="20" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="15" y1="20" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="35" y1="45" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="35" y1="45" x2="55" y2="85" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="55" y1="85" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="80" y1="65" x2="90" y2="25" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="90" y1="25" x2="65" y2="15" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="65" y1="15" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="65" y1="15" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <circle cx="35" cy="45" r="6" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="80" cy="65" r="8" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="65" cy="15" r="5" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="15" cy="20" r="1.2" fill="currentColor" opacity="0.1" />
                                        <circle cx="35" cy="45" r="1.8" fill="currentColor" opacity="0.15" />
                                        <circle cx="10" cy="75" r="1.5" fill="currentColor" opacity="0.1" />
                                        <circle cx="55" cy="85" r="1.6" fill="currentColor" opacity="0.1" />
                                        <circle cx="80" cy="65" r="2" fill="currentColor" opacity="0.15" />
                                        <circle cx="90" cy="25" r="1.2" fill="currentColor" opacity="0.1" />
                                        <circle cx="65" cy="15" r="1.6" fill="currentColor" opacity="0.15" />
                                    </svg>
                                    
                                    <svg width="520" height="520" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: -30px; position: relative; z-index: 2;">
                                        <line x1="6" y1="24" x2="14" y2="20" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="6" y1="24" x2="10" y2="12" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="14" y1="20" x2="10" y2="12" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.8" stroke-dasharray="2.5 2.5" />
                                        <circle cx="6" cy="24" r="3.2" fill="#508484" />
                                        <circle cx="10" cy="12" r="3.2" fill="#6d597a" />
                                        <circle cx="14" cy="20" r="3.2" fill="#355070" />
                                        <circle cx="26" cy="8" r="4.8" fill="#e56b6f" stroke="#2b2623" stroke-width="1.2" />
                                    </svg>
                                    <div style="font-family: var(--font-heading); font-size: 7.2rem; font-weight: 800; color: #faf9f5; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 30px; text-align: center; line-height: 1.1; user-select: none; position: relative; z-index: 2;">
                                        Edge Cases
                                        <div style="font-size: 4.2rem; font-weight: 600; color: #e56b6f; letter-spacing: 0.16em; margin-top: 10px;">2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 6.9 CCS Square Logo (Light) -->
                <div class="card-container-wrapper">
                    <div class="card-label">
                        <div>CCS Square Logo (Light)<span class="dimensions">1080 x 1080</span></div>
                        <div class="card-actions">
                            <button class="card-action-btn" onclick="previewCard('logo-ccs-square-light')">👁️ Preview</button>
                            <button class="card-action-btn" onclick="saveCard('logo-ccs-square-light')">💾 Save PNG</button>
                        </div>
                    </div>
                    <div class="preview-scale-wrapper size-square-wrapper checkerboard-light">
                        <div class="card-export-container size-square transparent-bg" id="logo-ccs-square-light" style="padding: 20px;">
                            <div class="card-content" style="justify-content: center; align-items: center; background: transparent;">
                                <div style="width: 1040px; height: 1040px; border-radius: 120px; background: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(43, 38, 35, 0.1); border: 24px solid #2b2623; position: relative; overflow: hidden;">
                                    <!-- Network Watermark Background -->
                                    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; color: #8c827a;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                        <line x1="15" y1="20" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="15" y1="20" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="35" y1="45" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="35" y1="45" x2="55" y2="85" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="55" y1="85" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="80" y1="65" x2="90" y2="25" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="90" y1="25" x2="65" y2="15" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="65" y1="15" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <line x1="65" y1="15" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.08" />
                                        <circle cx="35" cy="45" r="6" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="80" cy="65" r="8" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="65" cy="15" r="5" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.1" />
                                        <circle cx="15" cy="20" r="1.2" fill="currentColor" opacity="0.15" />
                                        <circle cx="35" cy="45" r="1.8" fill="currentColor" opacity="0.2" />
                                        <circle cx="10" cy="75" r="1.5" fill="currentColor" opacity="0.15" />
                                        <circle cx="55" cy="85" r="1.6" fill="currentColor" opacity="0.15" />
                                        <circle cx="80" cy="65" r="2" fill="currentColor" opacity="0.2" />
                                        <circle cx="90" cy="25" r="1.2" fill="currentColor" opacity="0.15" />
                                        <circle cx="65" cy="15" r="1.6" fill="currentColor" opacity="0.2" />
                                    </svg>
                                    
                                    <svg width="520" height="520" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: -30px; position: relative; z-index: 2;">
                                        <line x1="6" y1="24" x2="14" y2="20" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="6" y1="24" x2="10" y2="12" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="14" y1="20" x2="10" y2="12" stroke="#8c827a" stroke-width="1.5" />
                                        <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.8" stroke-dasharray="2.5 2.5" />
                                        <circle cx="6" cy="24" r="3.2" fill="#508484" />
                                        <circle cx="10" cy="12" r="3.2" fill="#6d597a" />
                                        <circle cx="14" cy="20" r="3.2" fill="#355070" />
                                        <circle cx="26" cy="8" r="4.8" fill="#e56b6f" stroke="#ffffff" stroke-width="1.2" />
                                    </svg>
                                    <div style="font-family: var(--font-heading); font-size: 7.2rem; font-weight: 800; color: #2b2623; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 30px; text-align: center; line-height: 1.1; user-select: none; position: relative; z-index: 2;">
                                        Edge Cases
                                        <div style="font-size: 4.2rem; font-weight: 700; color: #e56b6f; letter-spacing: 0.16em; margin-top: 10px;">2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 6.10 CCS Square Logo (Dark) -->
                <div class="card-container-wrapper">
                    <div class="card-label">
                        <div>CCS Square Logo (Dark)<span class="dimensions">1080 x 1080</span></div>
                        <div class="card-actions">
                            <button class="card-action-btn" onclick="previewCard('logo-ccs-square-dark')">👁️ Preview</button>
                            <button class="card-action-btn" onclick="saveCard('logo-ccs-square-dark')">💾 Save PNG</button>
                        </div>
                    </div>
                    <div class="preview-scale-wrapper size-square-wrapper checkerboard-dark">
                        <div class="card-export-container size-square transparent-bg" id="logo-ccs-square-dark" style="padding: 20px;">
                            <div class="card-content" style="justify-content: center; align-items: center; background: transparent;">
                                <div style="width: 1040px; height: 1040px; border-radius: 120px; background: #2b2623; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); border: 24px solid #faf9f5; position: relative; overflow: hidden;">
                                    <!-- Network Watermark Background -->
                                    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; color: #faf9f5;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                        <line x1="15" y1="20" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="15" y1="20" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="35" y1="45" x2="10" y2="75" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="35" y1="45" x2="55" y2="85" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="55" y1="85" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="80" y1="65" x2="90" y2="25" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="90" y1="25" x2="65" y2="15" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="65" y1="15" x2="35" y2="45" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <line x1="65" y1="15" x2="80" y2="65" stroke="currentColor" stroke-width="0.4" opacity="0.06" />
                                        <circle cx="35" cy="45" r="6" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="80" cy="65" r="8" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="65" cy="15" r="5" stroke="currentColor" stroke-width="0.2" fill="none" opacity="0.08" />
                                        <circle cx="15" cy="20" r="1.2" fill="currentColor" opacity="0.1" />
                                        <circle cx="35" cy="45" r="1.8" fill="currentColor" opacity="0.15" />
                                        <circle cx="10" cy="75" r="1.5" fill="currentColor" opacity="0.1" />
                                        <circle cx="55" cy="85" r="1.6" fill="currentColor" opacity="0.1" />
                                        <circle cx="80" cy="65" r="2" fill="currentColor" opacity="0.15" />
                                        <circle cx="90" cy="25" r="1.2" fill="currentColor" opacity="0.1" />
                                        <circle cx="65" cy="15" r="1.6" fill="currentColor" opacity="0.15" />
                                    </svg>
                                    
                                    <svg width="520" height="520" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: -30px; position: relative; z-index: 2;">
                                        <line x1="6" y1="24" x2="14" y2="20" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="6" y1="24" x2="10" y2="12" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="14" y1="20" x2="10" y2="12" stroke="#faf9f5" stroke-dasharray="none" stroke-width="1.5" opacity="0.4" />
                                        <line x1="14" y1="20" x2="26" y2="8" stroke="#e56b6f" stroke-width="1.8" stroke-dasharray="2.5 2.5" />
                                        <circle cx="6" cy="24" r="3.2" fill="#508484" />
                                        <circle cx="10" cy="12" r="3.2" fill="#6d597a" />
                                        <circle cx="14" cy="20" r="3.2" fill="#355070" />
                                        <circle cx="26" cy="8" r="4.8" fill="#e56b6f" stroke="#2b2623" stroke-width="1.2" />
                                    </svg>
                                    <div style="font-family: var(--font-heading); font-size: 7.2rem; font-weight: 800; color: #faf9f5; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 30px; text-align: center; line-height: 1.1; user-select: none; position: relative; z-index: 2;">
                                        Edge Cases
                                        <div style="font-size: 4.2rem; font-weight: 600; color: #e56b6f; letter-spacing: 0.16em; margin-top: 10px;">2026</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

    </main>

"""

# Let's perform the replacement in Python
new_lines = lines[:start_idx] + [logos_html] + lines[modal_idx:]

with open(pr_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Replacement applied successfully!")
