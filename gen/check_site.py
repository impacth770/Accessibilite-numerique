"""Contrôle du site généré (dist/) : liens internes cassés, ancres absentes, identifiants en double.
Usage : python3 gen/build.py prod && python3 gen/check_site.py   (code de sortie 1 en cas d'erreur)"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
errors, pages = [], 0
for r, d, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(r, f); s = open(p, encoding='utf-8').read(); pages += 1
        rel = os.path.relpath(p, ROOT)
        for h in re.findall(r'href="(/[^"#?]*)', s):
            t = ROOT + h
            if not (os.path.isfile(t) or os.path.isfile(os.path.join(t, 'index.html'))):
                errors.append('%s : lien cassé %s' % (rel, h))
        for h in re.findall(r'href="#([^"]+)"', s):
            if ' id="%s"' % h not in s:
                errors.append('%s : ancre absente #%s' % (rel, h))
        ids = re.findall(r' id="([^"]+)"', s)
        dup = sorted(set(i for i in ids if ids.count(i) > 1))
        if dup:
            errors.append('%s : identifiants en double %s' % (rel, dup))
print('%d pages contrôlées, %d erreur(s)' % (pages, len(errors)))
for e in errors[:50]:
    print(' -', e)
sys.exit(1 if errors else 0)
