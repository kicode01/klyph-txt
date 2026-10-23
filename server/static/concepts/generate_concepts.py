"""
Generate 4 distinct logo design concepts for Klyph following logo-design-skill.
Each concept represents a fundamentally different visual archetype:
1. Concept A: The Architectural Chisel (Monolithic Letterform)
2. Concept B: The Editorial Feather Quill (Pictorial Geometric Reduction)
3. Concept C: The AST Syntax Tree (Computational Abstract / Parse Nodes)
4. Concept D: The Glyphic Medallion (Negative-Space Stencil Seal)
"""

import os

CONCEPTS = {}

# ---------------------------------------------------------------------------
# CONCEPT A: The Architectural Chisel (Monolithic Letterform)
# Vertical pillar with 45-deg dual chisel blades and interlocking keystone diamond.
# ---------------------------------------------------------------------------
CONCEPTS["concept-a-chisel"] = {
    "name": "The Architectural Chisel",
    "type": "Monolithic Letterform",
    "idea": "A monolithic vertical pillar with dual 45-deg chisel planes locked by a central amber keystone.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="ca-title">
  <title id="ca-title">Klyph Concept A - The Architectural Chisel</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#00f0ff"/>
  <path d="M96 136 L176 56 H216 L124 148 Z" fill="#00f0ff"/>
  <path d="M124 108 L216 200 H176 L96 120 Z" fill="#00f0ff"/>
  <polygon points="116,102 142,128 116,154 90,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="ca-title">
  <title id="ca-title">Klyph Concept A - The Architectural Chisel Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#0284c7"/>
  <path d="M96 136 L176 56 H216 L124 148 Z" fill="#0284c7"/>
  <path d="M124 108 L216 200 H176 L96 120 Z" fill="#0284c7"/>
  <polygon points="116,102 142,128 116,154 90,128" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT B: The Editorial Feather Quill (Pictorial Geometric Reduction)
# 45-deg angled writing quill composed of a central spine and geometric barbs forming K.
# ---------------------------------------------------------------------------
CONCEPTS["concept-b-quill"] = {
    "name": "The Editorial Feather Quill",
    "type": "Pictorial Geometric Reduction",
    "idea": "An energetic 45-deg writing quill whose geometric vanes and ink nib outline an italic letter K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cb-title">
  <title id="cb-title">Klyph Concept B - The Editorial Feather Quill</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Central quill shaft angled at 45 deg -->
  <path d="M72 196 L196 72 L184 60 L60 184 Z" fill="#00f0ff"/>
  <!-- Upper feather vane / upper K arm -->
  <path d="M116 116 L160 72 H200 L140 132 Z" fill="#00f0ff"/>
  <!-- Lower feather vane / lower K arm -->
  <path d="M136 136 L196 196 H156 L112 152 Z" fill="#00f0ff"/>
  <!-- Golden ink nib / writing tip -->
  <polygon points="60,184 72,196 52,216 40,204" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cb-title">
  <title id="cb-title">Klyph Concept B - The Editorial Feather Quill Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <path d="M72 196 L196 72 L184 60 L60 184 Z" fill="#0284c7"/>
  <path d="M116 116 L160 72 H200 L140 132 Z" fill="#0284c7"/>
  <path d="M136 136 L196 196 H156 L112 152 Z" fill="#0284c7"/>
  <polygon points="60,184 72,196 52,216 40,204" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT C: The AST Syntax Tree (Computational Abstract / Parse Nodes)
# Vertical anchor stem with floating 45-deg syntax chevrons (> <) and central circular semantic node.
# ---------------------------------------------------------------------------
CONCEPTS["concept-c-syntax"] = {
    "name": "The AST Syntax Tree",
    "type": "Computational Abstract",
    "idea": "An editorial anchor stem paired with floating syntax chevrons (> <) orbiting a circular parse node.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cc-title">
  <title id="cc-title">Klyph Concept C - The AST Syntax Tree</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Vertical token anchor -->
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#00f0ff"/>
  <!-- Floating upper syntax chevron -->
  <path d="M120 112 L184 48 H212 L136 124 Z" fill="#00f0ff"/>
  <!-- Floating lower syntax chevron -->
  <path d="M136 132 L212 208 H184 L120 144 Z" fill="#00f0ff"/>
  <!-- Circular AST root parse node -->
  <circle cx="116" cy="128" r="16" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cc-title">
  <title id="cc-title">Klyph Concept C - The AST Syntax Tree Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <rect x="52" y="44" width="36" height="168" rx="6" fill="#0284c7"/>
  <path d="M120 112 L184 48 H212 L136 124 Z" fill="#0284c7"/>
  <path d="M136 132 L212 208 H184 L120 144 Z" fill="#0284c7"/>
  <circle cx="116" cy="128" r="16" fill="#d97706"/>
</svg>"""
}

# ---------------------------------------------------------------------------
# CONCEPT D: The Glyphic Medallion (Negative-Space Stencil Seal)
# High-contrast solid disc with negative space incisions sculpting an architectural K.
# ---------------------------------------------------------------------------
CONCEPTS["concept-d-seal"] = {
    "name": "The Glyphic Medallion",
    "type": "Negative-Space Inscription",
    "idea": "A monolithic cyan stone medallion with razor-sharp stencil incisions carving an architectural K.",
    "dark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cd-title">
  <title id="cd-title">Klyph Concept D - The Glyphic Medallion</title>
  <rect width="256" height="256" rx="60" fill="#080b10"/>
  <!-- Solid cyan stone medallion -->
  <circle cx="128" cy="128" r="88" fill="#00f0ff"/>
  <!-- Incised negative-space vertical channel -->
  <rect x="80" y="56" width="28" height="144" rx="4" fill="#080b10"/>
  <!-- Incised negative-space upper diagonal channel -->
  <path d="M116 132 L172 76 H196 L132 140 Z" fill="#080b10"/>
  <!-- Incised negative-space lower diagonal channel -->
  <path d="M132 116 L196 180 H172 L116 124 Z" fill="#080b10"/>
  <!-- Inset golden keystone jewel -->
  <polygon points="120,114 134,128 120,142 106,128" fill="#f59e0b"/>
</svg>""",
    "light": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="cd-title">
  <title id="cd-title">Klyph Concept D - The Glyphic Medallion Light</title>
  <rect width="256" height="256" rx="60" fill="#fbfaf6"/>
  <circle cx="128" cy="128" r="88" fill="#0284c7"/>
  <rect x="80" y="56" width="28" height="144" rx="4" fill="#fbfaf6"/>
  <path d="M116 132 L172 76 H196 L132 140 Z" fill="#fbfaf6"/>
  <path d="M132 116 L196 180 H172 L116 124 Z" fill="#fbfaf6"/>
  <polygon points="120,114 134,128 120,142 106,128" fill="#d97706"/>
</svg>"""
}

def main():
    os.makedirs("concepts", exist_ok=True)
    for cid, data in CONCEPTS.items():
        dark_path = f"concepts/{cid}-dark.svg"
        light_path = f"concepts/{cid}-light.svg"
        symbol_path = f"concepts/{cid}.svg"

        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(data["light"].strip() + "\n")
        with open(symbol_path, "w", encoding="utf-8") as f:
            f.write(data["dark"].strip() + "\n")

        # Also generate responsive SVG with @media (prefers-color-scheme)
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
        # Parse inner elements of dark SVG and replace static fills with classes
        inner = data["dark"].split('</title>', 1)[1].rsplit('</svg>', 1)[0]
        # Replace fills
        inner = inner.replace('fill="#080b10"', 'class="klyph-base"')
        inner = inner.replace('fill="#00f0ff"', 'class="klyph-glyph"')
        inner = inner.replace('fill="#f59e0b"', 'class="klyph-keystone"')
        resp_svg += inner.strip() + "\n</svg>\n"

        with open(f"concepts/{cid}-responsive.svg", "w", encoding="utf-8") as f:
            f.write(resp_svg)

        print(f"Generated SVGs for {cid}")

if __name__ == "__main__":
    main()
