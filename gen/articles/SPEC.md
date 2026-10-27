# Cahier des charges des articles — accessibilitenumerique.eu

## Le site et le cabinet
- Site institutionnel du cabinet « Accessibilité numérique » : audit et conseil en accessibilité numérique pour le secteur public, les grands comptes et les PME, en France, en Belgique, au Luxembourg et en Suisse, avec une dimension européenne. Ambiance : cabinet de conseil sérieux, sobre, précis.
- Objectif SEO déclaré : être premier sur « accessibilité numérique » (et ses équivalents NL « digitale toegankelijkheid », DE « digitale Barrierefreiheit », EN « digital accessibility ») en France, Belgique, Luxembourg et Suisse. Chaque article doit être LA meilleure page du web sur son sujet : plus concrète, plus à jour et plus utile que les pages institutionnelles qui dominent aujourd'hui.
- Faits sur le cabinet que vous pouvez utiliser (et aucun autre) : dédié à l'accessibilité numérique depuis 15 ans ; plus de 400 clients ; 80 consultants ; délai moyen d'un audit : 3 semaines ; membre de l'IAAP et du W3C ; site lui-même déclaré totalement conforme au RGAA 4.1.2. Ne citez AUCUN nom de client, AUCUNE personne, aucune étude de cas, aucun témoignage, aucune statistique « interne ». Ne mettez personne en avant. Parlez du cabinet avec retenue (« nous » est possible, mais l'article informe avant de vendre : pas plus de 2 ou 3 mentions du cabinet hors bloc CTA).

## Exactitude (non négociable)
- Le droit et les normes ont évolué : nous sommes le 27 octobre 2026. Vérifiez chaque fait réglementaire ou normatif avec WebSearch / WebFetch auprès de sources officielles avant de l'écrire : textes de loi, dates, montants de sanctions, autorités de contrôle, versions de normes (RGAA, RAWeb, RAAM, WCAG, EN 301 549, eCH-0059), seuils d'exemption, calendrier.
- Sources à privilégier : legifrance.gouv.fr, accessibilite.numerique.gouv.fr, numerique.gouv.fr, arcom.fr, defenseurdesdroits.fr, economie.gouv.fr / DGCCRF, eur-lex.europa.eu, commission.europa.eu, w3.org/WAI, etsi.org, ejustice.just.fgov.be, bosa.belgium.be, legilux.public.lu, accessibilite.public.lu, sip.gouvernement.lu, fedlex.admin.ch, ech.ch, edi.admin.ch (BFEH), accessibility-developer-guide.com, etc.
- Aucun chiffre sans source vérifiée et liée. Si vous n'arrivez pas à vérifier un point, ne l'écrivez pas (ou formulez-le prudemment sans chiffre). N'inventez jamais un numéro d'article de loi, un montant, une date.
- Mettez 3 à 8 liens externes vers ces sources officielles, intégrés au texte avec la syntaxe `[[https://url-exacte|libellé descriptif]]`. Vérifiez que chaque URL existe (WebFetch) : pas d'URL inventée.
- Restez cohérent avec les pages pays du site (lisez la partie `COUNTRY` et `STANDARDS` de /home/claude/an-site/gen/content_fr.py). Si vous constatez qu'une page du site contient une erreur ou une information dépassée, NE la contredisez pas en silence : écrivez juste dans l'article ce qui est exact, et signalez l'écart dans votre compte rendu final.

## Style
- Français impeccable, vouvoiement, registre institutionnel mais limpide : un directeur juridique, un DSI ou un élu doit comprendre sans être spécialiste. Phrases nettes, paragraphes de 2 à 5 phrases.
- Concret avant tout : exemples réels de situations (un formulaire de paiement, un PDF de délibération, un captcha, un menu déroulant, un lecteur d'écran sur mobile), étapes, ordres de grandeur sourcés, pièges fréquents.
- À proscrire (marqueurs de texte « généré ») : « Dans un monde où », « À l'ère du numérique », « Plongeons », « Il est crucial de », « En conclusion », « Que vous soyez… ou… », « véritable », « incontournable », « levier », « booster », les questions rhétoriques en série, les listes de trois adjectifs, le gras décoratif, les emojis, les tirets cadratins en rafale. Pas de conclusion qui résume l'article : terminez sur une section utile (plan d'action, calendrier, checklist).
- Typographie : guillemets « » avec espaces insécables (U+00A0) à l'intérieur ; écrivez un espace normal avant ? ! : ; (le générateur les rend insécables) ; « % » précédé d'une espace insécable ; nombres avec espace insécable comme séparateur de milliers ; dates « 28 juin 2025 ».

## SEO
- Le titre (h1) doit être différenciant : il promet quelque chose de précis que les pages concurrentes ne promettent pas, contient le mot-clé principal de l'article, fait moins de 90 caractères. Pas de « Tout savoir sur », « Le guide ultime ».
- `meta_title` : 65 caractères maximum, mot-clé principal au début, distinct du h1 si utile, sans le nom du site.
- `meta_desc` : 120 à 165 caractères, bénéfice concret + mot-clé.
- Mot-clé principal dans le h1, le `lead`, au moins deux intertitres h2 et naturellement dans le texte (densité naturelle, aucun bourrage). Couvrez les variantes et questions que les gens tapent réellement (« accessibilité numérique obligation », « RGAA c'est quoi », « audit accessibilité prix », etc.) via les h2/h3 et la FAQ.
- Maillage interne : au moins 6 liens internes avec la syntaxe `[[cle|libellé]]`. Clés valides :
  - prestations : `svc:audit-rgaa`, `svc:audit-raam`, `svc:audit-conformite`, `svc:recette`, `svc:test-utilisateur`, `svc:developpement`, `svc:prestation-informatique`, `svc:aide-recrutement`, `svc:elearning`, `svc:formations`
  - pays : `country:france`, `country:belgique`, `country:luxembourg`, `country:suisse` ; pages `standards`, `services`, `contact`, `firm`
  - secteurs : `sector:public`, `sector:grands-comptes`, `sector:pme`
  - autres articles : `article:guide`, `article:eaa`, `article:france`, `article:declaration`, `article:belgique`, `article:luxembourg`, `article:suisse`, `article:normes`
- Les liens ne fonctionnent que dans les paragraphes, items de listes, notes, cellules de tableau, le lead et les réponses de FAQ (pas dans les titres).

## Format du fichier (JSON UTF-8)
Écrivez le fichier avec l'outil Write à l'emplacement indiqué, JSON valide (guillemets doubles, échappez les guillemets internes), indentation libre.

```json
{
  "slug": "accessibilite-numerique-belgique",
  "h1": "Titre affiché de l'article",
  "crumb": "Libellé court pour le fil d'Ariane (3 à 5 mots)",
  "meta_title": "≤ 65 caractères",
  "meta_desc": "120 à 165 caractères",
  "card_desc": "Résumé d'une phrase (≤ 140 caractères) affiché sur la carte de l'article",
  "cat": "guide | analyse | reglementation",
  "where": "France | Belgique | Luxembourg | Suisse | Europe",
  "cover": "≤ 5 caractères affichés en très grand sur la couverture (ex. BE, RGAA, EAA)",
  "cover_note": ["Ligne 1 de la couverture (ex. référence d'un texte)", "Ligne 2 (ex. date clé)"],
  "date": "2026-10-27",
  "lead": "Chapô de 2 à 4 phrases, contient le mot-clé principal.",
  "body": [
    ["h2", "identifiant-de-section", "Intertitre de section"],
    ["p", "Paragraphe, avec éventuellement un [[svc:audit-rgaa|lien interne]] ou une [[https://www.legifrance.gouv.fr/...|source officielle]]."],
    ["h3", "Sous-intertitre"],
    ["ul", ["élément de liste ;", "autre élément."]],
    ["ol", [["Étape en gras", "suite de l'étape en texte normal."], ["Deuxième étape", "explication."]]],
    ["note", "À retenir", "Phrase clé mise en exergue."],
    ["table", {"caption": "Titre du tableau", "head": ["Colonne 1", "Colonne 2", "Colonne 3"], "rows": [["Ligne", "valeur", "valeur"]]}]
  ],
  "faq": [["Question telle qu'un internaute la tape ?", "Réponse autonome de 40 à 90 mots."]],
  "cta_svc": "audit-rgaa",
  "cta_title": "Question d'accroche du bloc final (≤ 60 caractères)",
  "cta_text": "Une ou deux phrases qui proposent l'étape suivante, sans pression.",
  "related": ["eaa", "france", "normes"]
}
```

Contraintes de structure : 7 à 14 sections h2 (identifiants uniques, minuscules, tirets, jamais « faq ») ; au moins un tableau ; au moins une liste ; 1 ou 2 notes ; FAQ de 5 à 8 questions (n'en faites pas un doublon du corps) ; 2 ou 3 articles `related`.

## Longueur et contrôle
- Version française : **au moins 4 000 mots** (lead + corps + FAQ). Versions traduites : **au moins 3 500 mots**.
- Vérifiez avant de rendre la main : `python3 /home/claude/an-site/gen/check_article.py /home/claude/an-site/gen/articles/<id>.<lang>.json 4000` (ou `3500` pour une traduction). Corrigez jusqu'à obtenir `OK`.
- Ne lancez PAS le build du site, ne modifiez aucun autre fichier que le vôtre.
