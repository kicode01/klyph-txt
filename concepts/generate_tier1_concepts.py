"""
Generate 4 Tier-1 Enterprise Flagship Concepts for Klyph following logo-design-skill.
Modeled after elite design firm work (Pentagram, Chermayeff & Geismar & Haviv, Landor, Collins).
Ultra-confident, extreme reduction, mathematical precision, zero amateur clutter.
"""

import os

TIER1_CONCEPTS = {}

# ---------------------------------------------------------------------------
# CONCEPT 1: The Monolith Chisel (Architectural Monogram)
# Pentagram style: Monumental vertical foundation pillar with dual 45-deg chisel blades
# and an interlocking amber diamond keystone.
# ---------------------------------------------------------------------------
TIER1_CONCEPTS["tier1-1-chisel"] = {
    "name": "The Monolith Chisel",
    "type": "Architectural Monogram (Pentagram style)",
    "idea": "A monumental vertical foundation pillar with dual 45-deg chisel blades and an interlocking amber keystone.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t1-title">
  <title id="t1-title">Klyph Tier 1 - The Monolith Chisel</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Foundation pillar -->
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#00f0ff"/>
  <!-- Upper 45-deg chisel blade -->
  <path d="M96 136 L176 56 H216 L124 148 Z" fill="#00f0ff"/>
  <!-- Lower 45-deg foundation leg -->
  <path d="M124 108 L216 200 H176 L96 120 Z" fill="#00f0ff"/>
  <!-- Interlocking amber keystone diamond -->
  <polygon points="116,102 142,128 116,154 90,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t1-title">
  <title id="t1-title">Klyph Tier 1 - The Monolith Chisel Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#0284c7"/>
  <path d="M96 136 L176 56 H216 L124 148 Z" fill="#0284c7"/>
  <path d="M124 108 L216 200 H176 L96 120 Z" fill="#0284c7"/>
  <polygon points="116,102 142,128 116,154 90,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 2: The Cadence Ribbons (Paul Rand / IBM / Medium style)
# Three parallel rhythmic editorial bars of staggered proportions forming an optical K.
# Represents human burstiness, sentence variance, and editorial cadence.
# ---------------------------------------------------------------------------
TIER1_CONCEPTS["tier1-2-cadence"] = {
    "name": "The Editorial Cadence",
    "type": "Rhythmic Kinetic Monogram (Paul Rand / IBM style)",
    "idea": "Three staggered architectural bars expressing linguistic cadence and human burstiness.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t2-title">
  <title id="t2-title">Klyph Tier 1 - The Editorial Cadence</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Left anchor stem -->
  <rect x="52" y="44" width="32" height="168" rx="6" fill="#00f0ff"/>
  <!-- Upper cadence chevron: angled bracket moving upward -->
  <path d="M104 128 L180 52 H216 L140 128 Z" fill="#00f0ff"/>
  <!-- Lower cadence chevron: angled bracket grounding downward -->
  <path d="M140 128 L216 204 H180 L104 128 Z" fill="#00f0ff"/>
  <!-- Floating amber rhythm pip -->
  <rect x="92" y="114" width="28" height="28" rx="6" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t2-title">
  <title id="t2-title">Klyph Tier 1 - The Editorial Cadence Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="32" height="168" rx="6" fill="#0284c7"/>
  <path d="M104 128 L180 52 H216 L140 128 Z" fill="#0284c7"/>
  <path d="M140 128 L216 204 H180 L104 128 Z" fill="#0284c7"/>
  <rect x="92" y="114" width="28" height="28" rx="6" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 3: The Interlocking Mobius Prism (OpenAI / Autodesk style)
# Continuous 3D dimensional ribbon folding through space to form an impossible K.
# ---------------------------------------------------------------------------
TIER1_CONCEPTS["tier1-3-mobius"] = {
    "name": "The Interlocking Prism",
    "type": "Isometric Dimensional Mark (OpenAI / Autodesk style)",
    "idea": "An isometric dimensional ribbon folding through space to form an infinite neurosymbolic K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t3-title">
  <title id="t3-title">Klyph Tier 1 - The Interlocking Prism</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Pillar stem -->
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#00f0ff"/>
  <!-- Upper isometric blade -->
  <polygon points="104,124 176,52 216,52 144,124" fill="#00f0ff"/>
  <!-- Lower isometric facet -->
  <polygon points="144,132 216,204 176,204 104,132" fill="#0284c7"/>
  <!-- Central amber keystone apex -->
  <polygon points="112,104 140,128 112,152 84,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t3-title">
  <title id="t3-title">Klyph Tier 1 - The Interlocking Prism Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#0284c7"/>
  <polygon points="104,124 176,52 216,52 144,124" fill="#0284c7"/>
  <polygon points="144,132 216,204 176,204 104,132" fill="#0369a1"/>
  <polygon points="112,104 140,128 112,152 84,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 4: The Glyphic Octagon / Institutional Seal (Chase / Palantir style)
# Chermayeff & Geismar style: A monumental octagonal seal with four chiseled cuts
# carving an unshakeable institutional K.
# ---------------------------------------------------------------------------
TIER1_CONCEPTS["tier1-4-seal"] = {
    "name": "The Glyphic Octagon",
    "type": "Institutional Octagonal Seal (Chermayeff & Geismar style)",
    "idea": "A monumental octagonal stone medallion with precision laser incisions carving an authoritative K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t4-title">
  <title id="t4-title">Klyph Tier 1 - The Glyphic Octagon</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Outer regular octagon medallion -->
  <polygon points="90,40 166,40 216,90 216,166 166,216 90,216 40,166 40,90" fill="#00f0ff"/>
  <!-- Negative-space vertical channel -->
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#080b10"/>
  <!-- Negative-space upper diagonal channel -->
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#080b10"/>
  <!-- Negative-space lower diagonal channel -->
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#080b10"/>
  <!-- Central amber keystone jewel -->
  <polygon points="116,114 130,128 116,142 102,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="t4-title">
  <title id="t4-title">Klyph Tier 1 - The Glyphic Octagon Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <polygon points="90,40 166,40 216,90 216,166 166,216 90,216 40,166 40,90" fill="#0284c7"/>
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#fbfaf6"/>
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#fbfaf6"/>
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#fbfaf6"/>
  <polygon points="116,114 130,128 116,142 102,128" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts/tier1", exist_ok=True)
    for cid, data in TIER1_CONCEPTS.items():
        dark_path = f"concepts/tier1/{cid}-dark.svg"
        light_path = f"concepts/tier1/{cid}-light.svg"
        symbol_path = f"concepts/tier1/{cid}.svg"

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(data["light"].strip() + "\n")
        with open(symbol_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")

        # Also generate responsive SVG
        resp_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="{cid}-title">
  <title id="{cid}-title">Klyph {data['name']}</title>
  <style>
    :root {{
      --klyph-base: #080b10;
      --klyph-glyph: #00f0ff;
      --klyph-keystone: #f59e0b;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --klyph-base: #fbfaf6;
        --klyph-glyph: #0284c7;
        --klyph-keystone: #d97706;
      }}
    }}
    .klyph-base {{ fill: var(--klyph-base); }}
    .klyph-glyph {{ fill: var(--klyph-glyph); }}
    .klyph-keystone {{ fill: var(--klyph-keystone); }}
  </style>
"""
        inner = data["dark"].split('</title>', 1)[1].rsplit('</svg>', 1)[0]
        inner = inner.replace('fill="#080b10"', 'class="klyph-base"')
        inner = inner.replace('fill="#00f0ff"', 'class="klyph-glyph"')
        inner = inner.replace('fill="#f59e0b"', 'class="klyph-keystone"')
        resp_svg += inner.strip() + "\n</svg>\n"

        with open(f"concepts/tier1/{cid}-responsive.svg", "w", encoding="utf-8") as f:
            f.write(resp_svg)

        print(f"Generated Tier 1 SVGs for {cid}")

if __name__ == "__main__":
    main()
