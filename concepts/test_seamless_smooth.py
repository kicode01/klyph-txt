"""
Refine Option 1 smooth corners with zero gaps.
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1")

BG_BLUE = "#0284c7"
BG_DARK = "#080b10"
WHITE = "#ffffff"
CYAN = "#00f0ff"
YELLOW = "#f59e0b"

def seamless_smooth(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # Pillar: x=54 to 96, y=44 to 216, rounded top (r=12) and bottom (r=12)
    # Diagonal Blades:
    # Fused single path:
    # Starts at (96, 114)
    # Upper arm to (160, 50) -> rounded top-left corner -> H 204 -> rounded top-right corner -> down to (132, 128)
    # Lower arm from (132, 128) -> down to (204, 200) -> rounded bottom-right -> H 168 -> rounded bottom-left -> up to (96, 142)
    # Yellow Wedge:
    # From (96, 92) down 45-deg to (126, 122)
    # Smooth rounded nose reaching (134, 128)
    # Down 45-deg back to (96, 164)
    # Vertical line back to (96, 92)
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Foundation Stem (Smooth Rounded Corners) -->
  <rect x="54" y="44" width="42" height="172" rx="14" fill="{k_col}"/>
  <!-- Fused Diagonal Blades with Smooth Rounded Terminals -->
  <path d="M 96 114 L 160 50 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 132 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 160 210 L 96 142 Z" fill="{k_col}"/>
  <!-- Smooth Yellow Wedge (Seamless Fit into the Crook) -->
  <path d="M 96 92 L 126 122 C 130 126 130 130 126 134 L 96 164 Z" fill="{YELLOW}"/>
</svg>'''

with open(os.path.join(DIR, "seamless-smooth-light.svg"), "w", encoding="utf-8") as f:
    f.write(seamless_smooth(dark=False))
with open(os.path.join(DIR, "seamless-smooth-dark.svg"), "w", encoding="utf-8") as f:
    f.write(seamless_smooth(dark=True))

print("Seamless smooth written")
