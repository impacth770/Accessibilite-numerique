import json as _json, os as _os

LANGS = ['fr', 'nl', 'de', 'en']
DOMAIN = 'https://accessibilitenumerique.eu'
SVC = ['audit-rgaa', 'audit-raam', 'audit-conformite', 'recette', 'test-utilisateur',
       'developpement', 'prestation-informatique', 'aide-recrutement', 'elearning', 'formations']
SVC_GROUPS = [SVC[0:5], SVC[5:8], SVC[8:10]]
COUNTRIES = ['france', 'belgique', 'luxembourg', 'suisse']
SECTORS = ['public', 'grands-comptes', 'pme']
LEGAL = ['mentions', 'confidentialite', 'accessibilite', 'plan']
CODES = {'france': 'FR', 'belgique': 'BE', 'luxembourg': 'LU', 'suisse': 'CH'}

SLUGS = {
    'fr': {'services': 'prestations', 'standards': 'referentiels', 'sectors': 'secteurs', 'firm': 'cabinet', 'resources': 'ressources', 'contact': 'contact',
           'svc': {'audit-rgaa': 'audit-rgaa', 'audit-raam': 'audit-raam', 'audit-conformite': 'audit-de-conformite', 'recette': 'recette-accessibilite', 'test-utilisateur': 'test-utilisateur-reel', 'developpement': 'developpement-accessible', 'prestation-informatique': 'prestation-informatique', 'aide-recrutement': 'aide-au-recrutement', 'elearning': 'e-learning-accessibilite', 'formations': 'formations'},
           'country': {'france': 'france', 'belgique': 'belgique', 'luxembourg': 'luxembourg', 'suisse': 'suisse'},
           'sector': {'public': 'secteur-public', 'grands-comptes': 'grands-comptes', 'pme': 'pme-eti'},
           'legal': {'mentions': 'mentions-legales', 'confidentialite': 'confidentialite', 'accessibilite': 'accessibilite', 'plan': 'plan-du-site'}},
    'nl': {'services': 'diensten', 'standards': 'normen', 'sectors': 'sectoren', 'firm': 'over-ons', 'resources': 'kennisbank', 'contact': 'contact',
           'svc': {'audit-rgaa': 'rgaa-audit', 'audit-raam': 'raam-audit', 'audit-conformite': 'conformiteitsaudit', 'recette': 'controle-bij-oplevering', 'test-utilisateur': 'tests-met-echte-gebruikers', 'developpement': 'toegankelijke-ontwikkeling', 'prestation-informatique': 'it-diensten', 'aide-recrutement': 'hulp-bij-werving', 'elearning': 'e-learning-toegankelijkheid', 'formations': 'opleidingen'},
           'country': {'france': 'frankrijk', 'belgique': 'belgie', 'luxembourg': 'luxemburg', 'suisse': 'zwitserland'},
           'sector': {'public': 'publieke-sector', 'grands-comptes': 'grote-ondernemingen', 'pme': 'kmo'},
           'legal': {'mentions': 'juridische-informatie', 'confidentialite': 'privacy', 'accessibilite': 'toegankelijkheid', 'plan': 'sitemap'}},
    'de': {'services': 'leistungen', 'standards': 'standards', 'sectors': 'branchen', 'firm': 'ueber-uns', 'resources': 'wissen', 'contact': 'kontakt',
           'svc': {'audit-rgaa': 'rgaa-audit', 'audit-raam': 'raam-audit', 'audit-conformite': 'konformitaetsaudit', 'recette': 'barrierefreiheits-abnahme', 'test-utilisateur': 'tests-mit-echten-nutzern', 'developpement': 'barrierefreie-entwicklung', 'prestation-informatique': 'it-dienstleistungen', 'aide-recrutement': 'personalgewinnung', 'elearning': 'e-learning-barrierefreiheit', 'formations': 'schulungen'},
           'country': {'france': 'frankreich', 'belgique': 'belgien', 'luxembourg': 'luxemburg', 'suisse': 'schweiz'},
           'sector': {'public': 'oeffentlicher-sektor', 'grands-comptes': 'grossunternehmen', 'pme': 'kmu'},
           'legal': {'mentions': 'impressum', 'confidentialite': 'datenschutz', 'accessibilite': 'barrierefreiheit', 'plan': 'sitemap'}},
    'en': {'services': 'services', 'standards': 'standards', 'sectors': 'sectors', 'firm': 'about', 'resources': 'resources', 'contact': 'contact',
           'svc': {'audit-rgaa': 'rgaa-audit', 'audit-raam': 'raam-audit', 'audit-conformite': 'compliance-audit', 'recette': 'accessibility-acceptance-testing', 'test-utilisateur': 'real-user-testing', 'developpement': 'accessible-development', 'prestation-informatique': 'it-services', 'aide-recrutement': 'recruitment-support', 'elearning': 'accessibility-e-learning', 'formations': 'training'},
           'country': {'france': 'france', 'belgique': 'belgium', 'luxembourg': 'luxembourg', 'suisse': 'switzerland'},
           'sector': {'public': 'public-sector', 'grands-comptes': 'large-companies', 'pme': 'smes'},
           'legal': {'mentions': 'legal-notice', 'confidentialite': 'privacy', 'accessibilite': 'accessibility', 'plan': 'sitemap'}},
}


# Articles du blog : un fichier JSON par article et par langue, dans gen/articles/<id>.<lang>.json
# Les articles sont découverts automatiquement (fichiers <id>.fr.json). Ordre d'affichage :
# l'article pilier d'abord, puis du plus récent au plus ancien.
PILLAR = 'guide'
_LEGACY_ORDER = ['guide', 'eaa', 'france', 'declaration', 'belgique', 'luxembourg', 'suisse', 'normes']
_ART_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'articles')

def _load_articles():
    ids = sorted(f[:-8] for f in _os.listdir(_ART_DIR) if f.endswith('.fr.json'))
    out = {l: {} for l in LANGS}
    for a in ids:
        for l in LANGS:
            f = _os.path.join(_ART_DIR, '%s.%s.json' % (a, l))
            if _os.path.exists(f):
                out[l][a] = _json.load(open(f, encoding='utf-8'))
    def rank(a):
        legacy = _LEGACY_ORDER.index(a) if a in _LEGACY_ORDER else -1
        return (a != PILLAR, -int(out['fr'][a]['date'].replace('-', '')), legacy, a)
    return out, sorted(ids, key=rank)

ART, ARTICLES = _load_articles()
# Seuls les articles disponibles dans les 4 langues sont publiés
ART_LIVE = [a for a in ARTICLES if all(a in ART[l] for l in LANGS)]


def keys():
    k = ['home', 'services'] + ['svc:' + s for s in SVC] + ['standards'] + ['country:' + c for c in COUNTRIES]
    k += ['sector:' + s for s in SECTORS] + ['firm', 'resources'] + ['article:' + a for a in ART_LIVE] + ['contact'] + ['legal:' + l for l in LEGAL]
    return k


def path(lang, key):
    """Chemin sans slash initial, terminé par / ('' pour l'accueil FR)."""
    S = SLUGS[lang]
    pre = '' if lang == 'fr' else lang + '/'
    if key == 'home':
        p = ''
    elif key in ('services', 'standards', 'firm', 'resources', 'contact'):
        p = S[key] + '/'
    elif key.startswith('svc:'):
        p = S['services'] + '/' + S['svc'][key[4:]] + '/'
    elif key.startswith('country:'):
        p = S['standards'] + '/' + S['country'][key[8:]] + '/'
    elif key.startswith('sector:'):
        p = S['sectors'] + '/' + S['sector'][key[7:]] + '/'
    elif key.startswith('article:'):
        p = S['resources'] + '/' + ART[lang][key[8:]]['slug'] + '/'
    elif key.startswith('legal:'):
        p = S['legal'][key[6:]] + '/'
    elif key == '404':
        p = '404/'
    else:
        raise KeyError(key)
    return pre + p

# Valeurs canoniques (FR) envoyées au webhook, quel que soit l'ordre ou la langue du formulaire
COUNTRY_FR = {
    'France': 'France', 'Frankrijk': 'France', 'Frankreich': 'France',
    'Belgique': 'Belgique', 'Belgium': 'Belgique', 'België': 'Belgique', 'Belgien': 'Belgique',
    'Luxembourg': 'Luxembourg', 'Luxemburg': 'Luxembourg',
    'Suisse': 'Suisse', 'Switzerland': 'Suisse', 'Zwitserland': 'Suisse', 'Schweiz': 'Suisse',
    'Autre pays': 'Autre pays', 'Other country': 'Autre pays', 'Ander land': 'Autre pays', 'Anderes Land': 'Autre pays',
}
