import os

pr_path = "/Users/phileasdazeleygaist/Desktop/My Websites/edge-cases-2026/pr.html"

with open(pr_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's find the start line (1-indexed 2397 is 0-indexed 2396)
# We look for "<!-- 6.7 CCS Circular Logo (Light) -->"
start_idx = -1
for idx, line in enumerate(lines):
    if "<!-- 6.7 CCS Circular Logo (Light) -->" in line:
        start_idx = idx
        break

# Let's find the end line of 6.12 CCS Square Logo (Coral)
# It should end with </div> of the card container wrapper
end_idx = -1
for idx in range(start_idx, len(lines)):
    if "<!-- 6.12" in lines[idx] or "logo-ccs-square-coral" in lines[idx]:
        # find the next closing tags that end the section
        # The next few divs close:
        # </div> for card-content
        # </div> for card-export-container
        # </div> for preview-scale-wrapper
        # </div> for card-container-wrapper
        # Let's count them or search for the next "</div>" blocks
        pass

# Since we know it starts at start_idx and the next section is the preview modal (around line 2594/2600):
modal_idx = -1
for idx in range(start_idx, len(lines)):
    if "<!-- Fullscreen Isolated Preview Modal Dialog -->" in lines[idx]:
        modal_idx = idx
        break

# The lines we want to replace are between start_idx and the empty line before modal_idx
# Let's backtrack from modal_idx to find the end of the cards grid
end_idx = modal_idx
while end_idx > start_idx:
    if "</main>" in lines[end_idx] or "</div>" in lines[end_idx]:
        # we want to keep the closing divs of the grid/tab panel
        # Let's trace it:
        # Line 2593 is </div> (card-container-wrapper)
        # Line 2594 is (empty line)
        # Line 2595 is </div> (cards-grid)
        # Line 2596 is </div> (tab-panel)
        # Line 2597 is (empty line)
        # Line 2598 is </main>
        # Line 2599 is (empty line)
        # Line 2600 is <!-- Fullscreen Isolated Preview Modal Dialog -->
        # So the cards section ends at index corresponding to line 2593, which is 0-indexed 2592.
        # Let's verify by searching backwards for "logo-ccs-square-coral" and then counting closing divs.
        break

# Let's just find the index of "logo-ccs-square-coral" and go down to its container's closing div.
coral_idx = -1
for idx in range(start_idx, len(lines)):
    if 'id="logo-ccs-square-coral"' in lines[idx]:
        coral_idx = idx
        break

div_count = 0
target_end_idx = -1
# We are inside the wrapper div. Let's find the closing tag of card-container-wrapper.
# The card-container-wrapper starts at:
# <div class="card-container-wrapper"> (above coral_idx)
# Let's find where it starts
wrapper_start = -1
for idx in range(coral_idx, start_idx, -1):
    if 'class="card-container-wrapper"' in lines[idx]:
        wrapper_start = idx
        break

# Now search forward from wrapper_start to find the matching closing div for card-container-wrapper
open_divs = 0
for idx in range(wrapper_start, len(lines)):
    if "<div" in lines[idx]:
        open_divs += lines[idx].count("<div")
    if "</div" in lines[idx]:
        open_divs -= lines[idx].count("</div")
    if open_divs == 0:
        target_end_idx = idx
        break

print(f"Start Index: {start_idx} (Line {start_idx+1})")
print(f"End Index: {target_end_idx} (Line {target_end_idx+1})")

# Let's print the lines we are replacing to double check
print("First line to replace:", lines[start_idx].strip())
print("Last line to replace:", lines[target_end_idx].strip())
