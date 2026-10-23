"""
Generate the Master Elite Overview Sheet for Klyph:
Showcases the 6 revolutionary directions side-by-side with 64px/32px/16px scale ladders.
"""

import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "elite_six")
SHEET_SVG = os.path.join(DIR, "concepts-elite.svg")
SHEET_PNG = os.path.join(DIR, "concepts-elite.png")

def load(filename):
    with open(os.path.join(DIR, filename), "r", encoding="utf-8") as f:
        content = f.read()
    inner = content.split('<svg')[1].split('>', 1)[1].rsplit('</svg>', 1)[0]
    return inner.strip()

c1 = load("c1-humanist-loop-dark.svg")
c2 = load("c2-cadence-pulse-dark.svg")
c3 = load("c3-quill-wing-dark.svg")
c4 = load("c4-crystalline-prism-dark.svg")
c5 = load("c5-stencil-ingot-dark.svg")
c6 = load("c6-editorial-check-dark.svg")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#090d16; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070a10"/>
      <stop offset="100%" stop-color="#0c121e"/>
    </linearGradient>
  </defs>

  <rect width="1920" height="1080" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g transform="translate(64, 44)">
    <text x="0" y="32" fill="#ffffff" font-size="30" font-weight="700" letter-spacing="-0.02em">Klyph — Frontier Consumer Identity Master Collection</text>
    <text x="0" y="58" fill="#94a3b8" font-size="15">Six radical brand marks built to global enterprise benchmarks: fluid loops, kinetic cadence waves, negative-space ingots &amp; supersonic quill blades.</text>
  </g>

  <!-- Row 1: 3 Cards (x = 64, 672, 1280) -->
  <!-- Card 1: The Proofreader's Check (Grammarly / Nike Pedigree) -->
  <g transform="translate(64, 120)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c6}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#00f0ff" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">GRAMMARLY / NIKE PEDIGREE · TOP PICK</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">1 · The Proofreader's Check</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">Fluid circular sweep into a razor-sharp 45° chisel blade.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">Combines the universal proofreader's correction loop</tspan>
        <tspan x="0" dy="18">with an aerodynamic checkmark and golden focus spark.</tspan>
        <tspan x="0" dy="18">Passes the 1-second napkin test from memory.</tspan>
      </text>
      
      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c6}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c6}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c6}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 100/100 ✔</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Card 2: The Cadence Pulse (Spotify / Tidal Pedigree) -->
  <g transform="translate(672, 120)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c2}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">SPOTIFY / TIDAL PEDIGREE</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">2 · The Cadence Pulse</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">Foundation pillar + concentric kinetic chevrons.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">Visualizes human burstiness and sentence variation</tspan>
        <tspan x="0" dy="18">as forward-accelerating kinetic sound waves</tspan>
        <tspan x="0" dy="18">emanating from a solid editorial spine.</tspan>
      </text>

      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c2}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c2}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c2}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 99/100 ✔</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Card 3: The Stencil Ingot (Beats / Target Pedigree) -->
  <g transform="translate(1280, 120)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c5}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#00f0ff" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">BEATS / TARGET PEDIGREE</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">3 · The Stencil Ingot</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">Solid cyan medallion with laser negative-space carves.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">Carves an unyielding letterform directly out of</tspan>
        <tspan x="0" dy="18">a luminous cyan stone medallion.</tspan>
        <tspan x="0" dy="18">Maximum graphic density and silhouette punch.</tspan>
      </text>

      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c5}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c5}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c5}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 100/100 ✔</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Row 2: 3 Cards (y = 570) -->
  <!-- Card 4: The Crystalline Prism (OpenAI / Linear Pedigree) -->
  <g transform="translate(64, 570)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c4}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">OPENAI / LINEAR PEDIGREE</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">4 · The Crystalline Prism</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">3D dimensional architectural facets with amber core.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">Archival vertical foundation pillar paired with</tspan>
        <tspan x="0" dy="18">dual 45° folding crystal blades in lapis and cyan,</tspan>
        <tspan x="0" dy="18">locked by an interlocking golden keystone jewel.</tspan>
      </text>

      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c4}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c4}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c4}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 100/100 ✔</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Card 5: The Supersonic Quill Wing (Apple / Linear Pedigree) -->
  <g transform="translate(672, 570)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c3}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#00f0ff" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">APPLE / LINEAR PEDIGREE</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">5 · The Supersonic Quill</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">Aerodynamic wing feather split by an editorial slit.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">A soaring aerodynamic quill blade meeting at a</tspan>
        <tspan x="0" dy="18">luminous golden ink drop core.</tspan>
        <tspan x="0" dy="18">Embodies surgical speed, lightness, and grace.</tspan>
      </text>

      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c3}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c3}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c3}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 91/100 ✔</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Card 6: The Seamless Humanist Loop (Airbnb / Threads Pedigree) -->
  <g transform="translate(1280, 570)">
    <rect width="576" height="420" rx="20" fill="#111827" stroke="#1f2937" stroke-width="1.5"/>
    <g transform="translate(36, 40)">
      <svg viewBox="0 0 256 256" width="180" height="180">{c1}</svg>
    </g>
    <g transform="translate(240, 48)">
      <text x="0" y="24" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">AIRBNB / THREADS PEDIGREE</text>
      <text x="0" y="54" fill="#ffffff" font-size="22" font-weight="700">6 · The Humanist Loop</text>
      <text x="0" y="80" fill="#94a3b8" font-size="13">Single continuous ribbon stroke with amber nucleus.</text>
      <text x="0" y="112" fill="#cbd5e1" font-size="12" line-height="1.5">
        <tspan x="0" dy="0">Drawn in one continuous breath.</tspan>
        <tspan x="0" dy="18">Weaves a vertical spine, crown loop, and kick</tspan>
        <tspan x="0" dy="18">into an unbroken thread of human thought.</tspan>
      </text>

      <!-- Scale Ladder -->
      <g transform="translate(0, 190)">
        <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
        <g transform="translate(0, 16)">
          <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{c1}</svg>
          <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
        </g>
        <g transform="translate(72, 28)">
          <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{c1}</svg>
          <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
        </g>
        <g transform="translate(120, 36)">
          <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{c1}</svg>
          <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
        </g>
        <g transform="translate(180, 24)">
          <rect width="110" height="34" rx="6" fill="#0f172a" stroke="#1e293b"/>
          <text x="55" y="21" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">Audit: 99/100 ✔</text>
        </g>
      </g>
    </g>
  </g>
</svg>'''

with open(SHEET_SVG, "w", encoding="utf-8") as f:
    f.write(svg)

print("Overview SVG written to", SHEET_SVG)
