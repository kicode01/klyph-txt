"""
Deploy transparent Option 1 assets to server/static/
- icon-dark.svg (Transparent Cyan #00f0ff + Yellow #f59e0b)
- icon-light.svg (Transparent Brand Blue #0284c7 + Yellow #f59e0b)
- icon.svg (Responsive Transparent SVG)
- icon-192.png & icon-512.png (Transparent raster PNGs)
"""
import os
import subprocess

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "server", "static")
STATIC_DIR = os.path.abspath(STATIC_DIR)

CYAN = "#00f0ff"
BLUE = "#0284c7"
YELLOW = "#f59e0b"

def get_glyph_paths(color):
    return f'''  <!-- Grounded Foundation Stem (Smooth Rounded Terminals, rx=14) -->
  <rect x="54" y="44" width="42" height="172" rx="14" fill="{color}"/>
  <!-- Fused Diagonal Blades with Smooth Rounded Terminals -->
  <path d="M 96 114 L 162 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 162 212 L 96 146 Z" fill="{color}"/>
  <!-- Smooth Yellow Wedge (Seamless Fit into the Crook) -->
  <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>'''

# 1. Dark Mode Vector
dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-dark-title">
  <title id="klyph-dark-title">Klyph Monogram - Dark Mode</title>
{get_glyph_paths(CYAN)}
</svg>'''

# 2. Light Mode Vector
light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-light-title">
  <title id="klyph-light-title">Klyph Monogram - Light Mode</title>
{get_glyph_paths(BLUE)}
</svg>'''

# 3. Responsive Vector
responsive_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-resp-title">
  <title id="klyph-resp-title">Klyph Monogram</title>
  <style>
    .mode-light {{ display: none; }}
    .mode-dark  {{ display: block; }}
    @media (prefers-color-scheme: light) {{
      .mode-light {{ display: block; }}
      .mode-dark  {{ display: none; }}
    }}
  </style>
  <g class="mode-dark">
{get_glyph_paths(CYAN)}
  </g>
  <g class="mode-light">
{get_glyph_paths(BLUE)}
  </g>
</svg>'''

with open(os.path.join(STATIC_DIR, "icon-dark.svg"), "w", encoding="utf-8") as f:
    f.write(dark_svg)

with open(os.path.join(STATIC_DIR, "icon-light.svg"), "w", encoding="utf-8") as f:
    f.write(light_svg)

with open(os.path.join(STATIC_DIR, "icon.svg"), "w", encoding="utf-8") as f:
    f.write(responsive_svg)

print("SVGs written to", STATIC_DIR)
