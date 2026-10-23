"""
Generate side-by-side comparison sheet for 'make the yellow fill:' options.
"""
import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "yellow_fills")
SHEET_SVG = os.path.join(DIR, "yellow-fill-options.svg")
SHEET_PNG = os.path.join(DIR, "yellow-fill-options.png")

def load(filename):
    with open(os.path.join(DIR, filename), "r", encoding="utf-8") as f:
        content = f.read()
    inner = content.split('<svg')[1].split('>', 1)[1].rsplit('</svg>', 1)[0]
    return inner.strip()

v1 = load("v1-wedge-light.svg")
v4 = load("v4-flush-diamond-light.svg")
v2 = load("v2-full-k-light.svg")
v3 = load("v3-dual-tone-light.svg")
v5 = load("v5-arrowhead-light.svg")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 640" width="1600" height="640" style="background:#080b11; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06090e"/>
      <stop offset="100%" stop-color="#0b1018"/>
    </linearGradient>
  </defs>

  <rect width="1600" height="640" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g transform="translate(64, 40)">
    <text x="0" y="32" fill="#ffffff" font-size="28" font-weight="700" letter-spacing="-0.02em">Klyph — Yellow Fill Variations</text>
    <text x="0" y="58" fill="#94a3b8" font-size="15">Select how you want the yellow/amber element to fill within the grounded monogram:</text>
  </g>

  <!-- 5 Cards Layout -->
  <!-- Option 1: Full Inner Wedge -->
  <g transform="translate(64, 110)">
    <rect width="280" height="490" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(40, 28)">
      <svg viewBox="0 0 256 256" width="200" height="200">{v1}</svg>
    </g>
    <text x="20" y="260" fill="#f59e0b" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPTION 1 · TOP PICK</text>
    <text x="20" y="286" fill="#ffffff" font-size="18" font-weight="700">Full Inner Wedge</text>
    <text x="20" y="310" fill="#94a3b8" font-size="12">Fills the entire triangular notch</text>
    <text x="20" y="338" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="20" dy="0">Yellow completely fills the</tspan>
      <tspan x="20" dy="18">triangular crook between the</tspan>
      <tspan x="20" dy="18">vertical pillar and diagonal arms.</tspan>
      <tspan x="20" dy="18">Seamless, zero awkward gaps.</tspan>
    </text>
  </g>

  <!-- Option 2: Flush Joint Diamond -->
  <g transform="translate(368, 110)">
    <rect width="280" height="490" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(40, 28)">
      <svg viewBox="0 0 256 256" width="200" height="200">{v4}</svg>
    </g>
    <text x="20" y="260" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPTION 2</text>
    <text x="20" y="286" fill="#ffffff" font-size="18" font-weight="700">Flush Joint Diamond</text>
    <text x="20" y="310" fill="#94a3b8" font-size="12">Diamond expanded to stroke edges</text>
    <text x="20" y="338" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="20" dy="0">Yellow diamond scaled so its</tspan>
      <tspan x="20" dy="18">corners connect flush with</tspan>
      <tspan x="20" dy="18">the outer edges of the blades,</tspan>
      <tspan x="20" dy="18">forming a bold central jewel.</tspan>
    </text>
  </g>

  <!-- Option 3: Full Letter K -->
  <g transform="translate(672, 110)">
    <rect width="280" height="490" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(40, 28)">
      <svg viewBox="0 0 256 256" width="200" height="200">{v2}</svg>
    </g>
    <text x="20" y="260" fill="#f59e0b" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPTION 3</text>
    <text x="20" y="286" fill="#ffffff" font-size="18" font-weight="700">Full Letter K Yellow</text>
    <text x="20" y="310" fill="#94a3b8" font-size="12">The entire K is golden yellow</text>
    <text x="20" y="338" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="20" dy="0">The entire letterform is filled</tspan>
      <tspan x="20" dy="18">with radiant golden yellow,</tspan>
      <tspan x="20" dy="18">with a white keystone diamond</tspan>
      <tspan x="20" dy="18">centered at the junction.</tspan>
    </text>
  </g>

  <!-- Option 4: Dual-Tone Wings -->
  <g transform="translate(976, 110)">
    <rect width="280" height="490" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(40, 28)">
      <svg viewBox="0 0 256 256" width="200" height="200">{v3}</svg>
    </g>
    <text x="20" y="260" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPTION 4</text>
    <text x="20" y="286" fill="#ffffff" font-size="18" font-weight="700">Dual-Tone Wings</text>
    <text x="20" y="310" fill="#94a3b8" font-size="12">White pillar, yellow diagonals</text>
    <text x="20" y="338" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="20" dy="0">Vertical pillar is solid white,</tspan>
      <tspan x="20" dy="18">while the two dynamic 45°</tspan>
      <tspan x="20" dy="18">diagonal blades are yellow,</tspan>
      <tspan x="20" dy="18">creating high-contrast lift.</tspan>
    </text>
  </g>

  <!-- Option 5: Forward Arrowhead -->
  <g transform="translate(1280, 110)">
    <rect width="280" height="490" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(40, 28)">
      <svg viewBox="0 0 256 256" width="200" height="200">{v5}</svg>
    </g>
    <text x="20" y="260" fill="#f59e0b" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPTION 5</text>
    <text x="20" y="286" fill="#ffffff" font-size="18" font-weight="700">Forward Arrowhead</text>
    <text x="20" y="310" fill="#94a3b8" font-size="12">Fills the counter-space triangle</text>
    <text x="20" y="338" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="20" dy="0">Yellow fills the negative space</tspan>
      <tspan x="20" dy="18">between the upper and lower</tspan>
      <tspan x="20" dy="18">diagonal blades, forming an</tspan>
      <tspan x="20" dy="18">accelerating forward arrow.</tspan>
    </text>
  </g>
</svg>'''

with open(SHEET_SVG, "w", encoding="utf-8") as f:
    f.write(svg)

print("Overview SVG written to", SHEET_SVG)
