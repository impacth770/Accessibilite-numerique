# Consignes de traduction et de localisation des articles

Vous produisez la version néerlandaise, allemande ou anglaise d'un article français déjà validé. Lisez d'abord SPEC.md (même dossier) : format JSON, règles d'exactitude, maillage, contrôle. Tout s'applique, sauf la longueur : **au moins 3 500 mots** pour une traduction.

## Principe
- Ce n'est pas une traduction mot à mot : c'est la même page, écrite nativement pour le lecteur visé, avec exactement les mêmes faits, la même structure de sections, les mêmes tableaux, la même FAQ et les mêmes liens internes (mêmes clés `[[cle|…]]`, libellés traduits).
- N'ajoutez aucun fait nouveau non vérifié et ne retirez aucun fait. Si la version obtenue fait moins de 3 500 mots, développez les explications et les exemples pratiques déjà présents, ou ajoutez une courte section utile au lecteur de votre langue (par exemple, pour le néerlandais, la situation des organisations flamandes et bruxelloises ; pour l'allemand, le lecteur luxembourgeois, suisse alémanique ou de la Communauté germanophone de Belgique), en vérifiant chaque fait nouveau comme exigé par SPEC.md.
- Liens externes : gardez les mêmes sources. Si la source officielle existe dans votre langue (EUR-Lex, sites de la Commission européenne, W3C/WAI, Fedlex, BOSA, Vlaanderen.be, etc.), remplacez l'URL par la version dans votre langue, après avoir vérifié qu'elle existe. Les textes français (Légifrance…) restent en français, avec un libellé traduit.
- Titres et intertitres : adaptez-les à la façon dont les gens cherchent dans votre langue. Gardez la promesse différenciante du titre français.
- Identifiants de sections h2 : traduisez-les en minuscules avec tirets dans votre langue (uniques, jamais « faq »).

## Champs propres à chaque langue
- `slug` : dans votre langue, minuscules, tirets, sans accents (ä → ae, ö → oe, ü → ue, ß → ss pour l'allemand), contient le mot-clé principal. Exception : l'article `eaa` garde le slug `european-accessibility-act` dans toutes les langues.
- `where` : traduit (Europe, Frankrijk / Frankreich / France, België / Belgien / Belgium, Luxemburg / Luxemburg / Luxembourg, Zwitserland / Schweiz / Switzerland).
- `cover` : identique au français, sauf si c'est un mot français (traduisez alors en 5 caractères au plus).
- `cover_note`, `crumb`, `meta_title` (≤ 65 caractères), `meta_desc` (120 à 165 caractères), `card_desc`, `cta_title`, `cta_text` : rédigés dans votre langue.
- `cat`, `date`, `cta_svc`, `related` : identiques au français.

## Langues
- **Néerlandais (nl)** : lectorat belge (Flandre, Bruxelles). Néerlandais standard avec les usages belges : « u », « kmo », « overheid », « FOD », « gemeente ». Mot-clé principal : « digitale toegankelijkheid » (variantes : « webtoegankelijkheid », « toegankelijke website »). Écrivez les espaces normalement (pas d'espace avant ? ! : ;).
- **Allemand (de)** : lectorat luxembourgeois, suisse et de la Communauté germanophone de Belgique. Allemand standard avec « ß » (comme le reste du site). Mot-clé principal : « digitale Barrierefreiheit » (variantes : « barrierefreie Website », « Barrierefreiheit im Internet », « Web-Barrierefreiheit »). Guillemets „…“ ou «…» : utilisez „…“.
- **Anglais (en)** : lectorat international (grands comptes, Luxembourg, Belgique, Suisse). Anglais britannique (organisation, programme), comme le reste du site. Mot-clé principal : « digital accessibility » (variantes : « web accessibility », « accessibility compliance »). Guillemets “…”.

## Contrôle
`python3 /home/claude/an-site/gen/check_article.py /home/claude/an-site/gen/articles/<id>.<lang>.json 3500` doit afficher OK. N'écrivez que votre fichier.
