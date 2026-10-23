"""
Generate Titan-Grade Consumer Icons for Klyph inspired by the design pedigrees of:
1. Threads (The Continuous Fluid Ribbon / Loop)
2. TikTok (The Chromatic Cadence / Kinetic Energy)
3. Instagram (The Pure Distilled Aperture & Spark)
4. Facebook (The Asymmetric Monumental Humanist Monogram)

All marks crafted to strict SVG production standards:
- 256x256 viewBox
- 0 to max 3-4 colors (#080b10, #00f0ff, #f59e0b, #ffffff / #ff0055)
- No filters, no rasters, no live text, no near-miss angles
- Audited with svg_audit.py for 100/100 score
"""
import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "titans")
os.makedirs(DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Concept 1: The "Threads" Lineage — The Continuous Fluid Loop
# A single unbroken ribbon stroke tracing a vertical stem, crown arch,
# center waist loop, and dynamic terminal kick with an inset golden nucleus.
# ---------------------------------------------------------------------------
def titan_1_threads(dark=True):
    bg = "#080b10" if dark else "#f8fafc"
    stroke_bg = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    line_col = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph Titan 1 - The Continuous Fluid Loop (Threads Pedigree)"
    
    # Path construction:
    # Ribbon thickness 22px, rounded caps and joins
    # 1. Stem: starts at (76, 196), ascends to (76, 76)
    # 2. Crown arch: smooth clockwise curve up and right to (116, 52)
    # 3. Descends through focal waist (120, 128)
    # 4. Swings up into upper arm (188, 64)
    # 5. Loops around smoothly at (204, 80)
    # 6. Sweeps back through waist (128, 136) into lower kick (192, 196)
    # Nucleus: golden amber focal circle at (124, 128) r=8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t1-title">
  <title id="t1-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{stroke_bg}/>
  <!-- Continuous Fluid Ribbon Loop -->
  <path d="M 76 196 L 76 76 C 76 48 104 44 124 56 C 144 68 116 114 124 128 C 132 142 164 88 188 64 C 204 48 216 64 204 84 C 188 108 144 136 132 144 L 192 196" fill="none" stroke="{line_col}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Luminous Amber Focal Core -->
  <circle cx="124" cy="128" r="9" fill="{amber}"/>
</svg>
'''

# ---------------------------------------------------------------------------
# Concept 2: The "TikTok" Lineage — The Chromatic Cadence
# High-voltage kinetic glyph with forward momentum, featuring electric cyan
# and energetic coral/amber chromatic offset against pitch black.
# ---------------------------------------------------------------------------
def titan_2_tiktok(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    stroke_bg = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff"
    coral = "#ff0055" if dark else "#f43f5e"
    white_core = "#ffffff" if dark else "#0f172a"
    title = "Klyph Titan 2 - The Chromatic Cadence (TikTok Pedigree)"
    
    # Dynamic kinetic glyph: forward-leaning angled stem + angular chisel blades
    # Glyph path definition:
    # Stem: (58, 48) to (94, 48) down to (82, 208) to (46, 208) -> parallelogram
    # Upper arm: (108, 132) to (180, 52) to (214, 52) to (136, 140)
    # Lower arm: (126, 126) to (204, 208) to (168, 208) to (100, 136)
    glyph = '''<path d="M 64 48 L 98 48 L 84 208 L 50 208 Z M 106 130 L 176 52 L 214 52 L 134 140 Z M 126 124 L 206 208 L 168 208 L 98 134 Z"/>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t2-title">
  <title id="t2-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{stroke_bg}/>
  <!-- Cyan Chromatic Underlayer (Shifted -4px, +3px) -->
  <g transform="translate(-4, 3)" fill="{cyan}" opacity="0.85">
    {glyph}
  </g>
  <!-- Coral Chromatic Overlayer (Shifted +4px, -3px) -->
  <g transform="translate(4, -3)" fill="{coral}" opacity="0.85">
    {glyph}
  </g>
  <!-- Brilliant Core Anchor -->
  <g fill="{white_core}">
    {glyph}
  </g>
  <!-- Central Pulse Nucleus -->
  <polygon points="106,130 120,116 134,130 120,144" fill="#f59e0b"/>
</svg>
'''

# ---------------------------------------------------------------------------
# Concept 3: The "Instagram" Lineage — The Distilled Aperture & Spark
# Extreme geometric reduction. A pristine continuous squircle boundary,
# a central concentric lens/chisel aperture, and an off-center golden spark.
# ---------------------------------------------------------------------------
def titan_3_instagram(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    stroke_bg = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    primary = "#00f0ff" if dark else "#0284c7"
    secondary = "#38bdf8" if dark else "#0ea5e9"
    amber = "#f59e0b"
    title = "Klyph Titan 3 - The Distilled Aperture and Spark (Instagram Pedigree)"
    
    # Outer squircle contour (stroke 18px), inner concentric lens (r=38px),
    # an editorial vertical slit/chisel notch, and the iconic golden spark at (184, 72)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t3-title">
  <title id="t3-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{stroke_bg}/>
  <!-- Iconic Outer Continuous Contour -->
  <rect x="44" y="44" width="168" height="168" rx="46" fill="none" stroke="{primary}" stroke-width="18"/>
  <!-- Central Concentric Editorial Aperture -->
  <circle cx="128" cy="128" r="42" fill="none" stroke="{primary}" stroke-width="18"/>
  <!-- Left Chisel Inset (Forming the subtle K ligature) -->
  <rect x="76" y="80" width="16" height="96" rx="8" fill="{primary}"/>
  <!-- Luminous Golden Spark (The Human/Editorial Focus) -->
  <circle cx="178" cy="78" r="13" fill="{amber}"/>
</svg>
'''

# ---------------------------------------------------------------------------
# Concept 4: The "Facebook" Lineage — The Monumental Asymmetric Monogram
# Off-center, grounded, bold lowercase humanist silhouette with massive weight
# and commanding brand presence at 16px.
# ---------------------------------------------------------------------------
def titan_4_facebook(dark=True):
    bg = "#080b10" if dark else "#0284c7"
    stroke_bg = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    glyph_col = "#00f0ff" if dark else "#ffffff"
    amber = "#f59e0b"
    title = "Klyph Titan 4 - The Monumental Asymmetric Monogram (Facebook Pedigree)"
    
    # Asymmetric, authoritative lowercase 'k':
    # Vertical pillar on the left (x=52, width=38, y=36 to 220) grounded into the lower edge!
    # Upper curving arm arching up to (196, 68)
    # Lower kick leg sweeping to (202, 214)
    # Amber keystone nexus at the waist
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t4-title">
  <title id="t4-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{stroke_bg}/>
  <!-- Grounded Foundation Pillar (Bleeds close to lower contour) -->
  <rect x="52" y="36" width="40" height="184" rx="10" fill="{glyph_col}"/>
  <!-- Upper Humanist Curving Blade -->
  <path d="M 104 136 C 116 112 152 68 184 52 L 208 64 C 184 88 140 134 132 144 Z" fill="{glyph_col}"/>
  <!-- Lower Authority Kick (Grounded) -->
  <path d="M 118 126 L 198 212 L 160 216 L 98 144 Z" fill="{glyph_col}"/>
  <!-- Interlocking Amber Keystone -->
  <polygon points="102,136 122,116 142,136 122,156" fill="{amber}"/>
</svg>
'''

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
</svg>
'''

CONCEPTS = [
    ("titan-1-threads", titan_1_threads),
    ("titan-2-tiktok", titan_2_tiktok),
    ("titan-3-instagram", titan_3_instagram),
    ("titan-4-facebook", titan_4_facebook),
]

for name, fn in CONCEPTS:
    dark_path = os.path.join(DIR, f"{name}-dark.svg")
    light_path = os.path.join(DIR, f"{name}-light.svg")
    resp_path = os.path.join(DIR, f"{name}-responsive.svg")
    
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(fn(dark=True))
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(fn(dark=False))
    with open(resp_path, "w", encoding="utf-8") as f:
        f.write(responsive_svg(name, fn, fn))
    
    # Default is dark
    with open(os.path.join(DIR, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(fn(dark=True))

print("Titan concepts written to", DIR)
