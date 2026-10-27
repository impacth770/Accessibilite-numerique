"""Vérifie un fichier d'article : python3 gen/check_article.py gen/articles/<id>.<lang>.json [min_mots]
Contrôle le schéma, les clés de liens internes, les identifiants de sections et compte les mots."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SVC, COUNTRIES, SECTORS, LEGAL, ARTICLES

f = sys.argv[1]; minw = int(sys.argv[2]) if len(sys.argv) > 2 else 3500
a = json.load(open(f, encoding='utf-8'))
err = []
REQ = ['slug', 'h1', 'crumb', 'meta_title', 'meta_desc', 'card_desc', 'cat', 'where', 'cover', 'cover_note', 'date', 'lead', 'body', 'faq', 'cta_svc', 'cta_title', 'cta_text', 'related']
for k in REQ:
    if k not in a: err.append('champ manquant : ' + k)
if a.get('cat') not in ('guide', 'analyse', 'reglementation'): err.append('cat invalide')
if a.get('cta_svc') not in SVC: err.append('cta_svc invalide : %s' % a.get('cta_svc'))
if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a.get('slug', '')): err.append('slug invalide')
if len(a.get('meta_title', '')) > 65: err.append('meta_title trop long (%d > 65)' % len(a['meta_title']))
if not 120 <= len(a.get('meta_desc', '')) <= 165: err.append('meta_desc hors 120-165 caractères (%d)' % len(a.get('meta_desc', '')))
if len(a.get('cover', '')) > 5: err.append('cover > 5 caractères')
for r in a.get('related', []):
    if r not in ARTICLES: err.append('related inconnu : ' + r)
valid = set(['home', 'services', 'standards', 'firm', 'resources', 'contact'] + ['svc:' + s for s in SVC] + ['country:' + c for c in COUNTRIES]
            + ['sector:' + s for s in SECTORS] + ['legal:' + l for l in LEGAL] + ['article:' + x for x in ARTICLES])
texts = [a.get('lead', '')]
ids = set(); h2 = 0; kinds = set()
for i, b in enumerate(a.get('body', [])):
    t = b[0]; kinds.add(t)
    if t == 'h2':
        h2 += 1
        if len(b) != 3 or not re.fullmatch(r'[a-z0-9-]+', b[1]) or b[1] in ids or b[1] == 'faq': err.append('h2 #%d invalide ou id en double' % i)
        ids.add(b[1]); texts.append(b[2])
    elif t in ('p', 'h3'):
        if len(b) != 2 or not isinstance(b[1], str): err.append('%s #%d invalide' % (t, i))
        else: texts.append(b[1])
    elif t == 'ul':
        if len(b) != 2 or not all(isinstance(x, str) for x in b[1]): err.append('ul #%d invalide' % i)
        else: texts += b[1]
    elif t == 'ol':
        if len(b) != 2 or not all(isinstance(x, list) and len(x) == 2 for x in b[1]): err.append('ol #%d invalide' % i)
        else: texts += [x[0] + ' ' + x[1] for x in b[1]]
    elif t == 'note':
        if len(b) != 3: err.append('note #%d invalide' % i)
        else: texts += [b[1], b[2]]
    elif t == 'table':
        tb = b[1] if len(b) == 2 else {}
        if not tb.get('caption') or not tb.get('head') or not tb.get('rows') or any(len(r) != len(tb['head']) for r in tb['rows']): err.append('table #%d invalide' % i)
        else: texts += tb['head'] + [c for r in tb['rows'] for c in r]
    else:
        err.append('type de bloc inconnu #%d : %s' % (i, t))
for q in a.get('faq', []):
    if len(q) != 2: err.append('faq invalide')
    else: texts += q
full = ' '.join(texts)
for mt in re.finditer(r'\[\[([^|\]]+)\|([^\]]+)\]\]', full):
    k = mt.group(1).strip()
    if not k.startswith('http') and k not in valid: err.append('lien interne inconnu : ' + k)
if re.search(r'\[\[(?![^\]]*\|)', full) or full.count('[[') != full.count(']]'): err.append('syntaxe de lien [[...]] cassée')
n = len(re.sub(r'\[\[[^|\]]+\|([^\]]+)\]\]', r'\1', full).split())
internal = len([1 for mt in re.finditer(r'\[\[([^|\]]+)\|', full) if not mt.group(1).startswith('http')])
external = len([1 for mt in re.finditer(r'\[\[(https?://[^|\]]+)\|', full)])
if h2 < 7: err.append('moins de 7 sections h2 (%d)' % h2)
if 'table' not in kinds: err.append('aucun tableau')
if not 5 <= len(a.get('faq', [])) <= 8: err.append('FAQ : 5 à 8 questions attendues')
if internal < 5: err.append('moins de 5 liens internes (%d)' % internal)
if external < 3: err.append('moins de 3 liens externes vers des sources (%d)' % external)
if n < minw: err.append('trop court : %d mots < %d' % (n, minw))
print('%s : %d mots, %d h2, %d liens internes, %d liens externes, %d FAQ' % (os.path.basename(f), n, h2, internal, external, len(a.get('faq', []))))
print('OK' if not err else 'ERREURS :\n- ' + '\n- '.join(err))
sys.exit(1 if err else 0)
