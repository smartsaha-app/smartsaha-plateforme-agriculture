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
    '/sesily-ai',
    '/fires',
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
  // Garde la langue de la page demandée lors des redirections
  // (pas de préfixe = langue par défaut avec prefix_except_default → chemin inchangé)
  const targetLocale = localeCodes.includes(pathParts[0]) ? pathParts[0] : null;
  const toLocalePath = useLocalePath();
  const localePath = (path: string) => (targetLocale ? toLocalePath(path, targetLocale) : path);
  // Vérifie si la route est publique (correspondance stricte ou commence par /recover-password)
  const isPublicRoute = PUBLIC_ROUTES.includes(basePath) || basePath.startsWith('/recover-password');

  // 1. Déjà connecté + tente d'aller sur une page publique restrictive (/login, /signup)
  if (isAuthenticated && (basePath === '/login' || basePath === '/signup')) {
    return navigateTo(localePath(authStore.getWorkspacePath()));
  }

  // 2. Non connecté + tente d'aller sur une page protégée
  if (!isAuthenticated && !isPublicRoute) {
    return navigateTo(localePath('/login'));
  }

  // 3. Cas particulier: "/" redirige vers le dashboard si connecté
  if (isAuthenticated && basePath === '/') {
    return navigateTo(localePath(authStore.getWorkspacePath()));
  }
});