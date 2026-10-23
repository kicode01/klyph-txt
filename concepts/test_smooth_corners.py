"""
Test and refine Option 1 with smooth, rounded corners (not sharp).
Generates multiple variations with different degrees of smooth curvature:
- S1: Subtle Modern Fillet (r=6px to 8px - crisp, modern, Apple-style)
- S2: Generous Soft Fillet (r=10px to 14px - friendly, smooth, Meta-style)
- S3: Ultra-Smooth Humanist (All terminals and inner joints fully rounded)
"""
import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1")
os.makedirs(DIR, exist_ok=True)

BG_BLUE = "#0284c7"
BG_DARK = "#080b10"
WHITE = "#ffffff"
CYAN = "#00f0ff"
YELLOW = "#f59e0b"

# -----------------------------------------------------------------------------
# S1: Subtle Modern Fillet (r=8px on stem and outer terminals, r=6px on wedge)
# -----------------------------------------------------------------------------
def smooth_s1(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # Stem: x=54 to 96, y=44 to 216, rounded top corners r=10, grounded bottom
    # Upper arm: 45-deg blade with r=8 on outer terminals
    # Lower arm: 45-deg blade with r=8 on outer terminals
    # Wedge: rounded triangle with r=6 apex
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Grounded Vertical Stem with Rounded Top -->
  <rect x="54" y="44" width="42" height="172" rx="10" fill="{k_col}"/>
  <!-- Upper 45-deg Arm with Rounded Outer Terminal -->
  <path d="M 96 114 L 164 46 C 168 44 172 44 176 44 H 210 C 216 44 220 48 218 54 L 136 132 Z" fill="{k_col}"/>
  <!-- Lower 45-deg Arm with Rounded Outer Terminal -->
  <path d="M 136 124 L 218 206 C 220 212 216 216 210 216 H 176 C 172 216 168 216 164 214 L 96 142 Z" fill="{k_col}"/>
  <!-- Yellow Inner Wedge with Smooth Rounded Corners -->
  <path d="M 96 96 L 126 126 C 128 128 128 130 126 132 L 96 162 Z" fill="{YELLOW}" stroke="{YELLOW}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
</svg>'''

# -----------------------------------------------------------------------------
# S2: Generous Soft Fillet (Meta / Airbnb Pedigree - Smooth r=12px curves)
# -----------------------------------------------------------------------------
def smooth_s2(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # Entire K drawn as a unified path with generous 12px rounded outer corners
    # and a smooth rounded yellow wedge
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Stem -->
  <path d="M 54 56 C 54 48 60 44 68 44 H 82 C 90 44 96 48 96 56 V 204 C 96 212 90 216 82 216 H 68 C 60 216 54 212 54 204 Z" fill="{k_col}"/>
  <!-- Upper Blade (Smooth Rounded Corners) -->
  <path d="M 96 114 L 160 50 C 166 44 174 44 182 44 H 206 C 214 44 218 50 216 58 L 136 132 Z" fill="{k_col}"/>
  <!-- Lower Blade (Smooth Rounded Corners) -->
  <path d="M 136 124 L 216 198 C 218 206 214 216 206 216 H 182 C 174 216 166 216 160 210 L 96 142 Z" fill="{k_col}"/>
  <!-- Yellow Smooth Wedge (Filleted apex and edges) -->
  <path d="M 96 98 L 124 126 C 126 128 126 130 124 132 L 96 160 Z" fill="{YELLOW}" stroke="{YELLOW}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>
</svg>'''

# -----------------------------------------------------------------------------
# S3: Unified Fillet Monogram (Single path with continuous smooth fillets)
# -----------------------------------------------------------------------------
def smooth_s3(dark=False):
    bg = BG_DARK if dark else BG_BLUE
    k_col = CYAN if dark else WHITE
    border = "" if dark else ' stroke="#0369a1" stroke-width="4"'
    
    # A single continuous path where the vertical stem and diagonal arms flow together,
    # and the yellow wedge has a smooth rounded tip
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <rect width="256" height="256" rx="64" fill="{bg}"{border}/>
  <!-- Unified Smooth K Path -->
  <path d="M 54 58 C 54 50 60 44 68 44 H 82 C 90 44 96 50 96 58 V 104 L 160 48 C 166 44 174 44 182 44 H 204 C 214 44 218 50 214 58 L 138 128 L 214 198 C 218 206 214 216 204 216 H 182 C 174 216 166 216 160 212 L 96 152 V 202 C 96 210 90 216 82 216 H 68 C 60 216 54 210 54 202 Z" fill="{k_col}"/>
  <!-- Yellow Smooth Inner Wedge (Rounded Apex) -->
  <path d="M 96 100 L 122 126 C 124 128 124 130 122 132 L 96 158 Z" fill="{YELLOW}" stroke="{YELLOW}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>
</svg>'''

SMOOTH = [
    ("s1-subtle", smooth_s1),
    ("s2-soft", smooth_s2),
    ("s3-unified", smooth_s3),
]

for name, fn in SMOOTH:
    with open(os.path.join(DIR, f"{name}-light.svg"), "w", encoding="utf-8") as f:
        f.write(fn(dark=False))
    with open(os.path.join(DIR, f"{name}-dark.svg"), "w", encoding="utf-8") as f:
        f.write(fn(dark=True))

print("Smooth variations written to", DIR)
