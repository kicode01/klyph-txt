"""
Generate the Four Titan Concepts for Klyph:
1. THREADS Archetype  : The Infinite Editorial Ribbon (Single continuous fluid line)
2. TIKTOK Archetype   : The Chromatic Cadence Wave (High-energy chromatic vibration)
3. INSTAGRAM Archetype: The Distilled Chisel Lens & Spark (Iconic squircle, lens, and golden spark)
4. FACEBOOK Archetype : The Monumental Grounded Monogram (Asymmetric, bold, grounded authority)
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "titans_final")
os.makedirs(DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. THREADS Archetype: The Infinite Ribbon
# A single continuous silky line with constant thickness (24px) and rounded caps.
# Traces an unbroken loop: vertical ascender -> sweeping crown arch ->
# descending focal loop -> soaring exit kick with an embedded golden focal nucleus.
# -----------------------------------------------------------------------------
def icon_threads(dark=True):
    bg = "#080b10" if dark else "#f8fafc"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph - The Infinite Ribbon (Threads Archetype)"
    
    # Mathematical curve:
    # Canvas 256x256.
    # Start at (76, 196) -> vertical stem up to (76, 80)
    # Crown arc: C 76 48, 108 44, 128 64
    # Descends into waist: C 144 80, 114 116, 126 128
    # Loops around upper right: C 138 140, 168 84, 188 64
    # Arch at top-right: C 204 48, 214 68, 200 88
    # Sweeps down to kick: C 182 116, 140 148, 132 154 L 192 196
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t-threads-title">
  <title id="t-threads-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Continuous Fluid Ribbon Stroke -->
  <path d="M 76 196 L 76 80 C 76 50 106 44 126 62 C 146 80 116 116 126 128 C 138 142 168 84 188 64 C 204 48 214 68 200 88 C 182 116 142 146 132 154 L 192 196" fill="none" stroke="{cyan}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Embedded Golden Core -->
  <circle cx="126" cy="128" r="9" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 2. TIKTOK Archetype: The Chromatic Cadence Wave
# Aerodynamic supersonic quill/rhythm glyph with high forward velocity (15-deg lean).
# Features TikTok's signature 3-layer chromatic offset:
# - Layer 1: Electric Cyan (#00f0ff) shifted (-4px, +3px)
# - Layer 2: Neon Magenta / Coral (#ff0055) shifted (+4px, -3px)
# - Layer 3: Brilliant Crisp White (#ffffff) core anchor
# - Central Golden Diamond Pulse (#f59e0b)
# -----------------------------------------------------------------------------
def icon_tiktok(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff"
    coral = "#ff0055" if dark else "#f43f5e"
    core = "#ffffff" if dark else "#0f172a"
    amber = "#f59e0b"
    title = "Klyph - The Chromatic Cadence (TikTok Archetype)"
    
    # Exact snapped 45-deg and 90-deg coordinates:
    # Pillar: M 66 48 L 102 48 L 82 208 L 46 208 Z (slanted parallelogram)
    # Upper blade: M 116 128 L 188 56 L 224 56 L 152 128 Z
    # Lower wing:  M 152 128 L 224 200 L 188 200 L 116 128 Z
    glyph = '''<path d="M 66 48 L 102 48 L 82 208 L 46 208 Z M 116 128 L 188 56 L 224 56 L 152 128 Z M 152 128 L 224 200 L 188 200 L 116 128 Z"/>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t-tiktok-title">
  <title id="t-tiktok-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Cyan Chromatic Fringe (-4px, +3px) -->
  <g transform="translate(-4, 3)" fill="{cyan}" opacity="0.85">
    {glyph}
  </g>
  <!-- Coral Chromatic Fringe (+4px, -3px) -->
  <g transform="translate(4, -3)" fill="{coral}" opacity="0.85">
    {glyph}
  </g>
  <!-- Core White Silhouette -->
  <g fill="{core}">
    {glyph}
  </g>
  <!-- Luminous Golden Pulse -->
  <polygon points="116,128 134,110 152,128 134,146" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 3. INSTAGRAM Archetype: The Distilled Chisel Lens & Spark
# Extreme graphic reduction inspired by Instagram's Squircle + Lens + Flash.
# Composed of 3 pure geometric elements:
# 1. Outer continuous squircle boundary (stroke 18px)
# 2. Concentric circular aperture lens (r=46px, stroke 18px) with internal 45-deg chisel notch
# 3. Radiant golden spark dot at (180, 76) r=14
# -----------------------------------------------------------------------------
def icon_instagram(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph - The Chisel Lens and Spark (Instagram Archetype)"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t-ig-title">
  <title id="t-ig-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Outer Minimalist Squircle Boundary -->
  <rect x="42" y="42" width="172" height="172" rx="48" fill="none" stroke="{cyan}" stroke-width="18"/>
  <!-- Concentric Editorial Aperture Lens -->
  <circle cx="128" cy="128" r="46" fill="none" stroke="{cyan}" stroke-width="18"/>
  <!-- Internal 45-deg Chisel Notch (Editorial Chevron) -->
  <path d="M 128 128 L 156 100 M 128 128 L 156 156" fill="none" stroke="{cyan}" stroke-width="16" stroke-linecap="round"/>
  <!-- Radiant Golden Spark (Human Insight & Clarity) -->
  <circle cx="180" cy="76" r="14" fill="{amber}"/>
</svg>'''


# -----------------------------------------------------------------------------
# 4. FACEBOOK Archetype: The Monumental Grounded Monogram
# Inspired by Facebook's iconic off-center, heavyweight 'f' grounded to the lower boundary.
# A commanding, ultra-bold, modern monogram with massive silhouette weight:
# - Foundation pillar on the left (w=42) rising from y=38 to y=218 (grounded)
# - Upper 45-deg soaring chisel blade
# - Lower 45-deg grounded anchor leg
# - Interlocking golden keystone jewel connecting the blades at the focal center
# -----------------------------------------------------------------------------
def icon_facebook(dark=True):
    bg = "#080b10" if dark else "#0284c7"
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    glyph_col = "#00f0ff" if dark else "#ffffff"
    amber = "#f59e0b"
    title = "Klyph - The Monumental Grounded Monogram (Facebook Archetype)"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t-fb-title">
  <title id="t-fb-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Asymmetric Foundation Pillar -->
  <rect x="52" y="38" width="42" height="180" rx="10" fill="{glyph_col}"/>
  <!-- Upper Soaring 45-deg Chisel Blade -->
  <path d="M 104 128 L 180 52 H 220 L 144 128 Z" fill="{glyph_col}"/>
  <!-- Lower Grounded 45-deg Anchor Leg -->
  <path d="M 144 128 L 220 204 H 180 L 104 128 Z" fill="{glyph_col}"/>
  <!-- Interlocking Luminous Golden Keystone -->
  <polygon points="104,128 124,108 144,128 124,148" fill="{amber}"/>
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


ICONS = [
    ("icon-threads", icon_threads),
    ("icon-tiktok", icon_tiktok),
    ("icon-instagram", icon_instagram),
    ("icon-facebook", icon_facebook),
]

for name, fn in ICONS:
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

print("Four Titan Icons generated in", DIR)
