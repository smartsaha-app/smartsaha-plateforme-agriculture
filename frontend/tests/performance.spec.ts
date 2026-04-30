import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('Measure page load metrics', async ({ page }) => {
    // Navigation avec mesure simplifiée
    const startTime = Date.now();
    await page.goto('/');
    const loadTime = Date.now() - startTime;

    console.log(`\x1b[32m[Performance]\x1b[0m Page total navigation time: ${loadTime}ms`);

    // Analyse approfondie via l'API Navigation Timing
    const [performanceTiming] = await page.evaluate(() => {
      const [timing] = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[];
      return [timing.toJSON()];
    });

    const domContentLoaded = performanceTiming.domContentLoadedEventEnd - performanceTiming.startTime;
    const responseStart = performanceTiming.responseStart - performanceTiming.startTime;
    const loadEventStart = performanceTiming.loadEventStart - performanceTiming.startTime;

    console.log(`\x1b[34m[Metrics]\x1b[0m TTFB: ${responseStart.toFixed(2)}ms`);
    console.log(`\x1b[34m[Metrics]\x1b[0m DOM Content Loaded: ${domContentLoaded.toFixed(2)}ms`);
    console.log(`\x1b[34m[Metrics]\x1b[0m Load Event Start: ${loadEventStart.toFixed(2)}ms`);

    // Assertions de performance raisonnables pour un environnement local
    // (A ajuster selon la complexité de l'application)
    expect(domContentLoaded).toBeLessThan(5000); // Seuil de 5s maximum
    expect(responseStart).toBeLessThan(1000);    // TTFB attendu sous 1s
  });

  test('Check hydration and interaction stability', async ({ page }) => {
    await page.goto('/');
    // Attente que le loader disparaisse pour mesurer l'interactivité
    await page.waitForSelector('h2:has-text("Smartsaha")', { state: 'hidden' });
    
    // Mesurer une interaction simple
    const interactionStart = Date.now();
    // Cliquer sur le corps de la page
    await page.mouse.click(0, 0);
    const interactionTime = Date.now() - interactionStart;

    console.log(`\x1b[32m[Performance]\x1b[0m First interaction delay: ${interactionTime}ms`);
    expect(interactionTime).toBeLessThan(200);
  });
});
