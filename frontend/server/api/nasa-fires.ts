/**
 * server/api/nasa-fires.ts
 * ─────────────────────────────────────────────────────────────────────────────
 * Proxy Nuxt server-side pour NASA FIRMS MODIS C6.1 CSV.
 * Évite les erreurs CORS lors d'un fetch direct depuis le navigateur.
 *
 * Usage :  GET /api/nasa-fires?days=1   (1 | 2 | 7)
 * Retourne : le contenu CSV brut filtré sur Madagascar côté serveur.
 */

export default defineEventHandler(async (event) => {
  const query  = getQuery(event)
  const days   = parseInt(String(query.days ?? '1'), 10) || 1

  // Choisir le fichier NASA FIRMS selon la fenêtre temporelle
  let file = 'MODIS_C6_1_Global_24h.csv'
  if (days > 2) file = 'MODIS_C6_1_Global_7d.csv'
  else if (days > 1) file = 'MODIS_C6_1_Global_48h.csv'

  const url = `https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/${file}`

  try {
    const response = await fetch(url, {
      headers: { 'User-Agent': 'SmartSaha-Platform/1.0 (contact: smartsahaapp@gmail.com)' },
    })

    if (!response.ok) {
      throw createError({ statusCode: response.status, statusMessage: `NASA FIRMS HTTP ${response.status}` })
    }

    const csv = await response.text()

    // Retourner le CSV brut — le filtrage Madagascar se fait côté client
    setResponseHeader(event, 'Content-Type', 'text/plain; charset=utf-8')
    setResponseHeader(event, 'Cache-Control', 'public, max-age=1800') // cache 30 min
    return csv

  } catch (err: any) {
    if (err.statusCode) throw err
    throw createError({
      statusCode: 502,
      statusMessage: 'NASA FIRMS indisponible',
    })
  }
})