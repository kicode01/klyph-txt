"""
Generate clean comparison board for the top 4 candidates (eliminating any deformed/pacman shapes).
1. The Grounded Monogram (Facebook/Meta Pedigree)
2. The Chromatic Cadence (TikTok Pedigree)
3. The Cadence Pulse (Spotify/Linear Pedigree)
4. The Stencil Medallion (Beats/Target Pedigree)
"""
import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "masterclass")
SHEET_SVG = os.path.join(DIR, "comparison-board.svg")
SHEET_PNG = os.path.join(DIR, "comparison-board.png")

def load(filename):
    with open(os.path.join(DIR, filename), "r", encoding="utf-8") as f:
        content = f.read()
    inner = content.split('<svg')[1].split('>', 1)[1].rsplit('</svg>', 1)[0]
    return inner.strip()

def load_c2():
    with open(os.path.join(os.path.dirname(__file__), "elite_six", "c2-cadence-pulse-dark.svg"), "r", encoding="utf-8") as f:
        content = f.read()
    inner = content.split('<svg')[1].split('>', 1)[1].rsplit('</svg>', 1)[0]
    return inner.strip()

ma = load("master-a-grounded-dark.svg")
mb = load("master-b-tiktok-dark.svg")
c2 = load_c2()
md = load("master-d-stencil-dark.svg")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900" style="background:#080b11; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06090e"/>
      <stop offset="100%" stop-color="#0b1018"/>
    </linearGradient>
  </defs>

  <rect width="1440" height="900" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g transform="translate(64, 44)">
    <text x="0" y="32" fill="#ffffff" font-size="28" font-weight="700" letter-spacing="-0.02em">Klyph — Pure Consumer App Icon Suite</text>
    <text x="0" y="58" fill="#94a3b8" font-size="15">Four pristine, iconic directions: zero deformed shapes, 100% brand clarity, built for mobile home screens and dynamic favicons.</text>
  </g>

  <!-- 4 Cards Layout -->
  <!-- Card 1: Grounded Monogram (Meta) -->
  <g transform="translate(64, 110)">
    <rect width="300" height="740" rx="20" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(50, 40)">
      <svg viewBox="0 0 256 256" width="200" height="200">{ma}</svg>
    </g>
    <text x="24" y="280" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">META / FACEBOOK PEDIGREE</text>
    <text x="24" y="310" fill="#ffffff" font-size="20" font-weight="700">A · Grounded Monogram</text>
    <text x="24" y="334" fill="#94a3b8" font-size="13">Solid Unified Silhouette</text>
    <text x="24" y="370" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="24" dy="0">Single fused silhouette grounded</tspan>
      <tspan x="24" dy="18">to the bottom boundary.</tspan>
      <tspan x="24" dy="18">Zero floating pieces. Pure weight</tspan>
      <tspan x="24" dy="18">and enterprise permanence.</tspan>
    </text>
    
    <!-- Scale Ladder -->
    <g transform="translate(24, 480)">
      <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
      <g transform="translate(0, 16)">
        <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{ma}</svg>
        <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
      </g>
      <g transform="translate(72, 28)">
        <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{ma}</svg>
        <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
      </g>
      <g transform="translate(120, 36)">
        <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{ma}</svg>
        <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
      </g>
    </g>
  </g>

  <!-- Card 2: Chromatic Cadence (TikTok) -->
  <g transform="translate(396, 110)">
    <rect width="300" height="740" rx="20" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(50, 40)">
      <svg viewBox="0 0 256 256" width="200" height="200">{mb}</svg>
    </g>
    <text x="24" y="280" fill="#ff0055" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">TIKTOK PEDIGREE</text>
    <text x="24" y="310" fill="#ffffff" font-size="20" font-weight="700">B · Chromatic Cadence</text>
    <text x="24" y="334" fill="#94a3b8" font-size="13">High-Voltage Vibration</text>
    <text x="24" y="370" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="24" dy="0">Kinetic 12° forward italic</tspan>
      <tspan x="24" dy="18">silhouette with electric cyan</tspan>
      <tspan x="24" dy="18">and neon fuchsia chromatic offset</tspan>
      <tspan x="24" dy="18">overlapping on velvet black.</tspan>
    </text>

    <!-- Scale Ladder -->
    <g transform="translate(24, 480)">
      <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
      <g transform="translate(0, 16)">
        <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{mb}</svg>
        <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
      </g>
      <g transform="translate(72, 28)">
        <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{mb}</svg>
        <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
      </g>
      <g transform="translate(120, 36)">
        <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{mb}</svg>
        <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
      </g>
    </g>
  </g>

  <!-- Card 3: Cadence Pulse (Spotify) -->
  <g transform="translate(728, 110)">
    <rect width="300" height="740" rx="20" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(50, 40)">
      <svg viewBox="0 0 256 256" width="200" height="200">{c2}</svg>
    </g>
    <text x="24" y="280" fill="#00f0ff" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">SPOTIFY / LINEAR PEDIGREE</text>
    <text x="24" y="310" fill="#ffffff" font-size="20" font-weight="700">C · The Cadence Pulse</text>
    <text x="24" y="334" fill="#94a3b8" font-size="13">Rhythm &amp; Kinetic Waves</text>
    <text x="24" y="370" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="24" dy="0">Foundation pillar paired with</tspan>
      <tspan x="24" dy="18">dual forward-accelerating</tspan>
      <tspan x="24" dy="18">kinetic chevron waves in cyan</tspan>
      <tspan x="24" dy="18">and lapis with golden nucleus.</tspan>
    </text>

    <!-- Scale Ladder -->
    <g transform="translate(24, 480)">
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
    </g>
  </g>

  <!-- Card 4: Stencil Medallion (Beats) -->
  <g transform="translate(1060, 110)">
    <rect width="300" height="740" rx="20" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
    <g transform="translate(50, 40)">
      <svg viewBox="0 0 256 256" width="200" height="200">{md}</svg>
    </g>
    <text x="24" y="280" fill="#38bdf8" font-size="11" font-weight="700" letter-spacing="0.08em" text-transform="uppercase">BEATS / TARGET PEDIGREE</text>
    <text x="24" y="310" fill="#ffffff" font-size="20" font-weight="700">D · Stencil Medallion</text>
    <text x="24" y="334" fill="#94a3b8" font-size="13">Negative-Space Carve</text>
    <text x="24" y="370" fill="#cbd5e1" font-size="12" line-height="1.5">
      <tspan x="24" dy="0">Solid cyan circular stone disc</tspan>
      <tspan x="24" dy="18">with precision laser negative</tspan>
      <tspan x="24" dy="18">space stencil cuts. Unshakeable</tspan>
      <tspan x="24" dy="18">contrast at 16px favicon scale.</tspan>
    </text>

    <!-- Scale Ladder -->
    <g transform="translate(24, 480)">
      <text x="0" y="0" fill="#64748b" font-size="10" font-weight="600" letter-spacing="0.05em">SCALE LADDER</text>
      <g transform="translate(0, 16)">
        <svg viewBox="0 0 256 256" width="48" height="48"><rect width="256" height="256" rx="64" fill="#080b10"/>{md}</svg>
        <text x="24" y="62" fill="#64748b" font-size="10" text-anchor="middle">48px</text>
      </g>
      <g transform="translate(72, 28)">
        <svg viewBox="0 0 256 256" width="24" height="24"><rect width="256" height="256" rx="64" fill="#080b10"/>{md}</svg>
        <text x="12" y="38" fill="#64748b" font-size="10" text-anchor="middle">24px</text>
      </g>
      <g transform="translate(120, 36)">
        <svg viewBox="0 0 256 256" width="16" height="16"><rect width="256" height="256" rx="64" fill="#080b10"/>{md}</svg>
        <text x="8" y="26" fill="#64748b" font-size="10" text-anchor="middle">16px</text>
      </g>
    </g>
  </g>
</svg>'''

with open(SHEET_SVG, "w", encoding="utf-8") as f:
    f.write(svg)

print("Comparison SVG written to", SHEET_SVG)
