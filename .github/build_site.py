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
<script>
  (function () {{
    try {{
      var t = localStorage.getItem("theme");
      if (t) document.documentElement.setAttribute("data-theme", t);
    }} catch (e) {{}}
  }})();
</script>
<style>
  :root {{
    --fond: #ffffff; --carte: #ffffff; --texte: #111111;
    --discret: #5c5c5c; --bord: #dcdcdc; --accent: #111111;
    color-scheme: light;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --fond: #0e0e0e; --carte: #171717; --texte: #f2f2f2;
      --discret: #a3a3a3; --bord: #333333; --accent: #ffffff;
      color-scheme: dark;
    }}
  }}
  :root[data-theme="dark"] {{
    --fond: #0e0e0e; --carte: #171717; --texte: #f2f2f2;
    --discret: #a3a3a3; --bord: #333333; --accent: #ffffff;
    color-scheme: dark;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--fond); color: var(--texte);
    font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
    transition: background .2s, color .2s;
  }}
  .enveloppe {{ max-width: 960px; margin: 0 auto; padding: 4rem 1.5rem 5rem; }}
  header {{ border-bottom: 1px solid var(--bord); padding-bottom: 2rem; margin-bottom: 2.5rem;
            display: flex; gap: 1rem; align-items: flex-start; justify-content: space-between; }}
  h1 {{ font-size: clamp(1.8rem, 4vw, 2.6rem); margin: 0 0 .6rem; letter-spacing: -.02em; }}
  header p {{ margin: 0; color: var(--discret); }}
  .bascule {{
    flex: none; display: inline-flex; align-items: center; gap: .45rem;
    padding: .5rem .9rem; font: inherit; font-size: .85rem; cursor: pointer;
    color: var(--texte); background: var(--carte);
    border: 1px solid var(--bord); border-radius: 999px;
    transition: border-color .15s;
  }}
  .bascule:hover {{ border-color: var(--texte); }}
  .bascule:focus-visible {{ outline: 2px solid var(--texte); outline-offset: 2px; }}
  .bascule svg {{ width: 1rem; height: 1rem; }}
  .grille {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}
  .carte {{
    display: block; padding: 1.4rem; text-decoration: none; color: inherit;
    background: var(--carte); border: 1px solid var(--bord); border-radius: 10px;
    transition: border-color .15s, transform .15s;
  }}
  .carte:hover {{ border-color: var(--texte); transform: translateY(-2px); }}
  .carte h2 {{ font-size: 1.05rem; margin: 0 0 .35rem; color: var(--accent); }}
  .soustitre {{ margin: 0 0 .7rem; font-size: .85rem; color: var(--discret);
                font-family: ui-monospace, SFMono-Regular, Menlo, monospace; word-break: break-all; }}
  .meta {{ margin: 0; font-size: .8rem; color: var(--discret); font-variant-numeric: tabular-nums; }}
  footer {{ margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--bord);
            color: var(--discret); font-size: .85rem; }}
  footer a {{ color: var(--accent); }}
  @media (max-width: 520px) {{ header {{ flex-direction: column-reverse; }} }}
</style>
</head>
<body>
  <div class="enveloppe">
    <header>
      <h1>Projets d'analyse de donnees</h1>
      <p>{nombre} notebooks Python &middot; {images} graphiques &middot; pandas, seaborn, matplotlib</p>
      <button class="bascule" type="button" id="bascule" aria-label="Changer de theme">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>
        <span id="bascule-texte">Mode sombre</span>
      </button>
    </header>
    <main class="grille">
{cartes}
    </main>
    <footer>
      Pages generees depuis les notebooks du depot
      <a href="https://github.com/Tsamh/Data_processing">Tsamh/Data_processing</a>.
    </footer>
  </div>
  <script>
    (function () {{
      var racine = document.documentElement;
      var texte = document.getElementById("bascule-texte");
      function actuel() {{
        return racine.getAttribute("data-theme") ||
          (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      }}
      function maj() {{ texte.textContent = actuel() === "dark" ? "Mode clair" : "Mode sombre"; }}
      document.getElementById("bascule").addEventListener("click", function () {{
        var t = actuel() === "dark" ? "light" : "dark";
        racine.setAttribute("data-theme", t);
        try {{ localStorage.setItem("theme", t); }} catch (e) {{}}
        maj();
      }});
      maj();
    }})();
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
