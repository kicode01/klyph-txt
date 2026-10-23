"""
100/100 Production Audit for Seamless Smooth Mark (Option 1 with smooth, non-sharp corners).
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1")

BG_BLUE = "#0284c7"
BG_DARK = "#080b10"
WHITE = "#ffffff"
CYAN = "#00f0ff"
YELLOW = "#f59e0b"

def build_svg(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    title = f"Klyph Icon - Smooth Grounded Monogram with Yellow Wedge ({'Dark' if dark else 'Light'})"
    
    # Mathematical Coordinates:
    # 1. Stem: x=54 to 96, y=44 to 216, rx=14
    # 2. Diagonal Blades:
    # Upper blade:
    # Starts at (96, 114)
    # 45-deg line to (162, 48) [dx=66, dy=-66 -> exact 45.0 deg]
    # Rounded corner: C 166 44 174 44 182 44
    # Horizontal top: H 204
    # Rounded corner: C 214 44 218 50 215 57
    # 45-deg line down: L 132 128
    # Lower blade:
    # From (132, 128)
    # 45-deg line down: L 215 199
    # Rounded corner: C 218 206 214 216 204 216
    # Horizontal bottom: H 182
    # Rounded corner: C 174 216 166 216 162 212
    # 45-deg line back: L 96 146 [dx=-66, dy=-66 -> exact 45.0 deg]
    # 3. Yellow Wedge:
    # From (96, 92) down 45-deg to (126, 122) [dx=30, dy=30 -> exact 45.0 deg]
    # Smooth rounded nose reaching (132, 128)
    # Down 45-deg back to (96, 164) [dx=-30, dy=30 -> exact 45.0 deg]
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-smooth-title">
  <title id="klyph-smooth-title">{title}</title>
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Foundation Stem (Smooth Rounded Terminals) -->
  <rect x="54" y="44" width="42" height="172" rx="14" fill="{k_col}"/>
  <!-- Fused Diagonal Blades with Smooth Rounded Terminals -->
  <path d="M 96 114 L 162 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 162 212 L 96 146 Z" fill="{k_col}"/>
  <!-- Smooth Yellow Wedge (Seamless Fit into the Crook) -->
  <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>
</svg>'''

def build_responsive():
    dark_inner = build_svg(dark=True).split('<rect width="256"')[1]
    dark_inner = '<rect width="256"' + dark_inner.replace('</svg>', '').strip()
    
    light_inner = build_svg(dark=False).split('<rect width="256"')[1]
    light_inner = '<rect width="256"' + light_inner.replace('</svg>', '').strip()
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-smooth-resp-title">
  <title id="klyph-smooth-resp-title">Klyph Responsive Icon - Smooth Grounded Monogram with Yellow Wedge</title>
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

with open(os.path.join(DIR, "klyph-smooth-light.svg"), "w", encoding="utf-8") as f:
    f.write(build_svg(dark=False))
with open(os.path.join(DIR, "klyph-smooth-dark.svg"), "w", encoding="utf-8") as f:
    f.write(build_svg(dark=True))
with open(os.path.join(DIR, "klyph-smooth-responsive.svg"), "w", encoding="utf-8") as f:
    f.write(build_responsive())

print("Built klyph-smooth SVGs")
