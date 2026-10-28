"""Rapport de maillage interne des articles (par langue).
Usage : python3 gen/maillage.py            -> rapport complet
        python3 gen/maillage.py <id>       -> contrôle bloquant pour un article (code 1 si règle non respectée)
Règles contrôlées pour l'article <id>, dans chaque langue :
  - au moins 3 liens entrants contextuels depuis d'autres articles (hors bloc « À lire aussi ») ;
  - au moins 4 liens sortants vers d'autres articles, dont l'article pilier ;
  - au moins 2 liens vers des pages prestations (svc:) et 1 vers une page pays ou secteur ;
  - aucun lien vers un article inexistant."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ART, ARTICLES, LANGS, PILLAR

LINK = re.compile(r'\[\[([^|\]]+)\|')

def texts(a):
    t = [a.get('lead', '')]
    for b in a['body']:
        if b[0] in ('p', 'h3'): t.append(b[1])
        elif b[0] == 'ul': t += b[1]
        elif b[0] == 'ol': t += [x[1] for x in b[1]]
        elif b[0] == 'note': t.append(b[2])
        elif b[0] == 'table': t += [c for r in b[1]['rows'] for c in r]
    t += [q[1] for q in a.get('faq', [])]
    return ' '.join(t)

def graph(lang):
    out, inb = {}, {a: set() for a in ARTICLES if a in ART[lang]}
    for a in inb:
        keys = LINK.findall(texts(ART[lang][a]))
        out[a] = keys
        for k in keys:
            if k.startswith('article:') and k[8:] in inb and k[8:] != a:
                inb[k[8:]].add(a)
    return out, inb

def check(aid):
    errs = []
    for l in LANGS:
        if aid not in ART[l]:
            errs.append('%s : version absente' % l); continue
        out, inb = graph(l)
        keys = out[aid]
        arts = set(k[8:] for k in keys if k.startswith('article:'))
        missing = [k for k in arts if k not in ART[l]]
        if missing: errs.append('%s : liens vers des articles inexistants %s' % (l, missing))
        if len(inb[aid]) < 3: errs.append('%s : %d lien(s) entrant(s) contextuel(s) seulement (minimum 3) : %s' % (l, len(inb[aid]), sorted(inb[aid])))
        if len(arts - {aid}) < 4: errs.append('%s : %d article(s) lié(s) seulement (minimum 4)' % (l, len(arts - {aid})))
        if aid != PILLAR and PILLAR not in arts: errs.append('%s : pas de lien vers l\'article pilier (%s)' % (l, PILLAR))
        if len(set(k for k in keys if k.startswith('svc:'))) < 2: errs.append('%s : moins de 2 pages prestations liées' % l)
        if not any(k.startswith(('country:', 'sector:')) for k in keys): errs.append('%s : aucune page pays ou secteur liée' % l)
    return errs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        e = check(sys.argv[1])
        print('OK' if not e else 'ERREURS :\n- ' + '\n- '.join(e))
        sys.exit(1 if e else 0)
    for l in LANGS:
        out, inb = graph(l)
        print('== %s' % l)
        for a in ARTICLES:
            if a not in ART[l]: continue
            arts = set(k[8:] for k in out[a] if k.startswith('article:')) - {a}
            flag = '  <-- à renforcer' if len(inb[a]) < 3 else ''
            print('  %-14s entrants %2d · sortants %2d articles, %2d prestations%s' % (a, len(inb[a]), len(arts), len(set(k for k in out[a] if k.startswith('svc:'))), flag))
