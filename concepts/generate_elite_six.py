"""
Generate Elite Six Concepts for Klyph with 100/100 Geometric Snapping:
1. The Seamless Humanist Loop (Airbnb/Threads pedigree - organic unbroken ribbon)
2. The Cadence Pulse (Spotify/Kinetic Waves meet Letter K - exact 45-deg chevrons)
3. The Supersonic Quill Wing (Apple/Linear - aerodynamic 45-deg feather/blade)
4. The Crystalline Prism (OpenAI/Linear pedigree - 3D faceted editorial keystones)
5. The Stencil Ingot Medallion (Beats/Target pedigree - negative space carved cyan medallion)
6. The Proofreader's Check (Grammarly/Nike pedigree - fluid loop snapping into 45-deg razor check)
"""

import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "elite_six")
os.makedirs(DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. The Seamless Humanist Loop (Airbnb / Threads)
# -----------------------------------------------------------------------------
def concept_1_humanist_loop(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph 1 - The Seamless Humanist Loop"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c1-title">
  <title id="c1-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Continuous Organic Ribbon -->
  <path d="M 76 196 L 76 80 C 76 50 106 44 126 62 C 146 80 116 116 126 128 C 138 142 168 84 188 64 C 204 48 214 68 200 88 C 182 116 142 146 132 154 L 192 196" fill="none" stroke="{cyan}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Amber Focal Core -->
  <circle cx="126" cy="128" r="9" fill="{amber}"/>
</svg>'''

# -----------------------------------------------------------------------------
# 2. The Cadence Pulse (Spotify / Kinetic Waves meet Letter K)
# Exact 45.0-deg chevron snapping (dx=60, dy=60)
# -----------------------------------------------------------------------------
def concept_2_cadence_pulse(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    lapis = "#0284c7" if dark else "#0369a1"
    amber = "#f59e0b"
    title = "Klyph 2 - The Cadence Pulse"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c2-title">
  <title id="c2-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Vertical Foundation Pillar -->
  <rect x="52" y="44" width="36" height="168" rx="8" fill="{cyan}"/>
  <!-- Inner Kinetic 45-deg Chevron -->
  <path d="M 176 68 L 116 128 L 176 188" fill="none" stroke="{cyan}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Outer Acceleration 45-deg Wave -->
  <path d="M 216 68 L 156 128 L 216 188" fill="none" stroke="{lapis}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Radiant Amber Spark Nucleus -->
  <polygon points="116,128 126,118 136,128 126,138" fill="{amber}"/>
</svg>'''

# -----------------------------------------------------------------------------
# 3. The Supersonic Quill Wing (Aerodynamic 45-deg feather/blade)
# Snapped to exact 45-deg and 90-deg coordinates
# -----------------------------------------------------------------------------
def concept_3_quill_wing(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    lapis = "#0284c7" if dark else "#0369a1"
    amber = "#f59e0b"
    title = "Klyph 3 - The Supersonic Quill Wing"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c3-title">
  <title id="c3-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Upper Aerodynamic Wing Blade -->
  <path d="M 64 192 L 192 64 C 180 110 150 144 128 152 Z" fill="{cyan}"/>
  <!-- Lower Chisel Foundation Facet -->
  <path d="M 64 192 L 128 152 C 110 180 86 196 64 192 Z" fill="{lapis}"/>
  <!-- Precision Editorial Slit -->
  <line x1="64" y1="192" x2="192" y2="64" stroke="{bg}" stroke-width="6" stroke-linecap="round"/>
  <!-- Golden Amber Ink Core -->
  <circle cx="128" cy="128" r="10" fill="{amber}"/>
</svg>'''

# -----------------------------------------------------------------------------
# 4. The Crystalline Prism (OpenAI / Linear / Dimensional)
# -----------------------------------------------------------------------------
def concept_4_crystalline_prism(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    lapis = "#0284c7" if dark else "#0369a1"
    amber = "#f59e0b"
    title = "Klyph 4 - The Crystalline Prism"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c4-title">
  <title id="c4-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Vertical Foundation Prism -->
  <rect x="52" y="44" width="38" height="168" rx="8" fill="{cyan}"/>
  <!-- Upper Soaring 45-deg Crystal Facet -->
  <polygon points="104,128 180,52 216,52 140,128" fill="{cyan}"/>
  <!-- Lower Depth Facet (Lapis) -->
  <polygon points="140,128 216,204 180,204 104,128" fill="{lapis}"/>
  <!-- Interlocking Golden Amber Keystone Jewel -->
  <polygon points="104,128 126,106 148,128 126,150" fill="{amber}"/>
</svg>'''

# -----------------------------------------------------------------------------
# 5. The Stencil Ingot Medallion (Negative-Space Carve)
# -----------------------------------------------------------------------------
def concept_5_stencil_ingot(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph 5 - The Stencil Ingot Medallion"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c5-title">
  <title id="c5-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Solid Cyan Medallion Disc -->
  <circle cx="128" cy="128" r="88" fill="{cyan}"/>
  <!-- Negative Space Vertical Carve -->
  <rect x="76" y="56" width="28" height="144" rx="4" fill="{bg}"/>
  <!-- Negative Space Upper Diagonal Carve -->
  <polygon points="112,132 168,76 192,76 128,140" fill="{bg}"/>
  <!-- Negative Space Lower Diagonal Carve -->
  <polygon points="128,116 192,180 168,180 112,124" fill="{bg}"/>
  <!-- Inset Golden Amber Jewel -->
  <polygon points="116,114 130,128 116,142 102,128" fill="{amber}"/>
</svg>'''

# -----------------------------------------------------------------------------
# 6. The Proofreader's Check (Grammarly / Nike)
# Fluid circular arc swooping into an exact 45-deg checkmark blade
# -----------------------------------------------------------------------------
def concept_6_editorial_check(dark=True):
    bg = "#080b10" if dark else "#ffffff"
    border = "" if dark else ' stroke="#e2e8f0" stroke-width="4"'
    cyan = "#00f0ff" if dark else "#0284c7"
    amber = "#f59e0b"
    title = "Klyph 6 - The Proofreader's Check"
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="c6-title">
  <title id="c6-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Continuous Proofreader's Sweep into 45-deg Chisel Check -->
  <path d="M 128 52 A 76 76 0 1 0 204 128 H 156 A 28 28 0 1 1 128 100 L 184 44 Z" fill="{cyan}"/>
  <!-- Radiant Golden Focus Point -->
  <polygon points="128,100 136,108 128,116 120,108" fill="{amber}"/>
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


CONCEPTS = [
    ("c1-humanist-loop", concept_1_humanist_loop),
    ("c2-cadence-pulse", concept_2_cadence_pulse),
    ("c3-quill-wing", concept_3_quill_wing),
    ("c4-crystalline-prism", concept_4_crystalline_prism),
    ("c5-stencil-ingot", concept_5_stencil_ingot),
    ("c6-editorial-check", concept_6_editorial_check),
]

for name, fn in CONCEPTS:
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

print("Elite Six refined concepts written to", DIR)
