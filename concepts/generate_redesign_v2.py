"""
Revolutionary Redesign Concepts for Klyph following logo-design-skill.
Breaks away from blocky letter-K typography and introduces 4 distinct,
globally iconic metaphors:
1. Concept 1: The Editorial Flow Loop (Proofreader's loop & continuous revision flow)
2. Concept 2: The Aerodynamic Quill Wing (Sleek modern quill feather & nib)
3. Concept 3: The Human Cadence Spectrum (Rhythmic burstiness waves & voice pulse)
4. Concept 4: The Keystones Pinwheel (Four interlocking architectural stones forming a radiant glyph)
"""

import os

REDESIGN_CONCEPTS = {}

# ---------------------------------------------------------------------------
# CONCEPT 1: The Editorial Flow Loop (Proofreader's Dele Loop / Continuous Flow)
# Inspired by the classic proofreader's deletion/revision loop and the infinity
# of continuous thought. A sleek circular loop that sweeps into a sharp editorial check.
# ---------------------------------------------------------------------------
REDESIGN_CONCEPTS["redesign-1-loop"] = {
    "name": "The Editorial Flow Loop",
    "type": "Continuous Fluid Loop (Grammarly / Airbnb / Beats pedigree)",
    "idea": "A seamless continuous editorial loop sweeping from an archival circle into a razor-sharp revision check.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r1-title">
  <title id="r1-title">Klyph Redesign 1 - The Editorial Flow Loop</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Outer flowing circular crescent -->
  <path d="M128 36 C77 36 36 77 36 128 C36 179 77 220 128 220 C168 220 202 195 215 158 H178 C168 178 149 190 128 190 C94 190 66 162 66 128 C66 94 94 66 128 66 C152 66 173 80 183 100 L212 78 C194 52 163 36 128 36 Z" fill="#00f0ff"/>
  <!-- Inner forward editorial check gesture -->
  <path d="M112 128 L144 160 L220 84 L200 64 L144 120 L132 108 Z" fill="#00f0ff"/>
  <!-- Central golden accent focal point -->
  <circle cx="128" cy="128" r="14" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r1-title">
  <title id="r1-title">Klyph Redesign 1 - The Editorial Flow Loop Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M128 36 C77 36 36 77 36 128 C36 179 77 220 128 220 C168 220 202 195 215 158 H178 C168 178 149 190 128 190 C94 190 66 162 66 128 C66 94 94 66 128 66 C152 66 173 80 183 100 L212 78 C194 52 163 36 128 36 Z" fill="#0284c7"/>
  <path d="M112 128 L144 160 L220 84 L200 64 L144 120 L132 108 Z" fill="#0284c7"/>
  <circle cx="128" cy="128" r="14" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 2: The Aerodynamic Quill Wing (QuillBot / Linear / Apple pedigree)
# A hyper-sleek, minimalist feather quill that looks like a supersonic wing.
# Two curved aerodynamic blades meeting at an editorial ink nib.
# ---------------------------------------------------------------------------
REDESIGN_CONCEPTS["redesign-2-quill"] = {
    "name": "The Aerodynamic Quill Wing",
    "type": "Modernist Pictorial (QuillBot / Apple / Linear pedigree)",
    "idea": "An aerodynamic quill feather soaring diagonally, split by a precision editorial slit meeting at a golden ink tip.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r2-title">
  <title id="r2-title">Klyph Redesign 2 - The Aerodynamic Quill Wing</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Upper feather vane: soaring forward wing -->
  <path d="M72 184 C92 144 132 88 208 48 C188 88 176 132 172 164 L120 112 Z" fill="#00f0ff"/>
  <!-- Lower feather vane: grounding stabilizer -->
  <path d="M64 192 L120 136 L164 180 C140 200 112 212 80 216 Z" fill="#0284c7"/>
  <!-- Golden ink nib writing point -->
  <polygon points="56,200 72,184 64,192 48,208" fill="#f59e0b"/>
  <!-- Central breather aperture keystone -->
  <circle cx="120" cy="124" r="10" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r2-title">
  <title id="r2-title">Klyph Redesign 2 - The Aerodynamic Quill Wing Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M72 184 C92 144 132 88 208 48 C188 88 176 132 172 164 L120 112 Z" fill="#0284c7"/>
  <path d="M64 192 L120 136 L164 180 C140 200 112 212 80 216 Z" fill="#0369a1"/>
  <polygon points="56,200 72,184 64,192 48,208" fill="#d97706"/>
  <circle cx="120" cy="124" r="10" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 3: The Human Cadence Spectrum (Perplexity / Audio / Pulse pedigree)
# Three concentric rhythm arcs and a pulsing golden core expressing sentence
# length variance, human burstiness, and the natural heartbeat of prose.
# ---------------------------------------------------------------------------
REDESIGN_CONCEPTS["redesign-3-cadence"] = {
    "name": "The Human Cadence Spectrum",
    "type": "Kinetic Pulse & Spectrum (Dolby / Tidal / Humane pedigree)",
    "idea": "Concentric rhythm waves radiating from a golden nucleus, expressing the natural heartbeat and burstiness of prose.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r3-title">
  <title id="r3-title">Klyph Redesign 3 - The Human Cadence Spectrum</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Left foundational rhythm wave -->
  <path d="M68 64 C52 82 44 104 44 128 C44 152 52 174 68 192 L86 174 C75 160 68 145 68 128 C68 111 75 96 86 82 Z" fill="#00f0ff"/>
  <!-- Right upper cadence burst -->
  <path d="M188 64 C204 82 212 104 212 128 C212 152 204 174 188 192 L170 174 C181 160 188 145 188 128 C188 111 181 96 170 82 Z" fill="#00f0ff"/>
  <!-- Inner rhythm brackets -->
  <path d="M96 96 C88 105 84 116 84 128 C84 140 88 151 96 160 L112 144 C109 139 108 134 108 128 C108 122 109 117 112 112 Z" fill="#00f0ff"/>
  <path d="M160 96 C168 105 172 116 172 128 C172 140 168 151 160 160 L144 144 C147 139 148 134 148 128 C148 122 147 117 144 112 Z" fill="#00f0ff"/>
  <!-- Golden voice pulse core -->
  <circle cx="128" cy="128" r="14" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r3-title">
  <title id="r3-title">Klyph Redesign 3 - The Human Cadence Spectrum Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M68 64 C52 82 44 104 44 128 C44 152 52 174 68 192 L86 174 C75 160 68 145 68 128 C68 111 75 96 86 82 Z" fill="#0284c7"/>
  <path d="M188 64 C204 82 212 104 212 128 C212 152 204 174 188 192 L170 174 C181 160 188 145 188 128 C188 111 181 96 170 82 Z" fill="#0284c7"/>
  <path d="M96 96 C88 105 84 116 84 128 C84 140 88 151 96 160 L112 144 C109 139 108 134 108 128 C108 122 109 117 112 112 Z" fill="#0284c7"/>
  <path d="M160 96 C168 105 172 116 172 128 C172 140 168 151 160 160 L144 144 C147 139 148 134 148 128 C148 122 147 117 144 112 Z" fill="#0284c7"/>
  <circle cx="128" cy="128" r="14" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT 4: The Keystones Pinwheel (OpenAI / Chase / Slack pedigree)
# Four architectural keystones in rotational 45-deg symmetry.
# ---------------------------------------------------------------------------
REDESIGN_CONCEPTS["redesign-4-keystones"] = {
    "name": "The Keystones Pinwheel",
    "type": "Rotational Geometric Seal (OpenAI / Chase pedigree)",
    "idea": "Four architectural keystones interlocking in rotational symmetry around a central luminous diamond star.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r4-title">
  <title id="r4-title">Klyph Redesign 4 - The Keystones Pinwheel</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Top Keystone Diamond -->
  <polygon points="128,44 156,72 128,100 100,72" fill="#00f0ff"/>
  <!-- Right Keystone Diamond -->
  <polygon points="212,128 184,156 156,128 184,100" fill="#00f0ff"/>
  <!-- Bottom Keystone Diamond -->
  <polygon points="128,212 100,184 128,156 156,184" fill="#00f0ff"/>
  <!-- Left Keystone Diamond -->
  <polygon points="44,128 72,100 100,128 72,156" fill="#00f0ff"/>
  <!-- Central golden diamond keystone star -->
  <polygon points="128,112 144,128 128,144 112,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="r4-title">
  <title id="r4-title">Klyph Redesign 4 - The Keystones Pinwheel Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <polygon points="128,44 156,72 128,100 100,72" fill="#0284c7"/>
  <polygon points="212,128 184,156 156,128 184,100" fill="#0284c7"/>
  <polygon points="128,212 100,184 128,156 156,184" fill="#0284c7"/>
  <polygon points="44,128 72,100 100,128 72,156" fill="#0284c7"/>
  <polygon points="128,112 144,128 128,144 112,128" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts/redesign", exist_ok=True)
    for cid, data in REDESIGN_CONCEPTS.items():
        dark_path = f"concepts/redesign/{cid}-dark.svg"
        light_path = f"concepts/redesign/{cid}-light.svg"
        symbol_path = f"concepts/redesign/{cid}.svg"

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

        with open(f"concepts/redesign/{cid}-responsive.svg", "w", encoding="utf-8") as f:
            f.write(resp_svg)

        print(f"Generated redesign SVGs for {cid}")

if __name__ == "__main__":
    main()
