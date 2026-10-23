"""
Generate 4 Tier-1 Enterprise Brand-Mark Concepts for Klyph following logo-design-skill.
Modeled after elite design firm work (Pentagram, Chermayeff & Geismar & Haviv, Collins).
Ultra-confident, extreme reduction, mathematical precision, zero amateur clutter.
"""

import os

ENTERPRISE_CONCEPTS = {}

# ---------------------------------------------------------------------------
# CONCEPT E1: The Monolith Ingot (Linear / Vercel Pedigree)
# A monumental vertical anchor slab with dual 45-deg forward-folded chisel blades.
# Extreme geometric economy: two pure forms separated by precision 16px light channels.
# ---------------------------------------------------------------------------
ENTERPRISE_CONCEPTS["ent-1-ingot"] = {
    "name": "The Monolith Ingot",
    "type": "Monumental Monogram (Linear / Vercel style)",
    "idea": "A monolithic vertical anchor slab paired with dual forward-folded 45-deg chisel blades.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e1-title">
  <title id="e1-title">Klyph Enterprise 1 - The Monolith Ingot</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Left monolithic vertical anchor -->
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#00f0ff"/>
  <!-- Upper 45-deg forward-folded chisel blade -->
  <path d="M108 120 L184 44 H220 L144 120 Z" fill="#00f0ff"/>
  <!-- Lower 45-deg foundation blade -->
  <path d="M144 136 L220 212 H184 L108 136 Z" fill="#00f0ff"/>
  <!-- Golden refraction nucleus -->
  <polygon points="120,116 132,128 120,140 108,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e1-title">
  <title id="e1-title">Klyph Enterprise 1 - The Monolith Ingot Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#0284c7"/>
  <path d="M108 120 L184 44 H220 L144 120 Z" fill="#0284c7"/>
  <path d="M144 136 L220 212 H184 L108 136 Z" fill="#0284c7"/>
  <polygon points="120,116 132,128 120,140 108,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT E2: The Modular Tessellation / Tri-Prism (Framer / Dropbox Pedigree)
# Three pure geometric prisms tessellating into an unmistakable architectural K.
# ---------------------------------------------------------------------------
ENTERPRISE_CONCEPTS["ent-2-prism"] = {
    "name": "The Modular Tessellation",
    "type": "Modular Geometric Prism (Framer / Dropbox style)",
    "idea": "Three pure architectural polygons tessellating into an impossible geometric K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e2-title">
  <title id="e2-title">Klyph Enterprise 2 - The Modular Tessellation</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Pillar: pure vertical foundation -->
  <path d="M52 44 H92 V212 H52 Z" fill="#00f0ff"/>
  <!-- Upper facet: 45-deg right-angled triangle -->
  <polygon points="108,44 196,44 108,132" fill="#00f0ff"/>
  <!-- Lower facet: 45-deg parallelogram -->
  <polygon points="108,124 196,212 108,212" fill="#00f0ff"/>
  <!-- Central golden keystone diamond linking the tessellation -->
  <polygon points="152,88 196,132 152,176 108,132" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e2-title">
  <title id="e2-title">Klyph Enterprise 2 - The Modular Tessellation Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M52 44 H92 V212 H52 Z" fill="#0284c7"/>
  <polygon points="108,44 196,44 108,132" fill="#0284c7"/>
  <polygon points="108,124 196,212 108,212" fill="#0284c7"/>
  <polygon points="152,88 196,132 152,176 108,132" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT E3: The Neural Aperture (Anthropic / OpenAI Pedigree)
# A rotational intelligence mark: three concentric aerodynamic blades carving a dynamic K.
# ---------------------------------------------------------------------------
ENTERPRISE_CONCEPTS["ent-3-aperture"] = {
    "name": "The Neural Aperture",
    "type": "Rotational Intelligence Symbol (Anthropic / OpenAI style)",
    "idea": "Three aerodynamic blades orbiting a golden nucleus, fusing language cadence with AI velocity.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e3-title">
  <title id="e3-title">Klyph Enterprise 3 - The Neural Aperture</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Left stem: aerodynamic vertical blade -->
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#00f0ff"/>
  <!-- Upper blade: 45-deg aerodynamic wing -->
  <path d="M104 120 L180 44 H216 L140 120 Z" fill="#00f0ff"/>
  <!-- Lower blade: 45-deg grounding stabilizer -->
  <path d="M140 136 L216 212 H180 L104 136 Z" fill="#00f0ff"/>
  <!-- Central golden circular aperture / parse nucleus -->
  <circle cx="122" cy="128" r="16" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e3-title">
  <title id="e3-title">Klyph Enterprise 3 - The Neural Aperture Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="8" fill="#0284c7"/>
  <path d="M104 120 L180 44 H216 L140 120 Z" fill="#0284c7"/>
  <path d="M140 136 L216 212 H180 L104 136 Z" fill="#0284c7"/>
  <circle cx="122" cy="128" r="16" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT E4: The Minimalist Glyphic Cut (Stripe / GitHub / Kotlin Pedigree)
# A monolithic solid squircle with a single mathematical diagonal incision carving the letter K.
# ---------------------------------------------------------------------------
ENTERPRISE_CONCEPTS["ent-4-cut"] = {
    "name": "The Minimalist Glyphic Cut",
    "type": "Monolithic Negative-Space Cut (Kotlin / Stripe style)",
    "idea": "A monolithic square tile with a single continuous triangular negative-space cut carving an indelible K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e4-title">
  <title id="e4-title">Klyph Enterprise 4 - The Minimalist Glyphic Cut</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Left solid foundation column -->
  <path d="M48 48 H96 V208 H48 Z" fill="#00f0ff"/>
  <!-- Upper diagonal facet -->
  <polygon points="112,48 208,48 112,144" fill="#00f0ff"/>
  <!-- Lower diagonal facet -->
  <polygon points="112,112 208,208 112,208" fill="#00f0ff"/>
  <!-- Floating amber nexus block -->
  <rect x="100" y="116" width="24" height="24" rx="4" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="e4-title">
  <title id="e4-title">Klyph Enterprise 4 - The Minimalist Glyphic Cut Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M48 48 H96 V208 H48 Z" fill="#0284c7"/>
  <polygon points="112,48 208,48 112,144" fill="#0284c7"/>
  <polygon points="112,112 208,208 112,208" fill="#0284c7"/>
  <rect x="100" y="116" width="24" height="24" rx="4" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts/enterprise", exist_ok=True)
    for cid, data in ENTERPRISE_CONCEPTS.items():
        dark_path = f"concepts/enterprise/{cid}-dark.svg"
        light_path = f"concepts/enterprise/{cid}-light.svg"
        symbol_path = f"concepts/enterprise/{cid}.svg"

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(data["light"].strip() + "\n")
        with open(symbol_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")

        print(f"Generated enterprise SVGs for {cid}")

if __name__ == "__main__":
    main()
