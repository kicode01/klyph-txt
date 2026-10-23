"""
Test perfect flush smooth geometry for Option 1.
"""
import os

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1")

BG_BLUE = "#0284c7"
BG_DARK = "#080b10"
WHITE = "#ffffff"
CYAN = "#00f0ff"
YELLOW = "#f59e0b"

def perfect_smooth(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # 1. Vertical Stem:
    # x=54 to 96, y=44 to 216, rounded top (r=12) and rounded bottom (r=12)
    # 2. Upper Arm:
    # From (96, 114) to (162, 48) - 45-deg
    # Rounded top-left corner: at (162, 48) curving to (172, 44)
    # Horizontal top edge: to (196, 44)
    # Rounded top-right corner: curving to (208, 54)
    # Outer 45-deg blade: down to (136, 128)
    # 3. Lower Arm:
    # From (136, 128) down 45-deg to (208, 202)
    # Rounded bottom-right corner: curving to (196, 216)
    # Horizontal bottom edge: to (172, 216)
    # Rounded bottom-left corner: curving to (162, 212)
    # Return 45-deg line to (96, 142)
    # 4. Yellow Wedge:
    # Left edge: x=96, y=98 to 158
    # Top diagonal: 45-deg line from (96, 98) to (122, 124)
    # Rounded apex: curve from (122, 124) via (127, 128) to (122, 132)
    # Bottom diagonal: 45-deg line back to (96, 158)
    # Top-left and bottom-left corners gently rounded (r=4)
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Foundation Stem (Smooth Rounded Terminals) -->
  <rect x="54" y="44" width="42" height="172" rx="14" fill="{k_col}"/>
  <!-- Upper Soaring Blade (Smooth Rounded Terminals) -->
  <path d="M 96 114 L 160 50 C 166 44 174 44 182 44 H 204 C 214 44 218 50 215 57 L 138 128 Z" fill="{k_col}"/>
  <!-- Lower Grounded Blade (Smooth Rounded Terminals) -->
  <path d="M 138 128 L 215 199 C 218 206 214 216 204 216 H 182 C 174 216 166 216 160 210 L 96 142 Z" fill="{k_col}"/>
  <!-- Smooth Yellow Wedge with Rounded Apex -->
  <path d="M 96 96 L 123 123 C 126 126 126 130 123 133 L 96 160 Z" fill="{YELLOW}"/>
</svg>'''

with open(os.path.join(DIR, "perfect-smooth-light.svg"), "w", encoding="utf-8") as f:
    f.write(perfect_smooth(dark=False))
with open(os.path.join(DIR, "perfect-smooth-dark.svg"), "w", encoding="utf-8") as f:
    f.write(perfect_smooth(dark=True))

print("Perfect smooth written")
