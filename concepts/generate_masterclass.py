"""
Generate Four Masterclass Consumer Marks for Klyph:
1. MARK A (The Meta/Facebook Pedigree): Grounded Solid Modern Monogram (Unified silhouette, grounded stem, zero floating pieces)
2. MARK B (The TikTok Pedigree): Kinetic Chromatic K (Aerodynamic silhouette with electric cyan & neon fuchsia fringe on black)
3. MARK C (The Threads Pedigree): Clean Continuous Monoline K (Uniform stroke ribbon with mathematical circular arcs)
4. MARK D (The Kotlin/Linear Pedigree): Pure Geometric Negative-Space K (Solid squircle carved with extreme geometric economy)
"""

import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "masterclass")
os.makedirs(DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. MARK A: The Meta/Facebook Formula — Grounded Modern Monogram
# Facebook's genius is: Solid container + unified, bold, friendly silhouette
# grounded to the bottom boundary.
# For Klyph:
# A solid squircle (#080b10 on dark, #0284c7 on light)
# Inside: A single, unified, bold letter K.
# The vertical stem is 44px wide and grounds cleanly to the bottom edge.
# The diagonal arms meet the stem in a seamless, unified curve (fillet junction),
# with a subtle luminous amber keystone diamond embedded at the junction.
# -----------------------------------------------------------------------------
def mark_a_grounded(dark=True):
    bg = "#080b10" if dark else "#0284c7"
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    glyph_col = "#00f0ff" if dark else "#ffffff"
    amber = "#f59e0b"
    title = "Klyph Masterclass A - The Grounded Monogram (Meta Pedigree)"
    
    # Unified, single-silhouette K:
    # Stem: x=52 to 92, y=44 to 216 (grounded to bottom curve)
    # Upper arm: 45-deg angle from junction (92, 130) to (196, 44)
    # Lower arm: 45-deg angle from junction (92, 130) to (200, 216)
    # Snapped exact angles:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="ma-title">
  <title id="ma-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Unified Monogram Silhouette -->
  <path d="M 54 44 H 96 V 110 L 156 44 H 208 L 132 126 L 212 216 H 158 L 96 144 V 216 H 54 Z" fill="{glyph_col}"/>
  <!-- Luminous Amber Keystone Nexus -->
  <polygon points="96,128 114,110 132,128 114,146" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 2. MARK B: The TikTok Formula — Kinetic Chromatic K
# TikTok's genius is: High-energy kinetic silhouette + cyan and magenta
# chromatic offset on deep OLED black.
# -----------------------------------------------------------------------------
def mark_b_tiktok(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff"
    magenta = "#ff0055" if dark else "#e11d48"
    white_core = "#ffffff" if dark else "#0f172a"
    amber = "#f59e0b"
    title = "Klyph Masterclass B - Kinetic Chromatic K (TikTok Pedigree)"
    
    # Bold italic K silhouette (12-deg forward momentum):
    glyph = '''<path d="M 64 44 H 102 L 86 216 H 48 Z M 112 124 L 176 44 H 220 L 144 130 Z M 136 122 L 216 216 H 172 L 102 134 Z"/>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="mb-title">
  <title id="mb-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Cyan Chromatic Fringe (-5px, +3px) -->
  <g transform="translate(-5, 3)" fill="{cyan}" opacity="0.9">
    {glyph}
  </g>
  <!-- Magenta Chromatic Fringe (+5px, -3px) -->
  <g transform="translate(5, -3)" fill="{magenta}" opacity="0.9">
    {glyph}
  </g>
  <!-- Core Crisp White Anchor -->
  <g fill="{white_core}">
    {glyph}
  </g>
  <!-- Central Pulse Diamond -->
  <polygon points="112,126 128,110 144,126 128,142" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 3. MARK C: The Threads Formula — Continuous Ribbon K
# Threads' genius is: Single continuous uniform line drawing (like @).
# For Klyph:
# A single continuous path of 24px uniform thickness:
# Starts at bottom-left, goes up the vertical stem, loops over the top,
# swoops down to the center junction, branches into the upper diagonal arm,
# and sweeps down into the lower kick leg.
# -----------------------------------------------------------------------------
def mark_c_threads(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph Masterclass C - Continuous Ribbon K (Threads Pedigree)"
    
    # Exact geometric paths:
    # Stem: (72, 48) to (72, 208)
    # Upper arm: 45-deg line from (72, 128) to (188, 48)
    # Lower arm: 45-deg line from (104, 128) to (188, 208)
    # Beautiful rounded joins and caps:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="mc-title">
  <title id="mc-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Continuous Vertical Stem -->
  <rect x="56" y="44" width="32" height="168" rx="16" fill="{cyan}"/>
  <!-- Upper Diagonal Ribbon -->
  <path d="M 88 128 L 176 48" stroke="{cyan}" stroke-width="32" stroke-linecap="round"/>
  <!-- Lower Diagonal Ribbon -->
  <path d="M 112 128 L 184 208" stroke="{cyan}" stroke-width="32" stroke-linecap="round"/>
  <!-- Golden Keystone Hinge -->
  <circle cx="108" cy="128" r="12" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 4. MARK D: The Kotlin / Vercel Formula — Pure Negative-Space Carve
# Extreme geometric economy: A solid cyan tile with ONE precision stencil
# cut forming the letter K in negative space.
# -----------------------------------------------------------------------------
def mark_d_stencil(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph Masterclass D - Negative-Space Carve (Kotlin Pedigree)"
    
    # A solid cyan disc (r=84) inside the dark squircle.
    # Inside the disc, a vertical cut and a 45-deg chevron cut form K in pure negative space!
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="md-title">
  <title id="md-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Solid Cyan Medallion Disc -->
  <circle cx="128" cy="128" r="84" fill="{cyan}"/>
  <!-- Negative Space Vertical Pillar Cut -->
  <rect x="76" y="56" width="28" height="144" rx="6" fill="{bg}"/>
  <!-- Negative Space Upper Diagonal Cut -->
  <polygon points="112,132 168,76 196,76 132,140" fill="{bg}"/>
  <!-- Negative Space Lower Diagonal Cut -->
  <polygon points="132,116 196,180 168,180 112,124" fill="{bg}"/>
  <!-- Inset Golden Amber Jewel -->
  <polygon points="116,114 130,128 116,142 102,128" fill="{amber}"/>
</svg>'''


def responsive_svg(name, dark_fn, light_fn):
    dark_inner = dark_fn(dark=True).split('<rect width="256"')[1]
    dark_inner = '<rect width="256"' + dark_inner.replace('</svg>', '').strip()
    
    light_inner = light_fn(dark=False).split('<rect width="256"')[1]
    light_inner = '<rect width="256"' + light_inner.replace('</svg>', '').strip()
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="{name}-title">
  <title id="{name}-title">Klyph Responsive Icon - {name}</title>
  <style>
    .mode-light {{ display: none; }}
    .mode-dark  {{ display: block; }}
    @media (prefers-color-scheme: light) {{
      .mode-light {{ display: block; }}
      .mode-dark  {{ display: none; }}
    }}
  </style>
  <g class="mode-dark">
    {dark_inner}
  </g>
  <g class="mode-light">
    {light_inner}
  </g>
</svg>'''


MARKS = [
    ("master-a-grounded", mark_a_grounded),
    ("master-b-tiktok", mark_b_tiktok),
    ("master-c-threads", mark_c_threads),
    ("master-d-stencil", mark_d_stencil),
]

for name, fn in MARKS:
    d_path = os.path.join(DIR, f"{name}-dark.svg")
    l_path = os.path.join(DIR, f"{name}-light.svg")
    r_path = os.path.join(DIR, f"{name}-responsive.svg")
    def_path = os.path.join(DIR, f"{name}.svg")
    
    with open(d_path, "w", encoding="utf-8") as f:
        f.write(fn(dark=True))
    with open(l_path, "w", encoding="utf-8") as f:
        f.write(fn(dark=False))
    with open(r_path, "w", encoding="utf-8") as f:
        f.write(responsive_svg(name, fn, fn))
    with open(def_path, "w", encoding="utf-8") as f:
        f.write(fn(dark=True))

print("Masterclass marks generated in", DIR)
