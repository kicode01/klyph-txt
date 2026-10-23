"""
Build transparent version of Option 1 (Full Inner Wedge with smooth, rounded corners).
Removes both black and blue background squircles.
Generates:
- Dark mode transparent (Cyan #00f0ff + Yellow #f59e0b)
- Light mode transparent A (Brand Blue #0284c7 + Yellow #f59e0b)
- Light mode transparent B (Carbon Ink #080b10 + Yellow #f59e0b)
- Responsive adaptive transparent (prefers-color-scheme)
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1", "transparent")
os.makedirs(DIR, exist_ok=True)

CYAN = "#00f0ff"
BLUE = "#0284c7"
CARBON = "#080b10"
YELLOW = "#f59e0b"

def build_svg(k_color, name, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="{name}-title">
  <title id="{name}-title">{title}</title>
  <!-- Grounded Foundation Stem (Smooth Rounded Terminals, rx=14) -->
  <rect x="54" y="44" width="42" height="172" rx="14" fill="{k_color}"/>
  <!-- Fused Diagonal Blades with Smooth Rounded Terminals -->
  <path d="M 96 114 L 162 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 162 212 L 96 146 Z" fill="{k_color}"/>
  <!-- Smooth Yellow Wedge (Seamless Fit into the Crook) -->
  <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>
</svg>'''

def build_responsive(light_color=BLUE):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="klyph-trans-resp-title">
  <title id="klyph-trans-resp-title">Klyph Transparent Icon - Grounded Monogram with Yellow Wedge</title>
  <style>
    .mode-light {{ display: none; }}
    .mode-dark  {{ display: block; }}
    @media (prefers-color-scheme: light) {{
      .mode-light {{ display: block; }}
      .mode-dark  {{ display: none; }}
    }}
  </style>
  <g class="mode-dark">
    <!-- Dark Mode: Electric Cyan + Yellow Wedge -->
    <rect x="54" y="44" width="42" height="172" rx="14" fill="{CYAN}"/>
    <path d="M 96 114 L 162 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 162 212 L 96 146 Z" fill="{CYAN}"/>
    <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>
  </g>
  <g class="mode-light">
    <!-- Light Mode: Brand Blue / Carbon + Yellow Wedge -->
    <rect x="54" y="44" width="42" height="172" rx="14" fill="{light_color}"/>
    <path d="M 96 114 L 162 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 162 212 L 96 146 Z" fill="{light_color}"/>
    <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>
  </g>
</svg>'''

# Write files
with open(os.path.join(DIR, "klyph-trans-dark.svg"), "w", encoding="utf-8") as f:
    f.write(build_svg(CYAN, "klyph-trans-dark", "Klyph Transparent Icon (Dark Theme: Cyan and Yellow)"))

with open(os.path.join(DIR, "klyph-trans-light-blue.svg"), "w", encoding="utf-8") as f:
    f.write(build_svg(BLUE, "klyph-trans-light-blue", "Klyph Transparent Icon (Light Theme: Brand Blue and Yellow)"))

with open(os.path.join(DIR, "klyph-trans-light-carbon.svg"), "w", encoding="utf-8") as f:
    f.write(build_svg(CARBON, "klyph-trans-light-carbon", "Klyph Transparent Icon (Light Theme: Carbon Ink and Yellow)"))

with open(os.path.join(DIR, "klyph-trans-responsive.svg"), "w", encoding="utf-8") as f:
    f.write(build_responsive(BLUE))

print("Transparent SVGs built successfully in", DIR)
