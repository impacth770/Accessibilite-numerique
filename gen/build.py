import os, sys, json, shutil, posixpath, importlib, re
from markupsafe import Markup, escape
from jinja2 import Environment, FileSystemLoader
sys.path.insert(0, os.path.dirname(__file__))
from common import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'prod'
OUT = os.path.join(ROOT, 'dist' if MODE == 'prod' else 'preview')
FORM_ENDPOINT = os.environ.get('FORM_ENDPOINT', 'https://hook.eu1.make.com/yzzl9yt5enats8we3umgcgw1x0g53rt6')
LOGOS = [('Canal+', 'canalplus.webp', 26), ('Porsche', 'porsche.webp', 15), ('ING', 'ing.webp', 30),
         ('OVHcloud', 'ovhcloud.webp', 40), ('Manutan', 'manutan.webp', 34), ('Lotus Bakeries', 'lotus.webp', 50)]

env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')), autoescape=True, trim_blocks=False)

def rich(text, u):
    """[[cle|libellé]] -> lien interne."""
    out, pos = [], 0
    for mt in re.finditer(r'\[\[([^|\]]+)\|([^\]]+)\]\]', text):
        out.append(escape(text[pos:mt.start()]))
        k = mt.group(1).strip()
        if k.startswith('http'):
            out.append(Markup('<a href="%s" rel="noopener">%s</a>') % (k, mt.group(2)))
        else:
            out.append(Markup('<a href="%s">%s</a>') % (u(k), mt.group(2)))
        pos = mt.end()
    out.append(escape(text[pos:]))
    return Markup('').join(out)
env.filters['rich'] = rich

C = {l: importlib.import_module('content_' + l) for l in LANGS}

MONTHS = {'fr': ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          'nl': ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'],
          'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']}

def fmt_date(lang, iso):
    y, mo, d = (int(x) for x in iso.split('-'))
    if lang == 'en': return '%d %s %d' % (d, MONTHS[lang][mo - 1], y)
    if lang == 'de': return '%d. %s %d' % (d, MONTHS[lang][mo - 1], y)
    return '%d %s %d' % (d, MONTHS[lang][mo - 1], y)

def words(a):
    t = [a.get('lead', '')]
    for b in a['body']:
        if b[0] in ('p', 'h3'): t.append(b[1])
        elif b[0] == 'h2': t.append(b[2])
        elif b[0] == 'ul': t += b[1]
        elif b[0] == 'ol': t += [x[0] + ' ' + x[1] for x in b[1]]
        elif b[0] == 'note': t += [b[1], b[2]]
        elif b[0] == 'table': t += b[1].get('head', []) + [c for r in b[1]['rows'] for c in r]
    t += [q + ' ' + r for q, r in a.get('faq', [])]
    return len(re.sub(r'\[\[[^|\]]+\|([^\]]+)\]\]', r'\1', ' '.join(t)).split())

def posts(lang):
    m = C[lang]; au = m.ARTICLE_UI
    return [{'key': 'article:' + a, 'id': a, 'live': True, 'catkey': ART[lang][a]['cat'], 'cat': au['cats'][ART[lang][a]['cat']],
             'where': ART[lang][a]['where'], 'cover': ART[lang][a]['cover'], 'cls': ['', 'c1', 'c2'][i % 3],
             'title': ART[lang][a]['h1'], 'desc': ART[lang][a]['card_desc']} for i, a in enumerate(ART_LIVE)]

def href(lang, key, cur_path):
    target = path(lang, key)
    if MODE == 'prod':
        return '/' + target
    rel = posixpath.relpath(target + 'index.html', cur_path or '.')
    return rel

def asset_url(name, cur_path):
    if MODE == 'prod':
        return '/assets/' + name
    return posixpath.relpath('assets/' + name, cur_path or '.')

def ld(o):
    return Markup(json.dumps(o, ensure_ascii=False).replace('</', '<\\/'))

def org(lang):
    return {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": DOMAIN + "/#org",
            "name": "Accessibilité numérique", "legalName": "MABEL AGENCY", "telephone": "+33465849826", "url": DOMAIN + "/", "numberOfEmployees": {"@type": "QuantitativeValue", "value": 80}, "taxID": "FR19904260742", "address": {"@type": "PostalAddress", "streetAddress": "25 rue Jules Isaac", "postalCode": "13009", "addressLocality": "Marseille", "addressCountry": "FR"}, "email": "contact@accessibilitenumerique.eu",
            "description": C[lang].META['home'][1],
            "areaServed": [{"@type": "Country", "name": n} for n in ["France", "Belgium", "Luxembourg", "Switzerland"]],
            "availableLanguage": ["fr", "nl", "de", "en"],
            "memberOf": [{"@type": "Organization", "name": "International Association of Accessibility Professionals"},
                         {"@type": "Organization", "name": "World Wide Web Consortium"}],
            "knowsAbout": ["RGAA", "WCAG", "EN 301 549", "European Accessibility Act", "RAWeb", "RAAM", "eCH-0059"]}

def crumbs_ld(lang, trail):
    items = [{"@type": "ListItem", "position": 1, "name": C[lang].UI['home'], "item": DOMAIN + '/' + path(lang, 'home')}]
    for i, (k, n) in enumerate(trail):
        it = {"@type": "ListItem", "position": i + 2, "name": n}
        if k: it["item"] = DOMAIN + '/' + path(lang, k)
        items.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def plan_sections(lang):
    m = C[lang]; ui = m.UI
    sec = [('pages', ui['sm_main'], [], [(k, m.META[k][0].split(' — ')[0] if k != 'home' else ui['home']) for k in ['home', 'services', 'standards', 'firm', 'resources', 'contact']]),
           ('services', ui['services'], [], [('svc:' + s, ui['svc'][s]) for s in SVC]),
           ('standards', ui['standards'], [], [('country:' + c, ui['country'][c]) for c in COUNTRIES]),
           ('sectors', ui['f_sectors'], [], [('sector:' + s, ui['sector'][s]) for s in SECTORS]),
           ('resources', ui['resources'], [], [('article:' + a, ART[lang][a]['h1']) for a in ART_LIVE]),
           ('infos', ui['sm_info'], [], [('legal:' + l, ui['legal'][l]) for l in ['mentions', 'confidentialite', 'accessibilite']])]
    return sec

def render(lang, key):
    m = C[lang]; ui = m.UI
    cur = path(lang, key)
    u = lambda k: href(lang, k, cur)
    ctx = dict(lang=lang, ui=ui, u=u, asset=lambda n: asset_url(n, cur), svc_groups=SVC_GROUPS, svc_all=SVC,
               countries=COUNTRIES, sectors=SECTORS, codes=CODES, svc=m.SVC, country=m.COUNTRY, logos=LOGOS,
               posts=posts(lang), form_endpoint=FORM_ENDPOINT, fr_contact=C['fr'].CONTACT, country_fr=COUNTRY_FR, section=None, page_type='page')
    jsonld = [org(lang)]
    trail = []
    if key == 'home':
        tpl, c = 'home.html', m.HOME
    elif key == 'services':
        tpl, c, ctx['section'] = 'services.html', m.SERVICES_HUB, 'services'; trail = [(None, ui['services'])]
    elif key.startswith('svc:'):
        sid = key[4:]; tpl, c = 'service.html', m.SVC[sid]; ctx.update(sid=sid, section='services')
        trail = [('services', ui['services']), (None, ui['svc'][sid])]
        jsonld.append(faq_ld(c['faq']))
        jsonld.append({"@context": "https://schema.org", "@type": "Service", "name": ui['svc'][sid], "description": c['intro'],
                       "provider": {"@id": DOMAIN + "/#org"}, "areaServed": ["FR", "BE", "LU", "CH"], "url": DOMAIN + '/' + cur})
    elif key == 'standards':
        tpl, c, ctx['section'] = 'standards.html', m.STANDARDS, 'standards'; trail = [(None, ui['standards'])]
    elif key.startswith('country:'):
        cid = key[8:]; tpl, c = 'country.html', m.COUNTRY[cid]; ctx.update(cid=cid, section='standards')
        trail = [('standards', ui['standards']), (None, ui['country'][cid])]; jsonld.append(faq_ld(c['faq']))
    elif key.startswith('sector:'):
        sid = key[7:]; tpl, c = 'sector.html', m.SECTOR[sid]; ctx.update(sid=sid)
        trail = [(None, ui['f_sectors']), (None, ui['sector'][sid])]
    elif key == 'firm':
        tpl, c, ctx['section'] = 'firm.html', m.FIRM, 'firm'; trail = [(None, ui['firm'])]
    elif key == 'resources':
        tpl, c, ctx['section'] = 'resources.html', m.RESOURCES, 'resources'; trail = [(None, ui['resources'])]
    elif key.startswith('article:'):
        aid = key[8:]; c = dict(ART[lang][aid]); au = m.ARTICLE_UI
        tpl, ctx['section'], ctx['page_type'] = 'article.html', 'resources', 'article'
        n = words(c)
        c['date_txt'] = au['published'] + ' ' + fmt_date(lang, c['date'])
        c['read_txt'] = au['read'] % max(1, round(n / 230))
        c['cat_txt'] = au['cats'][c['cat']] + ' · ' + c['where']
        rel = [a for a in c.get('related', []) if a in ART_LIVE] or [a for a in ART_LIVE if a != aid]
        ctx.update(au=au, related=[p for p in posts(lang) if p['id'] in rel[:3]])
        trail = [('resources', ui['resources']), (None, c['crumb'])]
        jsonld.append({"@context": "https://schema.org", "@type": "Article", "headline": c['h1'], "description": c['meta_desc'],
                       "inLanguage": lang, "datePublished": c['date'], "dateModified": c.get('modified', c['date']), "wordCount": n,
                       "author": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"}, "mainEntityOfPage": DOMAIN + '/' + cur})
        if c.get('faq'): jsonld.append(faq_ld(c['faq']))
    elif key == 'contact':
        tpl, c = 'contact.html', m.CONTACT; trail = [(None, ui['contact'])]
    elif key.startswith('legal:'):
        lid = key[6:]; tpl = 'legal.html'
        c = dict(m.LEGAL[lid])
        if lid == 'plan':
            c['sections'] = plan_sections(lang) + [('langs', ui['sm_langs'], [], [('home', ui['langs'][l], href(l, 'home', cur), l) for l in LANGS if l != lang])]
        trail = [(None, c['title'])]
    elif key == '404':
        tpl, c = '404.html', m.NOTFOUND
    if trail: jsonld.append(crumbs_ld(lang, trail))
    if key.startswith('article:'):
        title, desc = c['meta_title'], c['meta_desc']
    else:
        title, desc = m.META.get(key, (None, None)) if key != '404' else (m.NOTFOUND['title'], m.NOTFOUND['text'])
    ctx.update(c=c, meta={'title': title, 'desc': desc}, jsonld=[ld(j) for j in jsonld],
               canonical=DOMAIN + '/' + cur,
               alternates=[{'lang': l, 'href': DOMAIN + '/' + path(l, key)} for l in LANGS] if key != '404' else [],
               xdefault=DOMAIN + '/' + path('fr', key if key != '404' else 'home'),
               switch=[{'lang': l, 'name': ui['langs'][l], 'href': href(l, key if key != '404' else 'home', cur)} for l in LANGS])
    html = env.get_template(tpl).render(**ctx)
    html = html.replace('EN 301 549', 'EN\u00a0301\u00a0549')
    if lang == 'fr':
        for a, b in ((' ?', '\u202f?'), (' !', '\u202f!'), (' :', '\u202f:'), (' ;', '\u202f;')):
            html = html.replace(a, b)
    out = os.path.join(OUT, cur, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    return cur

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, 'static'), os.path.join(OUT, 'assets'))
    pages = []
    for l in LANGS:
        for k in keys():
            pages.append((l, k, render(l, k)))
        render(l, '404')
    if MODE == 'prod':
        shutil.copy(os.path.join(OUT, '404', 'index.html'), os.path.join(OUT, '404.html'))
        # sitemaps
        idx = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for l in LANGS:
            rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
            for k in keys():
                rows.append('<url><loc>%s/%s</loc>' % (DOMAIN, path(l, k)) + ''.join(
                    '<xhtml:link rel="alternate" hreflang="%s" href="%s/%s"/>' % (a, DOMAIN, path(a, k)) for a in LANGS) +
                    '<xhtml:link rel="alternate" hreflang="x-default" href="%s/%s"/></url>' % (DOMAIN, path('fr', k)))
            rows.append('</urlset>')
            open(os.path.join(OUT, 'sitemap-%s.xml' % l), 'w').write('\n'.join(rows))
            idx.append('<sitemap><loc>%s/sitemap-%s.xml</loc></sitemap>' % (DOMAIN, l))
        idx.append('</sitemapindex>')
        open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(idx))
        open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % DOMAIN)
        open(os.path.join(OUT, '_headers'), 'w').write(
            '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n/assets/*\n  Cache-Control: public, max-age=86400\n')
    print(MODE, len(pages), 'pages ->', OUT)

if __name__ == '__main__':
    main()
