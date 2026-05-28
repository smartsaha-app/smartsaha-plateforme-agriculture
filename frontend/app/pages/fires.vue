<template>
  <div class="min-h-screen bg-gray-50 font-['Readex_Pro']">

    <!-- ═══════════════ HERO ═══════════════ -->
    <section class="relative pt-32 pb-10 overflow-hidden">
      <!-- Gradient top -->
      <div class="absolute inset-x-0 top-0 h-[500px] bg-gradient-to-b from-orange-50/80 via-white to-gray-50 pointer-events-none"></div>
      <div class="absolute top-20 right-0 w-[500px] h-[500px] bg-orange-100/30 rounded-full blur-[120px] pointer-events-none"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">

        <!-- ── Title row ── -->
        <div class="flex flex-col lg:flex-row items-start lg:items-end justify-between gap-8 mb-8">
          <div>
            <!-- Live badge -->
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 bg-orange-100 border border-orange-200/80 rounded-full mb-5">
              <span class="relative flex h-2 w-2 flex-shrink-0">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-500 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-orange-500"></span>
              </span>
              <span class="text-[10px] font-black uppercase tracking-[0.15em] text-orange-700">Surveillance satellite en temps réel · MODIS C6.1</span>
            </div>

            <h1 class="text-[2.8rem] sm:text-[3.6rem] font-black text-[#112830] leading-[1.06] tracking-tight">
              Incendies actifs
              <span class="block text-orange-500">à Madagascar</span>
            </h1>
            <p class="mt-4 text-gray-500 text-[15px] font-medium leading-relaxed max-w-xl">
              Foyers détectés par satellite <strong class="text-[#112830]">MODIS</strong> (NASA).
              Données publiques officielles, mises à jour toutes les <strong class="text-[#112830]">3 à 6 heures</strong>.
            </p>
          </div>

          <!-- NASA source card -->
          <a href="https://firms.modaps.eosdis.nasa.gov/" target="_blank" rel="noopener"
            class="flex items-center gap-4 px-5 py-4 bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md hover:border-blue-200 transition-all group flex-shrink-0">
            <div class="w-11 h-11 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
              <i class="bx bxs-globe-alt text-blue-600 text-xl"></i>
            </div>
            <div>
              <p class="text-[9px] text-gray-400 font-black uppercase tracking-widest mb-0.5">Source officielle</p>
              <p class="font-black text-[#112830] text-[15px]">NASA FIRMS</p>
              <p class="text-[10px] text-gray-400">firms.modaps.eosdis.nasa.gov</p>
            </div>
            <i class="bx bx-link-external text-gray-300 group-hover:text-blue-500 text-sm ml-2 transition-colors"></i>
          </a>
        </div>

        <!-- ── Trust bar ── -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-7">
          <div class="bg-white border border-gray-100 rounded-xl px-4 py-3 flex items-center gap-3 shadow-sm">
            <div class="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <i class="bx bxs-data text-blue-600 text-sm"></i>
            </div>
            <div>
              <p class="text-[9px] text-gray-400 font-black uppercase tracking-wider">Source</p>
              <p class="text-[12px] font-black text-[#112830]">NASA FIRMS</p>
            </div>
          </div>
          <div class="bg-white border border-gray-100 rounded-xl px-4 py-3 flex items-center gap-3 shadow-sm">
            <div class="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <i class="bx bx-time-five text-emerald-600 text-sm"></i>
            </div>
            <div>
              <p class="text-[9px] text-gray-400 font-black uppercase tracking-wider">Fréquence</p>
              <p class="text-[12px] font-black text-[#112830]">Toutes les 3–6h</p>
            </div>
          </div>
          <div class="bg-white border border-gray-100 rounded-xl px-4 py-3 flex items-center gap-3 shadow-sm">
            <div class="w-8 h-8 bg-orange-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <i class="bx bxs-planet text-orange-500 text-sm"></i>
            </div>
            <div>
              <p class="text-[9px] text-gray-400 font-black uppercase tracking-wider">Satellite</p>
              <p class="text-[12px] font-black text-[#112830]">MODIS Aqua & Terra</p>
            </div>
          </div>
          <div class="bg-white border border-gray-100 rounded-xl px-4 py-3 flex items-center gap-3 shadow-sm">
            <div class="w-8 h-8 bg-[#10b481]/10 rounded-lg flex items-center justify-center flex-shrink-0">
              <i class="bx bx-check-shield text-[#10b481] text-sm"></i>
            </div>
            <div>
              <p class="text-[9px] text-gray-400 font-black uppercase tracking-wider">Données</p>
              <p class="text-[12px] font-black text-[#112830]">100% officielles</p>
            </div>
          </div>
        </div>

        <!-- ── Stats ── -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">

          <!-- Total -->
          <div class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-orange-200 transition-all group">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 bg-orange-50 rounded-xl flex items-center justify-center group-hover:bg-orange-100 transition-colors">
                <i class="bx bxs-flame text-orange-500 text-xl"></i>
              </div>
              <span class="text-[9px] font-black uppercase tracking-wider text-orange-500 bg-orange-50 px-2 py-1 rounded-lg">
                {{ selectedDays === 1 ? '24h' : selectedDays + 'j' }}
              </span>
            </div>
            <div v-if="isLoading" class="h-9 w-20 bg-gray-100 rounded-lg animate-pulse mb-1"></div>
            <span v-else class="text-[2.2rem] font-black text-[#112830] leading-none">{{ computedSummary.total }}</span>
            <p class="text-[11px] text-gray-400 font-semibold mt-2">Foyers actifs</p>
          </div>

          <!-- Critical -->
          <div class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-red-200 transition-all group">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 bg-red-50 rounded-xl flex items-center justify-center group-hover:bg-red-100 transition-colors">
                <i class="bx bxs-error text-red-500 text-xl"></i>
              </div>
              <span class="text-[9px] font-black text-red-600 bg-red-50 px-2 py-1 rounded-lg">≥ 370 K</span>
            </div>
            <div v-if="isLoading" class="h-9 w-20 bg-gray-100 rounded-lg animate-pulse mb-1"></div>
            <span v-else class="text-[2.2rem] font-black text-red-600 leading-none">{{ computedSummary.critical }}</span>
            <p class="text-[11px] text-gray-400 font-semibold mt-2">Critique</p>
          </div>

          <!-- High -->
          <div class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-orange-200 transition-all group">
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 bg-orange-50 rounded-xl flex items-center justify-center group-hover:bg-orange-100 transition-colors">
                <i class="bx bx-trending-up text-orange-500 text-xl"></i>
              </div>
              <span class="text-[9px] font-black text-orange-600 bg-orange-50 px-2 py-1 rounded-lg">≥ 330 K</span>
            </div>
            <div v-if="isLoading" class="h-9 w-20 bg-gray-100 rounded-lg animate-pulse mb-1"></div>
            <span v-else class="text-[2.2rem] font-black text-orange-500 leading-none">{{ computedSummary.high }}</span>
            <p class="text-[11px] text-gray-400 font-semibold mt-2">Élevé</p>
          </div>

        </div>

        <!-- ── Controls ── -->
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div class="flex items-center gap-2 flex-wrap">
            <!-- Period selector -->
            <div class="flex items-center gap-1 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
              <button v-for="d in [1, 3, 7]" :key="d"
                @click="changeDays(d)"
                :class="[
                  'px-4 py-2 rounded-lg text-[11px] font-black uppercase tracking-widest transition-all',
                  selectedDays === d
                    ? 'bg-[#112830] text-white shadow-sm'
                    : 'text-gray-500 hover:text-[#112830] hover:bg-gray-50'
                ]">
                {{ d === 1 ? '24 h' : d === 3 ? '3 jours' : '7 jours' }}
              </button>
            </div>

            <!-- Source badge -->
            <div v-if="dataSource" :class="[
              'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-[10px] font-black uppercase tracking-wider',
              dataSource === 'backend'
                ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                : 'bg-blue-50 border-blue-200 text-blue-700'
            ]">
              <i :class="['text-xs', dataSource === 'backend' ? 'bx bx-server' : 'bx bx-satellite']"></i>
              {{ dataSource === 'backend' ? 'SmartSaha API' : 'NASA FIRMS Direct' }}
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span v-if="lastUpdated" class="text-[11px] text-gray-400 font-semibold hidden sm:block">
              <i class="bx bx-time text-xs mr-1"></i>Mis à jour {{ lastUpdated }}
            </span>
            <button @click="loadData" :disabled="isLoading"
              class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] hover:bg-[#1c3e4a] active:scale-95 text-white rounded-xl text-[11px] font-black uppercase tracking-widest transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
              <i v-if="isLoading" class="bx bx-loader-alt animate-spin text-sm"></i>
              <i v-else class="bx bx-refresh text-sm"></i>
              Actualiser
            </button>
          </div>
        </div>

        <!-- ── Map (dark satellite) ── -->
        <div class="relative rounded-2xl overflow-hidden border border-gray-200"
          style="height: 600px; box-shadow: 0 8px 40px rgba(0,0,0,0.12);">

          <!-- Loading overlay -->
          <Transition name="fade-overlay">
            <div v-if="isLoading" class="absolute inset-0 bg-black/60 backdrop-blur-sm z-30 flex flex-col items-center justify-center gap-4">
              <div class="relative">
                <div class="w-16 h-16 bg-orange-500/15 border border-orange-400/30 rounded-2xl flex items-center justify-center">
                  <i class="bx bx-loader-alt animate-spin text-orange-400 text-3xl"></i>
                </div>
                <div class="absolute -inset-1 rounded-2xl border border-orange-500/15 animate-pulse"></div>
              </div>
              <div class="text-center">
                <p class="text-[14px] text-gray-200 font-semibold">
                  {{ nasaLoading ? 'Chargement NASA FIRMS…' : 'Récupération des données…' }}
                </p>
                <p class="text-[12px] text-gray-500 mt-1">Source : MODIS C6.1 · NASA</p>
              </div>
            </div>
          </Transition>

          <!-- Error overlay -->
          <Transition name="fade-overlay">
            <div v-if="fetchError && !isLoading" class="absolute inset-0 z-20 flex flex-col items-center justify-center gap-4 bg-black/60 backdrop-blur-sm">
              <div class="w-16 h-16 bg-red-500/10 border border-red-400/25 rounded-2xl flex items-center justify-center">
                <i class="bx bx-wifi-off text-red-400 text-2xl"></i>
              </div>
              <div class="text-center">
                <p class="text-white font-black text-[15px] mb-1">Données indisponibles</p>
                <p class="text-gray-400 text-[13px] max-w-xs">{{ fetchError }}</p>
                <button @click="loadData" class="mt-4 px-5 py-2 bg-white/10 hover:bg-white/20 border border-white/15 text-white rounded-xl text-[12px] font-bold transition-all">
                  Réessayer
                </button>
              </div>
            </div>
          </Transition>

          <!-- No data overlay -->
          <Transition name="fade-overlay">
            <div v-if="!isLoading && !fetchError && fires.length === 0 && hasLoaded" class="absolute inset-0 z-10 flex flex-col items-center justify-center gap-3 pointer-events-none">
              <div class="bg-black/75 backdrop-blur-md rounded-2xl px-8 py-6 text-center border border-white/10">
                <div class="w-12 h-12 bg-emerald-500/15 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <i class="bx bx-check-shield text-emerald-400 text-2xl"></i>
                </div>
                <p class="text-white font-black text-[15px]">Aucun foyer actif</p>
                <p class="text-gray-400 text-[12px] mt-1">Zone Madagascar · {{ selectedDays === 1 ? '24 dernières heures' : selectedDays + ' derniers jours' }}</p>
              </div>
            </div>
          </Transition>

          <!-- Leaflet map -->
          <div id="fires-map-public" class="w-full h-full z-0 bg-[#0d1117]"></div>

          <!-- Legend (top-left) -->
          <div class="absolute top-3 left-3 z-10 bg-black/80 backdrop-blur-md border border-white/10 rounded-xl px-3.5 py-3 min-w-[155px]">
            <p class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-2.5">Sévérité</p>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <span class="relative flex h-3.5 w-3.5 flex-shrink-0">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-60"></span>
                  <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-red-600"></span>
                </span>
                <span class="text-[11px] text-gray-300 font-semibold">Critique ≥ 370 K</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-orange-500 flex-shrink-0 shadow-[0_0_5px_#f97316]"></span>
                <span class="text-[11px] text-gray-300 font-semibold">Élevé ≥ 330 K</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400 flex-shrink-0 ml-px"></span>
                <span class="text-[11px] text-gray-300 font-semibold">Moyen &lt; 330 K</span>
              </div>
            </div>
          </div>

          <!-- Count badge (bottom center) -->
          <div v-if="fires.length > 0" class="absolute bottom-3 left-1/2 -translate-x-1/2 z-10">
            <div class="bg-black/80 backdrop-blur-md border border-orange-500/30 rounded-full px-5 py-2 flex items-center gap-2.5">
              <i class="bx bxs-flame text-orange-400 text-sm animate-pulse"></i>
              <span class="text-[12px] font-black text-white">
                {{ fires.length }} foyer{{ fires.length > 1 ? 's' : '' }} détecté{{ fires.length > 1 ? 's' : '' }} · Madagascar
              </span>
            </div>
          </div>
        </div>

        <!-- ── Data Table ── -->
        <div v-if="fires.length > 0" class="mt-8">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <div>
              <h2 class="text-xl font-black text-[#112830]">Détail des foyers détectés</h2>
              <p class="text-sm text-gray-400 font-medium mt-0.5">
                {{ displayFires.length }} / {{ fires.length }} hotspot{{ fires.length > 1 ? 's' : '' }} MODIS ·
                {{ selectedDays === 1 ? '24 dernières heures' : selectedDays + ' derniers jours' }}
              </p>
            </div>
            <span class="text-[11px] text-gray-400 font-semibold hidden sm:flex items-center gap-1">
              <i class="bx bx-mouse-alt text-xs"></i>Cliquer pour localiser sur la carte
            </span>
          </div>

          <div class="bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="bg-gray-50 border-b border-gray-100">
                    <th class="text-left px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest w-12">#</th>
                    <th class="text-left px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Sévérité</th>
                    <th class="text-left px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Date · Heure UTC</th>
                    <th class="text-left px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Brightness (K)</th>
                    <th class="text-left px-5 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden sm:table-cell">Satellite</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(fire, idx) in displayFires" :key="fire.uuid"
                    class="border-b border-gray-50 hover:bg-orange-50/50 transition-colors cursor-pointer group"
                    @click="flyToFire(fire)">
                    <td class="px-5 py-4 text-gray-300 font-bold text-xs">{{ idx + 1 }}</td>
                    <td class="px-5 py-4">
                      <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-wider border', severityBadgeClass(fire.severity)]">
                        <span :class="['w-1.5 h-1.5 rounded-full flex-shrink-0', severityDotClass(fire.severity)]"></span>
                        {{ fire.severity_label || severityFr(fire.severity) }}
                      </span>
                    </td>
                    <td class="px-5 py-4">
                      <p class="font-bold text-[#112830] text-sm">{{ formatDate(fire.acq_date) }}</p>
                      <p class="text-[11px] text-gray-400 font-mono mt-0.5">{{ formatTime(fire.acq_time) }}</p>
                    </td>
                    <td class="px-5 py-4">
                      <span :class="['text-[17px] font-black tabular-nums', brightnessColor(fire.brightness)]">
                        {{ fire.brightness ? Number(fire.brightness).toFixed(0) : '—' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 hidden sm:table-cell">
                      <span class="text-sm text-gray-400 font-semibold">{{ fire.satellite || 'MODIS' }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Footer note if more than 30 -->
            <div v-if="fires.length > 30" class="px-5 py-3 border-t border-gray-100 bg-gray-50/60">
              <p class="text-[11px] text-gray-400 font-semibold text-center">
                Affichage des 30 foyers les plus sévères sur <strong class="text-[#112830]">{{ fires.length }}</strong> détectés
              </p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ═══════════════ CTA ═══════════════ -->
    <section class="py-20 px-4 sm:px-6">
      <div class="max-w-4xl mx-auto">
        <div class="relative overflow-hidden rounded-[2rem] p-8 sm:p-12"
          style="background: linear-gradient(135deg, #0a1f15 0%, #112830 50%, #0d2a1a 100%);">
          <div class="absolute -right-16 -top-16 w-48 h-48 bg-[#10b481]/10 rounded-full blur-3xl pointer-events-none"></div>
          <div class="absolute -left-8 -bottom-8 w-36 h-36 bg-orange-500/6 rounded-full blur-2xl pointer-events-none"></div>

          <div class="relative z-10 flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
            <div class="flex-1 text-center lg:text-left">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-[#10b481]/12 border border-[#10b481]/20 rounded-full mb-5">
                <i class="bx bxs-bell text-[#10b481] text-sm"></i>
                <span class="text-[9px] font-black uppercase tracking-widest text-[#10b481]">Alertes SMS &amp; Email · Temps réel</span>
              </div>
              <h2 class="text-2xl sm:text-3xl font-black text-white leading-tight mb-3">
                Soyez alerté dès qu'un feu<br>
                <span class="text-[#10b481]">approche vos parcelles</span>
              </h2>
              <p class="text-gray-400 text-[13px] leading-relaxed max-w-sm mx-auto lg:mx-0">
                SmartSaha croise les données NASA FIRMS avec vos terres enregistrées
                et vous notifie automatiquement avant qu'il soit trop tard.
              </p>
            </div>
            <div class="flex flex-col gap-3 flex-shrink-0 w-full sm:w-auto">
              <NuxtLink to="/signup"
                class="flex items-center justify-center gap-2.5 px-7 py-4 bg-[#10b481] hover:bg-[#0da070] text-white rounded-xl font-black text-[11px] uppercase tracking-widest shadow-xl shadow-[#10b481]/25 hover:-translate-y-0.5 transition-all active:scale-95">
                <i class="bx bx-user-plus text-sm"></i>
                Créer un compte gratuit
              </NuxtLink>
              <NuxtLink to="/features"
                class="flex items-center justify-center gap-2 px-7 py-4 bg-white/6 hover:bg-white/10 border border-white/12 text-gray-300 hover:text-white rounded-xl font-black text-[11px] uppercase tracking-widest transition-all">
                Découvrir SmartSaha
                <i class="bx bx-chevron-right text-sm text-[#10b481]"></i>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Toast -->
    <Transition name="toast-slide">
      <div v-if="toast.show" class="fixed bottom-8 right-6 z-[200]">
        <div :class="[
          'flex items-center gap-3 px-5 py-3.5 rounded-xl shadow-2xl text-[13px] font-bold text-white',
          toast.type === 'success' ? 'bg-emerald-600' : 'bg-rose-600'
        ]">
          <i :class="['text-lg', toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle']"></i>
          {{ toast.message }}
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "vitrine" })

import { ref, computed, onMounted, onUnmounted } from "vue"
import { useApi } from "~/composables/useApi"

// ── SEO ──────────────────────────────────────────────────────────────────────
useHead({
  title: "Incendies Madagascar · Surveillance NASA FIRMS — SmartSaha",
  meta: [
    { name: "description", content: "Carte des incendies actifs à Madagascar. Détection satellite MODIS C6.1 via NASA FIRMS, croisée avec les parcelles agricoles SmartSaha." },
    { property: "og:title",       content: "🔥 Incendies Madagascar — SmartSaha" },
    { property: "og:description", content: "Foyers actifs à Madagascar détectés par satellite MODIS NASA FIRMS. Données officielles en temps réel." },
  ],
})

// ── Types ─────────────────────────────────────────────────────────────────────
interface FireAlert {
  uuid:           string
  latitude:       number
  longitude:      number
  brightness:     number
  confidence:     number
  acq_date:       string
  acq_time:       string
  satellite:      string
  source?:        string
  parcel?:        string | null
  parcel_name?:   string | null
  owner_email?:   string | null
  distance_km?:   number | null
  severity:       "CRITICAL" | "HIGH" | "MEDIUM"
  severity_label: string
  is_active:      boolean
  created_at:     string
}

interface FireSummary {
  total_active:          number
  critical_count:        number
  high_count:            number
  medium_count:          number
  parcels_at_risk_count: number
  last_update:           string
}

// ── State ─────────────────────────────────────────────────────────────────────
const fires        = ref<FireAlert[]>([])
const backendSum   = ref<FireSummary | null>(null)
const isLoading    = ref(false)
const nasaLoading  = ref(false)
const hasLoaded    = ref(false)
const fetchError   = ref("")
const selectedDays = ref(1)
const lastUpdated  = ref("")
const dataSource   = ref<"" | "backend" | "nasa_direct">("")
const toast        = ref({ show: false, message: "", type: "success" as "success" | "error" })

// Leaflet — chargé dynamiquement (SSR-safe, package npm local)
let L:            any = null
let mapInstance:  any = null
let markersLayer: any = null

const MDG_CENTER: [number, number] = [-18.9, 46.9]

// ── Computed ──────────────────────────────────────────────────────────────────
const computedSummary = computed(() => {
  if (backendSum.value) {
    return {
      total:       backendSum.value.total_active,
      critical:    backendSum.value.critical_count,
      high:        backendSum.value.high_count,
      nearParcels: backendSum.value.parcels_at_risk_count,
    }
  }
  return {
    total:       fires.value.length,
    critical:    fires.value.filter(f => f.severity === "CRITICAL").length,
    high:        fires.value.filter(f => f.severity === "HIGH").length,
    nearParcels: fires.value.filter(f => f.parcel_name).length,
  }
})

const displayFires = computed(() =>
  [...fires.value]
    .sort((a, b) => {
      const order = { CRITICAL: 0, HIGH: 1, MEDIUM: 2 }
      const diff  = (order[a.severity] ?? 2) - (order[b.severity] ?? 2)
      if (diff !== 0) return diff
      return `${b.acq_date}${b.acq_time}`.localeCompare(`${a.acq_date}${a.acq_time}`)
    })
    .slice(0, 30)
)

// ── Helpers ───────────────────────────────────────────────────────────────────
function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => (toast.value.show = false), 3500)
}

function formatDate(d: string) {
  if (!d) return "—"
  return new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}

function formatTime(t: string) {
  if (!t) return "—"
  const s = String(t).padStart(4, "0")
  return `${s.slice(0, 2)}:${s.slice(2)} UTC`
}

function severityFr(s: string) {
  const m: Record<string, string> = { CRITICAL: "Critique", HIGH: "Élevé", MEDIUM: "Moyen" }
  return m[s] ?? s
}

// Light theme badge styles
function severityBadgeClass(s: string) {
  if (s === "CRITICAL") return "bg-red-50 text-red-700 border-red-200"
  if (s === "HIGH")     return "bg-orange-50 text-orange-700 border-orange-200"
  return "bg-amber-50 text-amber-700 border-amber-200"
}

function severityDotClass(s: string) {
  if (s === "CRITICAL") return "bg-red-500"
  if (s === "HIGH")     return "bg-orange-500"
  return "bg-amber-400"
}

function brightnessColor(b: number) {
  if (!b)    return "text-gray-400"
  if (b >= 370) return "text-red-600"
  if (b >= 330) return "text-orange-500"
  return "text-amber-500"
}

function getMarkerColor(severity: string) {
  if (severity === "CRITICAL") return "#ef4444"
  if (severity === "HIGH")     return "#f97316"
  return "#f59e0b"
}

// ── NASA CSV parser ────────────────────────────────────────────────────────────
function parseMDGFromCSV(csv: string): FireAlert[] {
  const lines = csv.split("\n").filter(l => l.trim())
  if (lines.length < 2) return []

  const headerLine = lines[0]
  if (!headerLine) return []
  const headers = headerLine.split(",").map(h => h.trim().replace(/^"|"$/g, ""))

  const col = (n: string) => headers.indexOf(n)
  const latIdx  = col("latitude")
  const lonIdx  = col("longitude")
  const brtIdx  = col("brightness")
  const dateIdx = col("acq_date")
  const timeIdx = col("acq_time")
  const satIdx  = col("satellite")
  const confIdx = col("confidence")

  if (latIdx < 0 || lonIdx < 0) return []

  const results: FireAlert[] = []

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i]
    if (!line) continue
    const cols = line.split(",")

    const lat = parseFloat(cols[latIdx] ?? "")
    const lon = parseFloat(cols[lonIdx] ?? "")
    if (isNaN(lat) || isNaN(lon)) continue

    // Madagascar bounding box
    if (lat < -25.6 || lat > -11.9 || lon < 43.2 || lon > 50.5) continue

    const brightness = parseFloat(cols[brtIdx] ?? "") || 0
    const severity: "CRITICAL" | "HIGH" | "MEDIUM" =
      brightness >= 370 ? "CRITICAL" :
      brightness >= 330 ? "HIGH" : "MEDIUM"

    results.push({
      uuid:          `nasa-${i}-${lat}-${lon}`,
      latitude:      lat,
      longitude:     lon,
      brightness,
      confidence:    parseInt(cols[confIdx] ?? "") || 0,
      acq_date:      (cols[dateIdx] ?? "").trim(),
      acq_time:      (cols[timeIdx] ?? "").trim(),
      satellite:     (cols[satIdx]  ?? "MODIS").trim(),
      severity,
      severity_label: severityFr(severity),
      is_active:     true,
      created_at:    new Date().toISOString(),
      parcel:        null,
      parcel_name:   null,
      distance_km:   null,
    })
  }

  return results
}

// ── API calls ─────────────────────────────────────────────────────────────────
const { apiFetch } = useApi()

async function loadFromBackend() {
  const [alertData, sumData]: [any, any] = await Promise.all([
    apiFetch(`/api/fire/alerts/?days=${selectedDays.value}&ordering=-acq_date`),
    apiFetch("/api/fire/alerts/summary/"),
  ])
  return {
    fires:   (alertData?.results ?? alertData ?? []) as FireAlert[],
    summary: (sumData ?? null) as FireSummary | null,
  }
}

async function loadFromNASA(): Promise<FireAlert[]> {
  const csv = await $fetch<string>(`/api/nasa-fires?days=${selectedDays.value}`)
  return parseMDGFromCSV(csv)
}

// ── Main load ─────────────────────────────────────────────────────────────────
async function loadData() {
  isLoading.value   = true
  nasaLoading.value = false
  fetchError.value  = ""
  dataSource.value  = ""

  let loaded = false

  // 1. Try SmartSaha backend (has parcel proximity data)
  try {
    const { fires: bf, summary: bs } = await loadFromBackend()
    if (bf.length > 0) {
      fires.value      = bf
      backendSum.value = bs
      dataSource.value = "backend"
      loaded = true
    } else {
      backendSum.value = bs
    }
  } catch { /* backend down, try NASA */ }

  // 2. Fallback — NASA FIRMS CSV direct (always real data)
  if (!loaded) {
    try {
      nasaLoading.value = true
      const nf = await loadFromNASA()
      fires.value       = nf
      backendSum.value  = null
      dataSource.value  = nf.length > 0 ? "nasa_direct" : ""
      loaded = true
    } catch {
      fetchError.value = "Impossible de joindre le serveur SmartSaha ni NASA FIRMS."
      showToast("Erreur de chargement des données.", "error")
    }
  }

  if (loaded) {
    hasLoaded.value   = true
    lastUpdated.value = new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })
    updateMarkers()
    if (fires.value.length === 0) showToast("Aucun foyer actif sur cette période.")
  }

  isLoading.value   = false
  nasaLoading.value = false
}

function changeDays(d: number) {
  selectedDays.value = d
  loadData()
}

// ── Map ───────────────────────────────────────────────────────────────────────
function injectMarkerCSS() {
  if (document.getElementById("fire-marker-style")) return
  const style = document.createElement("style")
  style.id = "fire-marker-style"
  style.textContent = `
    @keyframes firePulse  { 0%{transform:scale(0.7);opacity:0.9} 70%{transform:scale(2.4);opacity:0} 100%{transform:scale(0.7);opacity:0} }
    @keyframes firePulse2 { 0%{transform:scale(0.7);opacity:0.7} 70%{transform:scale(3.1);opacity:0} 100%{transform:scale(0.7);opacity:0} }
    .fp1 { animation: firePulse  1.8s ease-out infinite; }
    .fp2 { animation: firePulse2 1.8s ease-out infinite 0.7s; }
  `
  document.head.appendChild(style)
}

function buildMarkerIcon(fire: FireAlert) {
  const c = getMarkerColor(fire.severity)

  if (fire.severity === "CRITICAL") {
    return L.divIcon({
      className: "",
      html: `<div style="position:relative;width:40px;height:40px">
        <div class="fp2" style="position:absolute;inset:0;background:${c};border-radius:50%;opacity:0.3"></div>
        <div class="fp1" style="position:absolute;inset:0;background:${c};border-radius:50%;opacity:0.5"></div>
        <div style="position:absolute;inset:11px;background:${c};border-radius:50%;border:2.5px solid rgba(255,255,255,0.95);box-shadow:0 0 12px ${c},0 0 24px ${c}55"></div>
      </div>`,
      iconSize: [40, 40], iconAnchor: [20, 20], popupAnchor: [0, -22],
    })
  }

  if (fire.severity === "HIGH") {
    return L.divIcon({
      className: "",
      html: `<div style="position:relative;width:28px;height:28px">
        <div class="fp1" style="position:absolute;inset:0;background:${c};border-radius:50%;opacity:0.45"></div>
        <div style="position:absolute;inset:7px;background:${c};border-radius:50%;border:2px solid rgba(255,255,255,0.85);box-shadow:0 0 8px ${c},0 0 16px ${c}44"></div>
      </div>`,
      iconSize: [28, 28], iconAnchor: [14, 14], popupAnchor: [0, -16],
    })
  }

  // MEDIUM
  return L.divIcon({
    className: "",
    html: `<div style="width:16px;height:16px;background:${c};border-radius:50%;border:2px solid rgba(255,255,255,0.85);box-shadow:0 0 6px ${c}99"></div>`,
    iconSize: [16, 16], iconAnchor: [8, 8], popupAnchor: [0, -10],
  })
}

function buildPopupHTML(fire: FireAlert): string {
  const c    = getMarkerColor(fire.severity)
  const near = fire.parcel_name
    ? `<div style="margin-top:8px;padding:7px 9px;background:#f0fdf4;border-radius:9px;border:1px solid #bbf7d0;display:flex;justify-content:space-between;gap:8px">
        <span style="color:#16a34a;font-weight:800;font-size:11px">📍 ${fire.parcel_name}</span>
        <span style="color:#16a34a;font-weight:700;font-size:11px">${fire.distance_km} km</span>
       </div>` : ""

  return `<div style="font-family:'Readex Pro',sans-serif;min-width:220px;padding:4px 2px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #eee">
      <span style="font-size:22px">🔥</span>
      <div>
        <div style="font-weight:900;font-size:13px;color:#112830;line-height:1.2">${severityFr(fire.severity)}</div>
        <div style="font-size:9px;color:#aaa;font-weight:700;text-transform:uppercase;letter-spacing:.05em">NASA FIRMS · MODIS C6.1</div>
      </div>
      <span style="margin-left:auto;padding:3px 8px;background:${c}18;color:${c};font-size:9px;font-weight:900;border-radius:6px;text-transform:uppercase;letter-spacing:.06em">${fire.severity}</span>
    </div>
    <div style="display:grid;gap:5px;font-size:12px">
      <div style="display:flex;justify-content:space-between;gap:12px"><span style="color:#888">Date</span><strong style="color:#112830">${formatDate(fire.acq_date)}</strong></div>
      <div style="display:flex;justify-content:space-between;gap:12px"><span style="color:#888">Heure</span><strong style="color:#112830">${formatTime(fire.acq_time)}</strong></div>
      <div style="display:flex;justify-content:space-between;gap:12px"><span style="color:#888">Brightness</span><strong style="color:${c}">${fire.brightness ? Number(fire.brightness).toFixed(0) + " K" : "—"}</strong></div>
      <div style="display:flex;justify-content:space-between;gap:12px"><span style="color:#888">Confiance</span><strong style="color:#112830">${fire.confidence ?? "—"}%</strong></div>
      <div style="display:flex;justify-content:space-between;gap:12px"><span style="color:#888">Satellite</span><strong style="color:#112830">${fire.satellite || "MODIS"}</strong></div>
    </div>
    ${near}
  </div>`
}

// Initialisation carte — même pattern que les pages parcelles du projet
async function initMap() {
  if (!import.meta.client || mapInstance) return

  // Import Leaflet depuis node_modules (pas de CDN — package déjà installé)
  L = await import("leaflet")
  await import("leaflet/dist/leaflet.css")

  injectMarkerCSS()

  mapInstance = L.map("fires-map-public", {
    zoomControl: false,
    preferCanvas: false,
  }).setView(MDG_CENTER, 6)

  // OpenStreetMap officiel — gratuit, aucune clé
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors · NASA FIRMS MODIS C6.1',
    maxZoom: 19,
    subdomains: "abc",
  }).addTo(mapInstance)

  L.control.zoom({ position: "bottomleft" }).addTo(mapInstance)
  markersLayer = L.layerGroup().addTo(mapInstance)
}

function updateMarkers() {
  if (!L || !mapInstance || !markersLayer) return
  markersLayer.clearLayers()

  fires.value.forEach(fire => {
    const lat = Number(fire.latitude)
    const lon = Number(fire.longitude)
    if (isNaN(lat) || isNaN(lon)) return

    const icon   = buildMarkerIcon(fire)
    const marker = L.marker([lat, lon], { icon })
    marker.bindPopup(buildPopupHTML(fire), { maxWidth: 270 })
    markersLayer.addLayer(marker)
  })
}

function flyToFire(fire: FireAlert) {
  if (!mapInstance) return
  const el = document.getElementById("fires-map-public")
  if (el) el.scrollIntoView({ behavior: "smooth", block: "center" })
  setTimeout(() => mapInstance.flyTo([fire.latitude, fire.longitude], 13, { duration: 1.2 }), 260)
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  await initMap()   // charge Leaflet + CSS depuis node_modules, puis initialise
  loadData()        // récupère les données (backend → NASA fallback)
})

onUnmounted(() => {
  if (mapInstance) { mapInstance.remove(); mapInstance = null }
})
</script>

<style scoped>
.fade-overlay-enter-active, .fade-overlay-leave-active { transition: opacity 0.3s ease; }
.fade-overlay-enter-from, .fade-overlay-leave-to { opacity: 0; }

.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(10px); }
.toast-slide-leave-to   { opacity: 0; transform: translateY(10px); }
</style>
