# Ligne éditoriale et procédure de publication du blog — accessibilitenumerique.eu

Ce document est la référence de toute publication sur le blog (rubrique Ressources). Il complète `SPEC.md` (format JSON, style, exactitude, contrôle) et `TRANSLATION.md` (versions NL, DE, EN), qui restent obligatoires. En cas de doute, la règle la plus stricte s'applique.

## 1. Objectif

Faire d'accessibilitenumerique.eu le site de référence sur l'accessibilité numérique en France, en Belgique, au Luxembourg et en Suisse, en français, néerlandais, allemand et anglais :
- premier sur la requête générique (« accessibilité numérique », « digitale toegankelijkheid », « digitale Barrierefreiheit », « digital accessibility ») grâce à l'article pilier et à un maillage dense ;
- présent sur des centaines de requêtes de longue traîne (une question précise, une norme, un secteur, un document, un pays) ;
- générateur de demandes d'audit, de conseil et de formation : chaque article mène vers une prestation.

Rythme : 3 articles par semaine, publiés dans les 4 langues (jamais un article dans une seule langue). Jamais deux fois le même sujet, jamais deux articles qui visent la même requête (pas de cannibalisation).

## 2. Architecture en silos (topic clusters)

Chaque article appartient à un seul silo, indiqué dans le champ `"cluster"` du JSON.

| Silo | `cluster` | Article de tête | Prestations à lier en priorité |
|---|---|---|---|
| Pilier général | `pilier` | `guide` | toutes |
| Réglementation et pays | `reglementation` | `eaa` (Europe), puis `france`, `belgique`, `luxembourg`, `suisse` | `audit-rgaa`, `audit-raam`, `audit-conformite` |
| Normes et critères | `normes` | `normes` | `audit-conformite`, `audit-rgaa`, `formations` |
| Méthode, audit et conformité | `methode` | `declaration` | `audit-rgaa`, `audit-conformite`, `recette`, `test-utilisateur` |
| Contenus et technique | `technique` | `normes` | `developpement`, `formations`, `elearning`, `recette` |
| Secteurs | `secteurs` | `eaa` | `audit-conformite`, `test-utilisateur` ; pages `sector:*` |
| Organisation et achats | `organisation` | `guide` | `formations`, `aide-recrutement`, `prestation-informatique`, `elearning` |

Quand un silo atteint 3 articles ou plus sans article de tête propre (`technique`, `secteurs`, `organisation`), le prochain article de ce silo peut en devenir la tête : c'est noté dans `CALENDAR.md`.

## 3. Maillage interne (bloquant)

Le maillage est ce qui fera la différence face aux sites institutionnels. Il est vérifié par `python3 gen/maillage.py <id>`, qui doit afficher `OK` dans les 4 langues avant toute publication.

Liens sortants du nouvel article (dans le texte, avec des ancres descriptives, jamais « cliquez ici ») :
- l'article pilier `article:guide` ;
- l'article de tête de son silo et au moins 2 autres articles proches (au moins 4 articles au total) ;
- au moins 2 pages prestations (`svc:*`), placées là où le lecteur en a besoin, pas seulement en fin d'article ;
- au moins 1 page pays (`country:*`) ou secteur (`sector:*`) ;
- `related` : 3 articles, les plus proches du sujet.

Liens entrants (à créer dans les articles existants, dans les 4 langues) :
- au moins 3 articles existants doivent pointer vers le nouvel article : l'article de tête du silo, et au moins 2 articles proches ;
- le lien est ajouté par une phrase naturelle, dans la section où il est utile (Edit ciblé du JSON, ou nouveau paragraphe `p` court), sans réécrire l'article ;
- ajoutez ou mettez à jour le champ `"modified": "AAAA-MM-JJ"` (date du jour) dans chaque article modifié ;
- ancres variées : ne reprenez pas trois fois la même ancre vers une même page.

Règles générales :
- un article ne lie jamais vers lui-même ni vers une page inexistante ;
- pas plus d'un lien par paragraphe vers la même page ;
- `python3 gen/maillage.py` (sans argument) donne la vue d'ensemble : tout article signalé « à renforcer » doit recevoir des liens lors des publications suivantes.

## 4. Choisir le sujet

1. Prenez dans `CALENDAR.md` d'abord la première ligne « à faire » de « Mises à jour prioritaires », sinon le premier sujet « à faire » de la file.
2. Vérifiez qu'aucun article existant (`gen/articles/*.fr.json`) ne vise déjà la même requête. Si oui, passez au suivant et notez-le.
3. Si la file compte moins de 10 sujets « à faire », ajoutez-en en fin de file : longue traîne, valeur commerciale, silo indiqué, requête cible FR, sans doublon.

## 5. Analyse de la concurrence (avant d'écrire)

Recherchez la requête cible en français (et l'équivalent dans chaque langue pour les versions traduites). Notez ce que proposent les 5 à 10 premiers résultats : très souvent des pages institutionnelles (textes de loi, définitions). Listez ce qui leur manque : exemples concrets, marche à suivre, check-lists, modèles, tableaux de décision, erreurs fréquentes, cas par secteur ou par pays, impact sur le budget et les délais. L'article est construit sur ces manques :
- la partie juridique est résumée et sourcée (20 % du texte au maximum, sauf article de réglementation) ;
- le H1, le `meta_title` et la `meta_desc` promettent un contenu concret que les pages concurrentes ne donnent pas ;
- jamais de concurrent nommé (autres cabinets, éditeurs d'outils, de widgets ou d'« overlays ») ; ne parlez pas des overlays/widgets d'accessibilité.

## 6. Contenu

- Version française : au moins 4 000 mots utiles ; versions NL, DE, EN : au moins 3 500 mots chacune (voir `TRANSLATION.md`).
- Structure : chapô, 7 à 14 sections h2, au moins un tableau, au moins une liste ou une check-list, 1 ou 2 encadrés `note` (« À retenir »), FAQ de 5 à 8 vraies questions d'internautes.
- Exactitude : chaque fait juridique, date, seuil, montant, numéro de critère est vérifié sur une source officielle le jour même ; 3 à 8 liens externes officiels vérifiés (URL ouverte avec WebFetch). Aucune statistique, étude, citation ou cas client inventé.
- Faits sur le cabinet autorisés, et aucun autre : dédié à l'accessibilité numérique depuis 15 ans ; plus de 400 clients ; 80 consultants ; délai moyen d'un audit : 3 semaines ; membre de l'IAAP et du W3C. Aucun nom de client, aucune personne mise en avant, aucun témoignage. Pas d'allégation « premier » dans les articles.
- Pas de tarif chiffré inventé : pour les sujets de prix, expliquez les facteurs qui font varier un devis et orientez vers la page Contact.
- Date : `"date"` = date de publication (AAAA-MM-JJ).
- `cluster` : obligatoire (voir section 2).

## 7. Veille (à chaque exécution)

Avant de choisir le sujet, vérifiez rapidement (recherche web) si l'un de ces événements a eu lieu depuis la dernière publication ; si oui, ajoutez une ligne dans « Mises à jour prioritaires » de `CALENDAR.md` et traitez-la en priorité :
- publication du RGAA 5 ;
- citation de l'EN 301 549 V4.1.1 au Journal officiel de l'UE ;
- publication du RAWeb 2 / RAAM 2 (Luxembourg) ;
- vote du Conseil des États sur la loi suisse sur l'inclusion ;
- nouveau texte, nouvelle sanction ou décision marquante (Arcom, DGCCRF, BOSA, SIP, OSAPS, tribunaux) dans les quatre pays.
Une mise à jour consiste à corriger les passages concernés dans les 4 langues des articles impactés (et à signaler dans le résumé les pages du site, hors blog, qui deviendraient inexactes), avec `"modified"` à la date du jour.

## 8. Procédure technique

Prérequis : `pip install --break-system-packages jinja2 markupsafe` et `npm install --no-save axe-core` (Playwright est préinstallé).

1. Écrire `gen/articles/<id>.fr.json` (`<id>` court, en minuscules, tirets, sans accent, unique), contrôler avec `python3 gen/check_article.py gen/articles/<id>.fr.json 4000`.
2. Faire vérifier les faits de la version française par un relecteur indépendant (sous-agent qui n'a pas écrit l'article), corriger.
3. Produire `<id>.nl.json`, `<id>.de.json`, `<id>.en.json` selon `TRANSLATION.md` (sous-agents en parallèle possibles), contrôler chacun avec `check_article.py … 3500`.
4. Créer les liens entrants (section 3) dans les articles existants, puis `python3 gen/maillage.py <id>` → `OK`.
5. `python3 gen/build.py prod && python3 gen/check_site.py` → 0 erreur.
6. `FORM_ENDPOINT= python3 gen/build.py preview && node tools/axe.cjs <chemins preview des 4 pages du nouvel article et des articles modifiés>` → `{}`.
7. Mettre à jour `CALENDAR.md` (sujet déplacé dans « Publiés » avec date, id, silo).
8. `git add -A && git commit` (message en français) puis `git push origin main`. Cloudflare déploie automatiquement en une minute environ. Ne jamais pousser si un contrôle échoue.
