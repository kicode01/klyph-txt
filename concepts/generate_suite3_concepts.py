"""
Generate Suite 3: Tier-1 Enterprise Flagship Concepts for Klyph following logo-design-skill.
Four distinct enterprise archetypes:
1. S3-1: The Origami Editorial Fold (Dimensional Paper Vellum / Figma / Tesla style)
2. S3-2: The Continuous Monoline Loop (Single-Stroke Ribbon / Airbnb / Meta style)
3. S3-3: The Isometric Hexagonal Ingot (3D Crystal Cube / Databricks / Scale AI style)
4. S3-4: The AST Syntax Lattice (Computational Node Network / GraphQL / Anthropic style)
"""

import os

SUITE3_CONCEPTS = {}

# ---------------------------------------------------------------------------
# S3-1: The Origami Editorial Fold (Figma / Tesla style)
# Dimensional flat paper fold forming an architectural K with zero blur/gradients.
# ---------------------------------------------------------------------------
SUITE3_CONCEPTS["s3-1-origami"] = {
    "name": "The Origami Editorial Fold",
    "type": "Dimensional Paper Fold (Figma style)",
    "idea": "An archival parchment plane folding across 45-deg geometric creases to form an architectural K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s31-title">
  <title id="s31-title">Klyph S3 - The Origami Editorial Fold</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Front vertical pillar -->
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#00f0ff"/>
  <!-- Upper fold facet: light cyan -->
  <polygon points="96,132 176,52 216,52 136,132" fill="#00f0ff"/>
  <!-- Lower under-fold facet: deeper lapis tone creating physical depth -->
  <polygon points="120,116 200,196 160,196 96,132" fill="#0284c7"/>
  <!-- Central golden amber keystone crease -->
  <polygon points="96,132 120,108 144,132 120,156" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s31-title">
  <title id="s31-title">Klyph S3 - The Origami Editorial Fold Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#0284c7"/>
  <polygon points="96,132 176,52 216,52 136,132" fill="#0284c7"/>
  <polygon points="120,116 200,196 160,196 96,132" fill="#0369a1"/>
  <polygon points="96,132 120,108 144,132 120,156" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# S3-2: The Continuous Monoline Ribbon (Airbnb / Meta style)
# Single continuous 28px vector path looping into a dynamic editorial K.
# ---------------------------------------------------------------------------
SUITE3_CONCEPTS["s3-2-monoline"] = {
    "name": "The Continuous Monoline Loop",
    "type": "Single-Stroke Ribbon (Airbnb style)",
    "idea": "A continuous unbroken monoline path looping into an infinite editorial K with an amber nucleus.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s32-title">
  <title id="s32-title">Klyph S3 - The Continuous Monoline Loop</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Continuous vertical spine -->
  <rect x="52" y="44" width="32" height="168" rx="16" fill="#00f0ff"/>
  <!-- Continuous upper diagonal loop arm -->
  <path d="M100 128 L176 52 H212 L136 128 Z" fill="#00f0ff"/>
  <!-- Continuous lower diagonal loop arm -->
  <path d="M136 128 L212 204 H176 L100 128 Z" fill="#00f0ff"/>
  <!-- Amber nexus aperture dot -->
  <circle cx="118" cy="128" r="16" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s32-title">
  <title id="s32-title">Klyph S3 - The Continuous Monoline Loop Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="32" height="168" rx="16" fill="#0284c7"/>
  <path d="M100 128 L176 52 H212 L136 128 Z" fill="#0284c7"/>
  <path d="M136 128 L212 204 H176 L100 128 Z" fill="#0284c7"/>
  <circle cx="118" cy="128" r="16" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# S3-3: The Isometric Diamond Ingot (Scale AI / Ethereum style)
# Solid 45-deg geometric diamond ingot with precision negative-space cuts sculpting K.
# ---------------------------------------------------------------------------
SUITE3_CONCEPTS["s3-3-diamond"] = {
    "name": "The Isometric Diamond Ingot",
    "type": "Isometric Diamond Ingot (Scale AI style)",
    "idea": "A monumental 45-deg diamond ingot with precision negative-space light channels sculpting an architectural K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s33-title">
  <title id="s33-title">Klyph S3 - The Isometric Diamond Ingot</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Outer 45-deg diamond ingot -->
  <polygon points="128,40 216,128 128,216 40,128" fill="#00f0ff"/>
  <!-- Negative-space vertical channel -->
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#080b10"/>
  <!-- Negative-space upper diagonal channel -->
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#080b10"/>
  <!-- Negative-space lower diagonal channel -->
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#080b10"/>
  <!-- Central amber keystone jewel -->
  <polygon points="116,114 130,128 116,142 102,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s33-title">
  <title id="s33-title">Klyph S3 - The Isometric Diamond Ingot Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <polygon points="128,40 216,128 128,216 40,128" fill="#0284c7"/>
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#fbfaf6"/>
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#fbfaf6"/>
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#fbfaf6"/>
  <polygon points="116,114 130,128 116,142 102,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# S3-4: The AST Syntax Lattice (GraphQL / Anthropic style)
# Connected network graph of precision nodes forming a radiant syntax tree K.
# ---------------------------------------------------------------------------
SUITE3_CONCEPTS["s3-4-lattice"] = {
    "name": "The AST Syntax Lattice",
    "type": "Network Constellation (GraphQL / Anthropic style)",
    "idea": "A mathematical constellation of syntax nodes and 45-deg lattice struts forming a radiant K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s34-title">
  <title id="s34-title">Klyph S3 - The AST Syntax Lattice</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Vertical foundation trunk -->
  <rect x="64" y="68" width="16" height="120" rx="4" fill="#00f0ff"/>
  <!-- Upper 45-deg lattice strut -->
  <polygon points="128,116 184,60 196,72 140,128" fill="#00f0ff"/>
  <!-- Lower 45-deg lattice strut -->
  <polygon points="140,128 196,184 184,196 128,140" fill="#00f0ff"/>
  <!-- Left root nodes -->
  <circle cx="72" cy="68" r="20" fill="#00f0ff"/>
  <circle cx="72" cy="188" r="20" fill="#00f0ff"/>
  <!-- Right branch nodes -->
  <circle cx="190" cy="66" r="20" fill="#00f0ff"/>
  <circle cx="190" cy="190" r="20" fill="#00f0ff"/>
  <!-- Center amber semantic nucleus -->
  <circle cx="128" cy="128" r="24" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="s34-title">
  <title id="s34-title">Klyph S3 - The AST Syntax Lattice Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="64" y="68" width="16" height="120" rx="4" fill="#0284c7"/>
  <polygon points="128,116 184,60 196,72 140,128" fill="#0284c7"/>
  <polygon points="140,128 196,184 184,196 128,140" fill="#0284c7"/>
  <circle cx="72" cy="68" r="20" fill="#0284c7"/>
  <circle cx="72" cy="188" r="20" fill="#0284c7"/>
  <circle cx="190" cy="66" r="20" fill="#0284c7"/>
  <circle cx="190" cy="190" r="20" fill="#0284c7"/>
  <circle cx="128" cy="128" r="24" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts/suite3", exist_ok=True)
    for cid, data in SUITE3_CONCEPTS.items():
        dark_path = f"concepts/suite3/{cid}-dark.svg"
        light_path = f"concepts/suite3/{cid}-light.svg"
        symbol_path = f"concepts/suite3/{cid}.svg"

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(data["light"].strip() + "\n")
        with open(symbol_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")

        # Responsive SVG
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

        with open(f"concepts/suite3/{cid}-responsive.svg", "w", encoding="utf-8") as f:
            f.write(resp_svg)

        print(f"Generated Suite 3 SVGs for {cid}")

if __name__ == "__main__":
    main()
