import os

pr_path = "/Users/phileasdazeleygaist/Desktop/My Websites/edge-cases-2026/pr.html"

with open(pr_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the DOMContentLoaded fetch block
old_dom_content_load = """            fetch('data/speakers.json')
                .then(res => res.json())
                .then(speakers => {
                    renderDynamicPR(speakers);
                    
                    // Route to specific tab from hash if present
                    const hash = window.location.hash.substring(1);
                    if (hash && document.getElementById(hash)) {
                        switchTab(hash);
                    }
                })
                .catch(err => {
                    console.error('Failed to load speakers for PR dynamic rendering:', err);
                });"""

new_dom_content_load = """            Promise.all([
                fetch('data/speakers.json').then(res => res.json()),
                fetch('data/settings.json').then(res => res.json()).catch(() => ({}))
            ])
            .then(([speakers, settings]) => {
                renderDynamicPR(speakers, settings);
                
                // Route to specific tab from hash if present
                const hash = window.location.hash.substring(1);
                if (hash && document.getElementById(hash)) {
                    switchTab(hash);
                }
            })
            .catch(err => {
                console.error('Failed to load data for PR dynamic rendering:', err);
            });"""

if old_dom_content_load not in content:
    print("Error: DOMContentLoaded fetch block not found in pr.html!")
    exit(1)

content = content.replace(old_dom_content_load, new_dom_content_load)

# Now let's locate function renderDynamicPR(speakers)
start_str = "        function renderDynamicPR(speakers) {"
end_str = "        // Columns layout (Stripe Columns Banner)" # we can replace in pieces, or replace the entire renderDynamicPR

# To be safe, let's find function renderDynamicPR(speakers) and replace the whole function up to the closing tag of script or similar.
# Let's inspect the exact lines of renderDynamicPR in pr.html and replace it.
# We will read lines and locate line indices.
with open(pr_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Part 1 (Fetch) applied successfully!")
