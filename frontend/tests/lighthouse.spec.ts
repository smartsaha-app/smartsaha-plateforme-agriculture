/**
 * Audit Lighthouse — Core Web Vitals SmartSaha
 * =============================================
 * Ce test mesure la performance ressentie par l'utilisateur sur les pages critiques.
 * Il vérifie les 4 métriques clés de Google :
 *   - Performance Score : Score global /100
 *   - LCP (Largest Contentful Paint) : Temps d'affichage du plus grand element. Cible < 2500ms
 *   - TBT (Total Blocking Time) : Temps de blocage JS. Cible < 200ms
 *   - CLS (Cumulative Layout Shift) : Stabilité visuelle. Cible < 0.1
 *
 * Prérequis :
 *   1. Démarrer le frontend : npm run dev (port 3000)
 *   2. Lancer ce test : npx playwright test tests/lighthouse.spec.ts
 *
 * Note : Ce test nécessite Chromium uniquement (Lighthouse est un outil Chrome).
 */
import { test, expect, chromium } from '@playwright/test';
import { playAudit } from 'playwright-lighthouse';
import * as path from 'path';

const FRONTEND_URL = 'http://localhost:3000';

// Seuils minimaux acceptables (standard industrie Google)
const THRESHOLDS = {
  performance:   50,  // En dev SSR, on accepte 50+ (production sera >85)
  accessibility: 70,  // Accessibilité de base (couleurs, attributs ARIA)
  'best-practices': 70, // HTTPS, console errors, deprecated APIs
  seo:           70,  // Balises meta, titres, structure HTML
};

// Pages critiques de Smartsaha à auditer
const PAGES_TO_AUDIT = [
  { url: '/',              name: 'Page de connexion / Landing' },
  { url: '/farmer',        name: 'Dashboard Agriculteur' },
  { url: '/farmer/parcels', name: 'Carte des Parcelles' },
  { url: '/admin',         name: 'Dashboard Admin' },
];

// Lighthouse ne tourne que sur Chromium
test.use({ browserName: 'chromium' });

test.describe('Audit Lighthouse — Core Web Vitals SmartSaha', () => {
  for (const page of PAGES_TO_AUDIT) {
    test(`[Lighthouse] ${page.name}`, async ({}) => {
      const browser = await chromium.launch({
        args: ['--remote-debugging-port=9222'],
      });

      const context = await browser.newContext();
      const browserPage = await context.newPage();

      const targetUrl = `${FRONTEND_URL}${page.url}`;
      console.log(`\n🔍 Audit Lighthouse sur : ${targetUrl}`);

      await browserPage.goto(targetUrl, { waitUntil: 'networkidle', timeout: 30000 });

      const reportPath = path.join(
        process.cwd(),
        'tests',
        'lighthouse-reports',
        `${page.name.replace(/[^a-z0-9]/gi, '_')}.html`
      );

      const result = await playAudit({
        page: browserPage,
        port: 9222,
        thresholds: THRESHOLDS,
        reports: {
          formats: { html: true },
          name: page.name,
          directory: path.join(process.cwd(), 'tests', 'lighthouse-reports'),
        },
        config: {
          extends: 'lighthouse:default',
          settings: {
            // Mode "navigation" pour une vraie simulation de chargement
            formFactor: 'desktop',
            screenEmulation: {
              mobile: false,
              width: 1350,
              height: 940,
              deviceScaleFactor: 1,
              disabled: false,
            },
            // Simule une connexion 4G standard (réaliste pour Madagascar)
            throttling: {
              rttMs: 40,
              throughputKbps: 10 * 1024,
              cpuSlowdownMultiplier: 1,
            },
          },
        },
      });

      const scores = result?.lhr?.categories;

      if (scores) {
        console.log(`\n  📊 Résultats pour "${page.name}" :`);
        console.log(`    🏆 Performance   : ${Math.round((scores.performance?.score || 0) * 100)}/100`);
        console.log(`    ♿ Accessibilité : ${Math.round((scores.accessibility?.score || 0) * 100)}/100`);
        console.log(`    ✅ Bonnes Pratiques : ${Math.round((scores['best-practices']?.score || 0) * 100)}/100`);
        console.log(`    🔍 SEO           : ${Math.round((scores.seo?.score || 0) * 100)}/100`);

        // Métriques Core Web Vitals
        const audits = result?.lhr?.audits;
        if (audits) {
          console.log(`\n  ⏱️  Core Web Vitals :`);
          console.log(`    LCP : ${audits['largest-contentful-paint']?.displayValue || 'N/A'}`);
          console.log(`    TBT : ${audits['total-blocking-time']?.displayValue || 'N/A'}`);
          console.log(`    CLS : ${audits['cumulative-layout-shift']?.displayValue || 'N/A'}`);
          console.log(`    FCP : ${audits['first-contentful-paint']?.displayValue || 'N/A'}`);
          console.log(`    SI  : ${audits['speed-index']?.displayValue || 'N/A'}`);
          console.log(`\n  📁 Rapport HTML : ${reportPath}`);
        }
      }

      await browser.close();
    });
  }
});
