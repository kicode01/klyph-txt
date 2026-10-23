"""
Refined Master Concepts for Klyph following logo-design-skill Phase 5 Refinements.
Focus on optical balance, elimination of disconnected crumbs, unified stroke anatomy,
freestanding scalability, and master-level craft.
"""

import os

REFINED_CONCEPTS = {}

# ---------------------------------------------------------------------------
# REFINEMENT 1: The Architectural Chisel (Unified Master)
# The floating diamond is now an integral faceted keystone that locks the stem
# and arms into a single harmonious architectural gesture.
# ---------------------------------------------------------------------------
REFINED_CONCEPTS["ref-1-chisel-master"] = {
    "name": "The Architectural Chisel (Master)",
    "type": "Architectural Letterform",
    "idea": "An architectural vertical pillar with dual 45-deg chisel planes locked into an integrated amber keystone.",
    # Freestanding (no background tile, pure mark)
    "standalone_dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r1-title">
  <title id="r1-title">Klyph Refined 1 - The Architectural Chisel Master</title>
  <!-- Vertical foundation pillar -->
  <rect x="44" y="36" width="40" height="184" rx="8" fill="#00f0ff"/>
  <!-- Upper 45-deg chisel blade -->
  <path d="M104 128 L180 52 H220 L136 136 Z" fill="#00f0ff"/>
  <!-- Lower 45-deg foundation blade -->
  <path d="M136 120 L220 204 H180 L104 128 Z" fill="#00f0ff"/>
  <!-- Interlocking golden keystone diamond -->
  <polygon points="104,128 128,104 152,128 128,152" fill="#f59e0b"/>
</svg>""",
    # Tile Dark
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r1-title">
  <title id="r1-title">Klyph Refined 1 - The Architectural Chisel Master</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Vertical foundation pillar -->
  <rect x="48" y="40" width="38" height="176" rx="8" fill="#00f0ff"/>
  <!-- Upper 45-deg chisel blade -->
  <path d="M104 128 L180 52 H216 L136 132 Z" fill="#00f0ff"/>
  <!-- Lower 45-deg foundation blade -->
  <path d="M136 124 L216 204 H180 L104 128 Z" fill="#00f0ff"/>
  <!-- Interlocking golden keystone diamond -->
  <polygon points="104,128 126,106 148,128 126,150" fill="#f59e0b"/>
</svg>""",
    # Tile Light
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r1-title">
  <title id="r1-title">Klyph Refined 1 - The Architectural Chisel Master Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="48" y="40" width="38" height="176" rx="8" fill="#0284c7"/>
  <path d="M104 128 L180 52 H216 L136 132 Z" fill="#0284c7"/>
  <path d="M136 124 L216 204 H180 L104 128 Z" fill="#0284c7"/>
  <polygon points="104,128 126,106 148,128 126,150" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# REFINEMENT 2: The Continuous Kinetic Chevron (Linear / Vercel Master)
# Extreme geometric reduction: an unbroken 45-deg chevron with an integrated
# negative-space aperture and chiseled apex.
# ---------------------------------------------------------------------------
REFINED_CONCEPTS["ref-2-chevron-kinetic"] = {
    "name": "The Continuous Kinetic Chevron",
    "type": "Minimalist Monogram (Linear / Vercel style)",
    "idea": "A monolithic pillar paired with an unbroken 45-deg chevron prism with an integrated amber nexus.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r2-title">
  <title id="r2-title">Klyph Refined 2 - The Continuous Kinetic Chevron</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Vertical pillar with subtle 45-deg beveled terminals -->
  <path d="M52 52 L60 44 H88 V212 H60 L52 204 Z" fill="#00f0ff"/>
  <!-- Continuous 45-deg chevron prism -->
  <path d="M112 128 L188 52 H220 L144 128 L220 204 H188 Z" fill="#00f0ff"/>
  <!-- Inset golden amber keystone eye -->
  <polygon points="120,116 132,128 120,140 108,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r2-title">
  <title id="r2-title">Klyph Refined 2 - The Continuous Kinetic Chevron Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M52 52 L60 44 H88 V212 H60 L52 204 Z" fill="#0284c7"/>
  <path d="M112 128 L188 52 H220 L144 128 L220 204 H188 Z" fill="#0284c7"/>
  <polygon points="120,116 132,128 120,140 108,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# REFINEMENT 3: The Dimensional Editorial Prism (Figma / Stripe Master)
# Pure isometric flat planes creating physical depth and tactile craft.
# ---------------------------------------------------------------------------
REFINED_CONCEPTS["ref-3-editorial-prism"] = {
    "name": "The Dimensional Editorial Prism",
    "type": "Isometric Dimensional Prism (Figma / Stripe style)",
    "idea": "Archival editorial planes folding across 45-deg isometric facets with dual-tone relief and an amber apex.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r3-title">
  <title id="r3-title">Klyph Refined 3 - The Dimensional Editorial Prism</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Front vertical foundation pillar -->
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#00f0ff"/>
  <!-- Upper fold blade: pure cyan -->
  <polygon points="100,128 176,52 216,52 140,128" fill="#00f0ff"/>
  <!-- Lower foundation facet: deeper lapis tone creating physical depth -->
  <polygon points="120,116 196,192 160,192 96,128" fill="#0284c7"/>
  <!-- Central golden amber keystone hinge -->
  <polygon points="100,128 124,104 148,128 124,152" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r3-title">
  <title id="r3-title">Klyph Refined 3 - The Dimensional Editorial Prism Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#0284c7"/>
  <polygon points="100,128 176,52 216,52 140,128" fill="#0284c7"/>
  <polygon points="120,116 196,192 160,192 96,128" fill="#0369a1"/>
  <polygon points="100,128 124,104 148,128 124,152" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# REFINEMENT 4: The Monumental Glyphic Ingot (Chase / National Geographic Master)
# Solid cyan medallion with razor-sharp stencil incisions carving an unyielding K.
# ---------------------------------------------------------------------------
REFINED_CONCEPTS["ref-4-stencil-ingot"] = {
    "name": "The Monumental Glyphic Ingot",
    "type": "Authoritative Negative-Space Ingot (Chermayeff & Geismar style)",
    "idea": "A monumental solid cyan medallion carved with precision laser stencil incisions into an unyielding K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r4-title">
  <title id="r4-title">Klyph Refined 4 - The Monumental Glyphic Ingot</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Solid cyan stone medallion -->
  <circle cx="128" cy="128" r="88" fill="#00f0ff"/>
  <!-- Negative-space vertical channel -->
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#080b10"/>
  <!-- Negative-space upper diagonal channel -->
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#080b10"/>
  <!-- Negative-space lower diagonal channel -->
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#080b10"/>
  <!-- Central golden amber keystone jewel -->
  <polygon points="116,114 130,128 116,142 102,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r4-title">
  <title id="r4-title">Klyph Refined 4 - The Monumental Glyphic Ingot Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <circle cx="128" cy="128" r="88" fill="#0284c7"/>
  <rect x="76" y="56" width="28" height="144" rx="4" fill="#fbfaf6"/>
  <path d="M112 132 L168 76 H192 L128 140 Z" fill="#fbfaf6"/>
  <path d="M128 116 L192 180 H168 L112 124 Z" fill="#fbfaf6"/>
  <polygon points="116,114 130,128 116,142 102,128" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts/refined", exist_ok=True)
    for cid, data in REFINED_CONCEPTS.items():
        dark_path = f"concepts/refined/{cid}-dark.svg"
        light_path = f"concepts/refined/{cid}-light.svg"
        symbol_path = f"concepts/refined/{cid}.svg"

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(data["light"].strip() + "\n")
        with open(symbol_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")

        # Responsive version
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

        with open(f"concepts/refined/{cid}-responsive.svg", "w", encoding="utf-8") as f:
            f.write(resp_svg)

        print(f"Generated refined SVGs for {cid}")

if __name__ == "__main__":
    main()
