"""
Generate comprehensive visual showcase of Option 1 with transparent background
(no black squircle, no blue squircle).
Renders comparison onto a PNG and copies to artifacts.
"""
import os
import subprocess

DIR = os.path.join(os.path.dirname(__file__), "smooth_option1", "transparent")
SHOWCASE_HTML = os.path.join(DIR, "showcase.html")
SHOWCASE_PNG = os.path.join(DIR, "transparent-showcase.png")

# Read SVG contents
def read_inner(filename):
    with open(os.path.join(DIR, filename), "r", encoding="utf-8") as f:
        content = f.read()
    inner = content.split('<svg')[1].split('>', 1)[1].rsplit('</svg>', 1)[0]
    return inner.strip()

dark_svg = read_inner("klyph-trans-dark.svg")
light_blue_svg = read_inner("klyph-trans-light-blue.svg")
light_carbon_svg = read_inner("klyph-trans-light-carbon.svg")

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Klyph Transparent Mark — Option 1 (No Background)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #06090e;
      color: #f8fafc;
      padding: 48px 40px;
    }}
    .header {{
      margin-bottom: 36px;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 24px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      background: rgba(245, 158, 11, 0.15);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.3);
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 32px;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    p.subtitle {{
      color: #94a3b8;
      font-size: 15px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 40px;
    }}
    .card {{
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid #1e293b;
      display: flex;
      flex-direction: column;
    }}
    .card-preview {{
      height: 280px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}
    .card-body {{
      padding: 24px;
      background: #0f172a;
      border-top: 1px solid #1e293b;
      flex: 1;
    }}
    .card-title {{
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .card-tag {{
      font-size: 12px;
      font-weight: 600;
      color: #38bdf8;
      margin-bottom: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .card-desc {{
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.5;
    }}

    /* Specific Preview Backgrounds */
    .bg-dark-obsidian {{
      background: #080b10;
      /* subtle dot grid to highlight transparency */
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      background-size: 16px 16px;
    }}
    .bg-light-paper {{
      background: #fbfaf6;
      background-image: radial-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px);
      background-size: 16px 16px;
    }}
    .bg-pure-white {{
      background: #ffffff;
      background-image: radial-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px);
      background-size: 16px 16px;
    }}

    /* Mockups Section */
    .mockups-header {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 20px;
      color: #e2e8f0;
    }}
    .mockups-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 32px;
    }}
    .mockup-card {{
      border-radius: 14px;
      padding: 24px;
      border: 1px solid #1e293b;
    }}
    .mockup-dark {{
      background: #080b10;
      color: #f8fafc;
    }}
    .mockup-light {{
      background: #fbfaf6;
      color: #0e121a;
      border-color: #e2dbcb;
    }}
    .nav-mockup {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 18px;
      border-radius: 10px;
      margin-bottom: 20px;
    }}
    .nav-dark {{
      background: #0d1219;
      border: 1px solid #182233;
    }}
    .nav-light {{
      background: #ffffff;
      border: 1px solid #e2dbcb;
    }}
    .brand-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .scale-row {{
      display: flex;
      align-items: flex-end;
      gap: 28px;
      padding-top: 14px;
    }}
    .scale-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: #64748b;
    }}
  </style>
</head>
<body>

  <div class="header">
    <div class="badge">Pure Transparent Mark · Zero Background</div>
    <h1>Klyph Option 1 — Black & Blue Backgrounds Removed</h1>
    <p class="subtitle">Executing the smooth Option 1 monogram as a floating vector glyph with transparent canvas. Seamless yellow inner crook fill, softened filleted corners.</p>
  </div>

  <div class="grid">
    <!-- Card 1: Dark Mode Transparent -->
    <div class="card">
      <div class="card-preview bg-dark-obsidian">
        <svg viewBox="0 0 256 256" width="160" height="160">
          {dark_svg}
        </svg>
      </div>
      <div class="card-body">
        <div class="card-tag" style="color:#00f0ff;">Dark Surface (Obsidian / Basalt)</div>
        <div class="card-title">Electric Cyan + Amber Wedge</div>
        <div class="card-desc">
          Zero container squircle. Floating Cyan monogram (`#00f0ff`) with amber crook (`#f59e0b`). Pristine illumination against dark editors, IDE toolbars, and twilight mode.
        </div>
      </div>
    </div>

    <!-- Card 2: Light Mode Brand Blue -->
    <div class="card">
      <div class="card-preview bg-light-paper">
        <svg viewBox="0 0 256 256" width="160" height="160">
          {light_blue_svg}
        </svg>
      </div>
      <div class="card-body">
        <div class="card-tag" style="color:#0284c7;">Light Surface (Brand Blue)</div>
        <div class="card-title">Brand Blue + Amber Wedge</div>
        <div class="card-desc">
          Meta / Twitter pedigree. The blue has moved from the background container into the letterform itself (`#0284c7`), preserving the signature brand hue with zero background box.
        </div>
      </div>
    </div>

    <!-- Card 3: Light Mode Carbon Ink -->
    <div class="card">
      <div class="card-preview bg-pure-white">
        <svg viewBox="0 0 256 256" width="160" height="160">
          {light_carbon_svg}
        </svg>
      </div>
      <div class="card-body">
        <div class="card-tag" style="color:#94a3b8;">Light Surface (Carbon Ink)</div>
        <div class="card-title">Carbon Ink + Amber Wedge</div>
        <div class="card-desc">
          Apple / Linear pedigree. Minimalist deep obsidian letterform (`#080b10`) with glowing amber crook (`#f59e0b`). Ultra-clean on pure white and warm vellum surfaces.
        </div>
      </div>
    </div>
  </div>

  <div class="mockups-header">Real-World In-App Context & Favicon Scales</div>

  <div class="mockups-grid">
    <!-- Dark Mode App Header & Scale -->
    <div class="mockup-card mockup-dark">
      <div style="font-size: 13px; font-weight: 600; color: #94a3b8; margin-bottom: 12px; text-transform: uppercase;">Twilight Theme Navigation Bar</div>
      <div class="nav-mockup nav-dark">
        <div class="brand-group">
          <svg viewBox="0 0 256 256" width="28" height="28">{dark_svg}</svg>
          <span>Klyph Studio</span>
        </div>
        <div style="margin-left: auto; font-size: 12px; color: #64748b; display: flex; gap: 16px;">
          <span style="color: #00f0ff;">Chisel</span>
          <span>Morph</span>
          <span>Radar</span>
        </div>
      </div>

      <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">Scale Ladder (Favicon & Tab UI):</div>
      <div class="scale-row">
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="64" height="64">{dark_svg}</svg>
          <span>64px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="32" height="32">{dark_svg}</svg>
          <span>32px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="24" height="24">{dark_svg}</svg>
          <span>24px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="16" height="16">{dark_svg}</svg>
          <span>16px</span>
        </div>
      </div>
    </div>

    <!-- Light Mode App Header & Scale -->
    <div class="mockup-card mockup-light">
      <div style="font-size: 13px; font-weight: 600; color: #687487; margin-bottom: 12px; text-transform: uppercase;">Paper Theme Navigation Bar</div>
      <div class="nav-mockup nav-light">
        <div class="brand-group">
          <svg viewBox="0 0 256 256" width="28" height="28">{light_blue_svg}</svg>
          <span style="color: #0e121a;">Klyph Studio</span>
        </div>
        <div style="margin-left: auto; font-size: 12px; color: #9aa3b2; display: flex; gap: 16px;">
          <span style="color: #0284c7; font-weight: 600;">Chisel</span>
          <span>Morph</span>
          <span>Radar</span>
        </div>
      </div>

      <div style="font-size: 12px; color: #687487; margin-bottom: 8px;">Scale Ladder (Favicon & Tab UI):</div>
      <div class="scale-row">
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="64" height="64">{light_blue_svg}</svg>
          <span style="color: #9aa3b2;">64px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="32" height="32">{light_blue_svg}</svg>
          <span style="color: #9aa3b2;">32px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="24" height="24">{light_blue_svg}</svg>
          <span style="color: #9aa3b2;">24px</span>
        </div>
        <div class="scale-item">
          <svg viewBox="0 0 256 256" width="16" height="16">{light_blue_svg}</svg>
          <span style="color: #9aa3b2;">16px</span>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
'''

with open(SHOWCASE_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Showcase HTML written to", SHOWCASE_HTML)
