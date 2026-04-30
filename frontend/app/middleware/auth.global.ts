import { useAuthStore } from "~/stores/auth";

export default defineNuxtRouteMiddleware(async (to) => {
  const PUBLIC_ROUTES = [
    '/',
    '/login',
    '/signup',
    '/reset-password',
    '/contact',
    '/features',
    '/guide',
    '/support',
  ];

  const authStore = useAuthStore();

  // Sur le client, on attend l'initialisation pour éviter les flashs/redirections erronées
  if (process.client && !authStore.isInitialized) {
    return;
  }

  const { $i18n } = useNuxtApp();
  const locales = $i18n.locales as any;
  const localeCodes = locales.value.map((l: any) => l.code);
  
  // Déterminer le chemin de base (sans le préfixe de langue)
  // ex: /mg/login -> /login, /en -> /
  const pathParts = to.path.split('/').filter(Boolean);
  let basePath = '/' + pathParts.join('/');
  
  if (pathParts.length > 0 && localeCodes.includes(pathParts[0])) {
    basePath = '/' + pathParts.slice(1).join('/');
  }

  const isAuthenticated = authStore.isAuthenticated;
  // Vérifie si la route est publique
  const isPublicRoute = PUBLIC_ROUTES.includes(basePath);

  // 1. Déjà connecté + tente d'aller sur une page publique restrictive (/login, /signup)
  if (isAuthenticated && (basePath === '/login' || basePath === '/signup')) {
    return navigateTo(authStore.getWorkspacePath());
  }

  // 2. Non connecté + tente d'aller sur une page protégée
  if (!isAuthenticated && !isPublicRoute) {
    return navigateTo('/login');
  }

  // 3. Cas particulier: "/" redirige vers le dashboard si connecté
  if (isAuthenticated && basePath === '/') {
    return navigateTo(authStore.getWorkspacePath());
  }
});