"""Convertit chaque notebook du depot en page HTML autonome et genere l'accueil."""

import html
import json
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "_site"


def titre_notebook(nb):
    """Premier titre markdown du notebook, s'il existe."""
    for cellule in nb.get("cells", []):
        if cellule.get("cell_type") == "markdown":
            texte = "".join(cellule["source"]).strip()
            if texte.startswith("# "):
                return texte[2:].split("\n")[0].strip()
    return ""


def statistiques(nb):
    cellules = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    images = sum(
        1
        for c in cellules
        for o in c.get("outputs", [])
        if any(k.startswith("image/") for k in (o.get("data") or {}))
    )
    return len(cellules), images


def main():
    SORTIE.mkdir(exist_ok=True)
    notebooks = sorted(
        p for p in RACINE.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts
    )
    if not notebooks:
        sys.exit("Aucun notebook trouve.")

    fiches = []
    for chemin in notebooks:
        nom = chemin.parent.name if chemin.parent != RACINE else chemin.stem
        nb = json.loads(chemin.read_text(encoding="utf-8"))
        subprocess.run(
            [
                sys.executable, "-m", "nbconvert",
                "--to", "html", "--embed-images",
                "--output", nom, "--output-dir", str(SORTIE),
                str(chemin),
            ],
            check=True,
        )
        blocs, images = statistiques(nb)
        fiches.append(
            {
                "url": f"{nom}.html",
                "titre": nom.replace("_", " ").capitalize(),
                "fichier": chemin.name,
                "blocs": blocs,
                "images": images,
            }
        )

    cartes = "\n".join(
        f"""      <a class="carte" href="{f['url']}">
        <h2>{html.escape(f['titre'])}</h2>
        <p class="soustitre">{html.escape(f['fichier'])}</p>
        <p class="meta">{f['blocs']} blocs de code &middot; {f['images']} graphique{'s' if f['images'] > 1 else ''}</p>
      </a>"""
        for f in fiches
    )

    total_images = sum(f["images"] for f in fiches)
    (SORTIE / "index.html").write_text(
        PAGE.format(cartes=cartes, nombre=len(fiches), images=total_images),
        encoding="utf-8",
    )
    print(f"{len(fiches)} notebooks convertis dans {SORTIE}")


PAGE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Projets d'analyse de donnees</title>
<style>
  :root {{
    --fond: #fbfaf8; --carte: #ffffff; --texte: #1b1a18;
    --discret: #6a655e; --bord: #e4e0da; --accent: #b4541f;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --fond: #161513; --carte: #201f1c; --texte: #ece9e4;
      --discret: #9b958c; --bord: #33312d; --accent: #e08b52;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--fond); color: var(--texte);
    font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  .enveloppe {{ max-width: 960px; margin: 0 auto; padding: 4rem 1.5rem 5rem; }}
  header {{ border-bottom: 1px solid var(--bord); padding-bottom: 2rem; margin-bottom: 2.5rem; }}
  h1 {{ font-size: clamp(1.8rem, 4vw, 2.6rem); margin: 0 0 .6rem; letter-spacing: -.02em; }}
  header p {{ margin: 0; color: var(--discret); }}
  .grille {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}
  .carte {{
    display: block; padding: 1.4rem; text-decoration: none; color: inherit;
    background: var(--carte); border: 1px solid var(--bord); border-radius: 10px;
    transition: border-color .15s, transform .15s;
  }}
  .carte:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
  .carte h2 {{ font-size: 1.05rem; margin: 0 0 .35rem; color: var(--accent); }}
  .soustitre {{ margin: 0 0 .7rem; font-size: .85rem; color: var(--discret);
                font-family: ui-monospace, SFMono-Regular, Menlo, monospace; word-break: break-all; }}
  .meta {{ margin: 0; font-size: .8rem; color: var(--discret); font-variant-numeric: tabular-nums; }}
  footer {{ margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--bord);
            color: var(--discret); font-size: .85rem; }}
  footer a {{ color: var(--accent); }}
</style>
</head>
<body>
  <div class="enveloppe">
    <header>
      <h1>Projets d'analyse de donnees</h1>
      <p>{nombre} notebooks Python &middot; {images} graphiques &middot; pandas, seaborn, matplotlib</p>
    </header>
    <main class="grille">
{cartes}
    </main>
    <footer>
      Pages generees depuis les notebooks du depot
      <a href="https://github.com/Tsamh/Data_processing">Tsamh/Data_processing</a>.
    </footer>
  </div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
