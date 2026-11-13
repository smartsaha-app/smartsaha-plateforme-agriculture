/**
 * Retire le préfixe de langue d'un chemin (ex: /en/farmer/dashboard -> /farmer/dashboard).
 * Avec la stratégie `prefix_except_default`, route.path contient /en ou /mg :
 * toute comparaison avec un chemin "nu" doit passer par ce helper.
 */
export function stripLocalePrefix(path: string, localeCodes: string[]): string {
  const [, first, ...rest] = path.split('/')
  if (first && localeCodes.includes(first)) return '/' + rest.join('/')
  return path
}

/** Chemin courant sans préfixe de langue (réactif). */
export function useBasePath() {
  const route = useRoute()
  const { locales } = useI18n()
  return computed(() =>
    stripLocalePrefix(route.path, locales.value.map((l: any) => (typeof l === 'string' ? l : l.code)))
  )
}
