import { test, expect } from '@playwright/test';

test('homepage has expected title', async ({ page }) => {
  await page.goto('/');
  // On vérifie que le titre contient bien "SmartSaha"
  await expect(page).toHaveTitle(/SmartSaha/i);
});

test('check for main loading screen', async ({ page }) => {
  await page.goto('/');
  // Le chargement initial affiche "Smartsaha" avec une animation
  const loader = page.locator('h2:has-text("Smartsaha")');
  await expect(loader).toBeVisible();
  
  // Attendre la fin du chargement (isInitialized devient true, l'overlay disparaît)
  await expect(loader).not.toBeVisible({ timeout: 10000 });
});
