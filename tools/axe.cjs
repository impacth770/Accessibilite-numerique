// Contrôle d'accessibilité automatique (axe-core, WCAG 2.2 AA) sur la version preview du site.
// Prérequis : python3 gen/build.py preview ; npm install --no-save axe-core (Playwright est préinstallé).
// Usage : node tools/axe.cjs                 -> toutes les pages
//         node tools/axe.cjs ressources/x/ nl/kennisbank/y/   -> pages choisies (chemins relatifs)
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.join(__dirname, '..', 'preview');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
function walk(d) { return fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? (e.name === 'assets' ? [] : walk(path.join(d, e.name))) : (e.name === 'index.html' ? [path.join(d, e.name)] : [])); }
(async () => {
  const args = process.argv.slice(2);
  const files = args.length ? args.map(a => path.join(ROOT, a.replace(/^\/+/, ''), a.endsWith('.html') ? '' : 'index.html')) : walk(ROOT);
  const b = await chromium.launch(); const p = await b.newPage();
  const agg = {};
  for (const f of files) {
    await p.goto('file://' + f);
    await p.addScriptTag({ content: axeSrc });
    const r = await p.evaluate(async () => await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] }));
    for (const v of r.violations) { agg[v.id] = agg[v.id] || { impact: v.impact, pages: [] }; agg[v.id].pages.push(path.relative(ROOT, f)); }
  }
  await b.close();
  console.log(files.length + ' pages');
  console.log(JSON.stringify(agg, null, 1));
  process.exit(Object.keys(agg).length ? 1 : 0);
})();
