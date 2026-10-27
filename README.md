# accessibilitenumerique.eu

Site statique multilingue (FR, NL, DE, EN) — 28 pages par langue, 112 pages au total.

## Structure
- `gen/content_fr.py`, `content_nl.py`, `content_de.py`, `content_en.py` : tous les textes du site, langue par langue.
- `gen/common.py` : arborescence et URL traduites.
- `templates/` : gabarits HTML (Jinja2).
- `static/` : feuille de style, scripts, police Manrope hébergée localement, logos.
- `gen/build.py` : génération.

## Articles du blog
- Un fichier JSON par article et par langue dans `gen/articles/<id>.<lang>.json` (8 articles × 4 langues).
- Cahier des charges : `gen/articles/SPEC.md` ; consignes de traduction : `gen/articles/TRANSLATION.md`.
- Contrôle d'un article : `python3 gen/check_article.py gen/articles/<id>.<lang>.json 3500`.
- Un article n'est publié que s'il existe dans les 4 langues (liste `ARTICLES` dans `gen/common.py`).

## Générer
    pip install -r requirements.txt
    python3 gen/build.py prod          # -> dist/ (URL propres, sitemap, robots.txt, _headers)
    python3 gen/build.py preview       # -> preview/ (liens relatifs, consultable hors ligne)

Le formulaire de contact envoie un JSON en POST vers l'URL définie au moment du build :

    FORM_ENDPOINT="https://hook.eu1.make.com/yzzl9yt5enats8we3umgcgw1x0g53rt6" python3 gen/build.py prod   # valeur par défaut déjà intégrée

## Déployer (Cloudflare Workers, gratuit)
Le dossier `dist/` est versionné : le site est déployable tel quel, sans étape de build.

    npx wrangler deploy

Avec le déploiement automatique depuis GitHub (Cloudflare Workers Builds) : commande de build vide
(ou `python3 gen/build.py prod` après avoir modifié les textes), commande de déploiement `npx wrangler deploy`.

Puis, dans Cloudflare : ajouter le domaine accessibilitenumerique.eu au Worker (Custom domain),
après avoir pointé les serveurs de noms du domaine IONOS vers Cloudflare.
