"""
Generate 'Yellow Fill' Variations for Concept A (Grounded Monogram):
1. V1: Full Triangular Wedge Fill (Yellow fills the entire inner crook between pillar and diagonals)
2. V2: Full Letter K Yellow Fill (The entire letter K is vibrant yellow)
3. V3: Dual-Tone Fill (Vertical pillar white, diagonal blades yellow)
4. V4: Flush Interlocking Diamond Fill (Diamond expanded to touch the stroke edges seamlessly)
5. V5: Arrowhead / Counter-space Fill (Yellow fills the forward-pointing triangle between the arms)
"""

import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "yellow_fills")
os.makedirs(DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# Base Colors from user screenshot:
# Blue background: #0284c7 (or rich meta blue #0077e6)
# White: #ffffff
# Yellow/Amber: #f59e0b (or #fbb01b / #eab308)
# -----------------------------------------------------------------------------
BG_BLUE = "#0284c7"
BG_DARK = "#080b10"
WHITE = "#ffffff"
CYAN = "#00f0ff"
YELLOW = "#f59e0b"

# V1: Full Triangular Wedge Fill (Yellow fills the entire crook between stem and arms)
def v1_wedge(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # White K:
    # Stem: M 54 44 H 96 V 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 V 216 H 54 Z
    # Wedge: from (96, 92) to (132, 128) to (96, 164) and back to (96, 92)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Letter K -->
  <path d="M 54 44 H 96 V 216 H 54 Z M 96 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 Z" fill="{k_col}"/>
  <!-- Yellow Full Wedge Fill (Filling the entire triangular crook) -->
  <polygon points="96,92 132,128 96,164" fill="{YELLOW}"/>
</svg>'''

# V2: Full Letter K Yellow Fill (The entire K is golden yellow)
def v2_full_k(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Entire Letter K Filled with Yellow -->
  <path d="M 54 44 H 96 V 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 V 216 H 54 Z" fill="{YELLOW}"/>
  <!-- White Inset Core Jewel -->
  <polygon points="96,128 114,110 132,128 114,146" fill="{WHITE}"/>
</svg>'''

# V3: Dual-Tone Fill (Stem is White, Diagonals are Yellow)
def v3_dual_tone(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    stem_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- White Foundation Pillar -->
  <rect x="54" y="44" width="42" height="172" rx="0" fill="{stem_col}"/>
  <!-- Yellow Soaring Diagonals -->
  <path d="M 96 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 Z" fill="{YELLOW}"/>
  <!-- Keystone Diamond -->
  <polygon points="96,128 114,110 132,128 114,146" fill="{stem_col}"/>
</svg>'''

# V4: Seamless Flush Diamond (Diamond scaled and aligned so it connects perfectly across the joint)
def v4_flush_diamond(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # Diamond scaled to (88, 128) to (128, 88) to (168, 128) to (128, 168)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Base Grounded K -->
  <path d="M 54 44 H 96 V 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 V 216 H 54 Z" fill="{k_col}"/>
  <!-- Large Flush Yellow Keystone (Filling the entire junction) -->
  <polygon points="96,128 128,96 160,128 128,160" fill="{YELLOW}"/>
</svg>'''

# V5: Arrowhead Counter-space (Yellow fills the forward triangle between the two diagonal arms)
def v5_arrowhead(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Base Grounded K -->
  <path d="M 54 44 H 96 V 114 L 166 44 H 216 L 132 128 L 220 216 H 170 L 96 142 V 216 H 54 Z" fill="{k_col}"/>
  <!-- Yellow Arrowhead in Forward Negative Space -->
  <polygon points="132,128 216,44 220,216" fill="{YELLOW}" opacity="0.95"/>
  <!-- Central Inset Core -->
  <polygon points="96,128 114,110 132,128 114,146" fill="{k_col}"/>
</svg>'''

VARIANTS = [
    ("v1-wedge", v1_wedge),
    ("v2-full-k", v2_full_k),
    ("v3-dual-tone", v3_dual_tone),
    ("v4-flush-diamond", v4_flush_diamond),
    ("v5-arrowhead", v5_arrowhead),
]

for name, fn in VARIANTS:
    # Save light (matching user screenshot)
    with open(os.path.join(DIR, f"{name}-light.svg"), "w", encoding="utf-8") as f:
        f.write(fn(dark=False))
    # Save dark
    with open(os.path.join(DIR, f"{name}-dark.svg"), "w", encoding="utf-8") as f:
        f.write(fn(dark=True))

print("Yellow fill variations written to", DIR)
