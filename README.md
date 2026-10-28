# accessibilitenumerique.eu

Site statique multilingue (FR, NL, DE, EN) — 28 pages par langue, 112 pages au total.

## Structure
- `gen/content_fr.py`, `content_nl.py`, `content_de.py`, `content_en.py` : tous les textes du site, langue par langue.
- `gen/common.py` : arborescence et URL traduites.
- `templates/` : gabarits HTML (Jinja2).
- `static/` : feuille de style, scripts, police Manrope hébergée localement, logos.
- `gen/build.py` : génération.

## Articles du blog
- Un fichier JSON par article et par langue dans `gen/articles/<id>.<lang>.json`, découverts automatiquement.
- Ligne éditoriale, silos, maillage et procédure : `gen/articles/EDITORIAL.md` ; format : `SPEC.md` ; traductions : `TRANSLATION.md` ; file des sujets : `CALENDAR.md`.
- Contrôles : `python3 gen/check_article.py <fichier> 3500`, `python3 gen/maillage.py [<id>]`, `python3 gen/check_site.py` (après build prod), `node tools/axe.cjs [chemins]` (après build preview, `npm install --no-save axe-core`).
- Un article n'est publié que s'il existe dans les 4 langues.

## Générer
    pip install jinja2
    python3 gen/build.py prod          # -> dist/ (URL propres, sitemap, robots.txt, _headers)
    python3 gen/build.py preview       # -> preview/ (liens relatifs, consultable hors ligne)

Le formulaire de contact envoie un JSON en POST vers l'URL définie au moment du build :

    FORM_ENDPOINT="https://hook.eu1.make.com/yzzl9yt5enats8we3umgcgw1x0g53rt6" python3 gen/build.py prod   # valeur par défaut déjà intégrée

## Déployer (Cloudflare Workers, gratuit)
    npx wrangler deploy

Puis, dans Cloudflare : ajouter le domaine accessibilitenumerique.eu au Worker (Custom domain),
après avoir pointé les serveurs de noms du domaine IONOS vers Cloudflare.
