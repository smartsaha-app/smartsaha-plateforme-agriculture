<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen font-sans">

    <!-- ===== HEADER ===== -->
    <div class="mb-8">
      <nav class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-widest text-gray-400 mb-3">
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
          <i class="bx bx-map text-xs"></i> Parcelles
        </NuxtLink>
        <i class="bx bx-chevron-right text-[9px]"></i>
        <NuxtLink :to="`/farmer/parcels/show/${route.params.id}`" class="hover:text-[#10b481] transition-colors">
          {{ parcelName || 'Parcelle' }}
        </NuxtLink>
        <i class="bx bx-chevron-right text-[9px]"></i>
        <span class="text-gray-700">Historique des alertes</span>
      </nav>

      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-[28px] font-medium text-gray-900 tracking-tight">Historique des alertes</h1>
          <p class="text-[14px] text-gray-400 mt-0.5">{{ parcelName }} · du plus récent au plus ancien</p>
        </div>
        <div class="flex items-center gap-3">
          <NuxtLink :to="`/farmer/parcels/show/${route.params.id}`" class="p-2.5 bg-white border border-gray-200 rounded-xl text-gray-400 hover:text-gray-700 transition-all">
            <i class="bx bx-arrow-back text-lg"></i>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- ===== STATS SUMMARY ===== -->
    <div v-if="!isLoading && sortedAlerts.length" class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in alertStats" :key="stat.label" class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100/50">
        <div class="flex items-center justify-between mb-3">
          <span :class="['w-8 h-8 rounded-xl flex items-center justify-center text-sm', stat.iconBg]">
            <i :class="['bx', stat.icon]"></i>
          </span>
          <span class="text-[22px] font-bold text-gray-900">{{ stat.count }}</span>
        </div>
        <p class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">{{ stat.label }}</p>
      </div>
    </div>

    <!-- ===== FILTRES ===== -->
    <div v-if="!isLoading && sortedAlerts.length" class="flex items-center gap-2 mb-6 flex-wrap">
      <button
        v-for="f in filters"
        :key="f.value"
        @click="activeFilter = f.value"
        :class="[
          'px-3.5 py-1.5 rounded-xl text-[12px] font-semibold transition-all',
          activeFilter === f.value
            ? 'bg-[#013b28] text-white'
            : 'bg-white text-gray-500 border border-gray-200 hover:border-gray-400'
        ]"
      >
        {{ f.label }}
        <span v-if="f.value !== 'ALL'" class="ml-1 opacity-60">{{ alertCountBy(f.value) }}</span>
      </button>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <i class="bx bx-loader-alt animate-spin text-3xl"></i>
      <p class="text-[13px]">Chargement des alertes...</p>
    </div>

    <!-- ===== LISTE ALERTES ===== -->
    <div v-else-if="filteredAlerts.length" class="space-y-3">
      <div
        v-for="(alert, idx) in filteredAlerts"
        :key="`${alert.type}-${alert.date}-${idx}`"
        :class="[
          'bg-white rounded-2xl p-5 shadow-sm border-l-4 transition-all hover:shadow-md',
          getSeverityBorder(alert.severity)
        ]"
      >
        <div class="flex items-start gap-4">
          <!-- Icône -->
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-lg', getSeverityIconBg(alert.severity)]">
            <i :class="['bx', getAlertIcon(alert.type)]"></i>
          </div>

          <!-- Contenu -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-3 mb-1">
              <h4 class="text-[14px] font-semibold text-gray-900">{{ getAlertTitle(alert.type) }}</h4>
              <div class="flex items-center gap-2 flex-shrink-0">
                <span :class="['text-[9px] font-bold text-white px-2 py-0.5 rounded uppercase tracking-wider', getSeverityBadge(alert.severity)]">
                  {{ alert.severity }}
                </span>
                <span v-if="alert.date" class="text-[11px] text-gray-400 font-medium whitespace-nowrap">
                  {{ formatAlertDate(alert.date) }}
                </span>
              </div>
            </div>
            <p class="text-[13px] text-gray-500 leading-relaxed mb-2">{{ alert.message }}</p>
            <div v-if="alert.action" class="flex items-center gap-1.5 text-[11.5px] text-emerald-700 font-medium">
              <i class="bx bx-bulb text-emerald-600 flex-shrink-0"></i>
              <span>{{ alert.action }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== ÉTAT VIDE ===== -->
    <div v-else-if="!isLoading" class="flex flex-col items-center justify-center py-24 text-center">
      <div class="w-16 h-16 bg-emerald-50 rounded-full flex items-center justify-center mb-5">
        <i class="bx bx-check-shield text-3xl text-emerald-500"></i>
      </div>
      <h3 class="text-[16px] font-semibold text-gray-900 mb-2">Aucune alerte enregistrée</h3>
      <p class="text-[13px] text-gray-400 max-w-xs leading-relaxed">
        {{ activeFilter !== 'ALL' ? 'Aucune alerte pour ce niveau de sévérité.' : 'Cette parcelle ne présente aucune alerte active ou passée.' }}
      </p>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" })

import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"

const route  = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()
const { locale } = useI18n()

// ===== STATE =====
const isLoading  = ref(true)
const parcelName = ref("")
const rawAlerts  = ref<any[]>([])
const activeFilter = ref<string>("ALL")

const filters = [
  { label: "Toutes",    value: "ALL"      },
  { label: "Critique",  value: "CRITICAL" },
  { label: "Élevée",    value: "HIGH"     },
  { label: "Moyenne",   value: "MEDIUM"   },
  { label: "Faible",    value: "LOW"      },
]

// ===== COMPUTED =====
const sortedAlerts = computed(() =>
  [...rawAlerts.value].sort((a, b) => {
    // Tri : d'abord par date (plus récent en premier), puis sévérité
    const dateA = a.date ? new Date(a.date).getTime() : 0
    const dateB = b.date ? new Date(b.date).getTime() : 0
    if (dateB !== dateA) return dateB - dateA
    const sevOrder: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 }
    return (sevOrder[a.severity] ?? 4) - (sevOrder[b.severity] ?? 4)
  })
)

const filteredAlerts = computed(() =>
  activeFilter.value === "ALL"
    ? sortedAlerts.value
    : sortedAlerts.value.filter(a => a.severity === activeFilter.value)
)

const alertStats = computed(() => {
  const all = sortedAlerts.value
  return [
    { label: "Total",    count: all.length,                                          icon: "bx-bell",         iconBg: "bg-gray-50 text-gray-500"    },
    { label: "Critique", count: all.filter(a => a.severity === "CRITICAL").length,   icon: "bxs-error",       iconBg: "bg-red-50 text-red-500"      },
    { label: "Élevée",   count: all.filter(a => a.severity === "HIGH").length,       icon: "bx-error-circle", iconBg: "bg-orange-50 text-orange-500" },
    { label: "Moyenne",  count: all.filter(a => a.severity === "MEDIUM").length,     icon: "bx-info-circle",  iconBg: "bg-amber-50 text-amber-500"  },
  ]
})

function alertCountBy(severity: string) {
  return sortedAlerts.value.filter(a => a.severity === severity).length
}

// ===== HELPERS =====
function formatAlertDate(dateStr: string) {
  if (!dateStr) return ""
  try {
    const d = new Date(dateStr)
    const diffDays = Math.floor((Date.now() - d.getTime()) / 86400000)
    if (diffDays === 0) return "Aujourd'hui"
    if (diffDays === 1) return "Hier"
    if (diffDays < 7)   return `il y a ${diffDays} jours`
    return d.toLocaleDateString(locale.value === "fr" ? "fr-FR" : "en-GB", { day: "2-digit", month: "short", year: "numeric" })
  } catch { return dateStr }
}

function getAlertIcon(type: string) {
  const t = (type || "").toLowerCase()
  if (t.includes("feu") || t.includes("fire"))             return "bxs-flame text-red-500"
  if (t.includes("pluie") || t.includes("rain") || t.includes("heavy_rain")) return "bx-cloud-rain text-blue-500"
  if (t.includes("gel") || t.includes("frost"))            return "bx-snowflake text-sky-400"
  if (t.includes("vent") || t.includes("wind"))            return "bx-wind text-blue-400"
  if (t.includes("humidité") || t.includes("humidity"))    return "bx-water text-teal-400"
  if (t.includes("sécheresse") || t.includes("drought") || t.includes("stress")) return "bx-sun text-amber-600"
  if (t.includes("tâche") || t.includes("task"))           return "bx-time-five text-amber-500"
  if (t.includes("ph") || t.includes("acide"))             return "bx-vial text-emerald-500"
  if (t.includes("azote") || t.includes("nitrogen"))       return "bx-leaf text-emerald-600"
  return "bx-error-circle text-gray-400"
}

function getAlertTitle(type: string) {
  const map: Record<string, string> = {
    "DROUGHT_RISK":  "Stress hydrique",
    "HEAVY_RAIN":    "Pluies intenses",
    "FROST_RISK":    "Risque de gel",
    "STRONG_WIND":   "Vent fort",
    "HIGH_HUMIDITY": "Humidité élevée",
  }
  const clean = type.replace(/^[⌀-➿\uD83C-􏰀-\uDFFF -㋿⏰🔔🧪🌱🔥🌧️❄️💨💧🌵]+\s*/, "")
  return map[type] ?? (clean || type)
}

function getSeverityBorder(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "border-red-500"
  if (s === "HIGH")     return "border-orange-400"
  if (s === "MEDIUM")   return "border-amber-400"
  return "border-blue-300"
}

function getSeverityIconBg(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "bg-red-50 text-red-500"
  if (s === "HIGH")     return "bg-orange-50 text-orange-500"
  if (s === "MEDIUM")   return "bg-amber-50 text-amber-500"
  return "bg-blue-50 text-blue-500"
}

function getSeverityBadge(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "bg-red-600"
  if (s === "HIGH")     return "bg-orange-500"
  if (s === "MEDIUM")   return "bg-amber-500"
  return "bg-blue-500"
}

// ===== INIT =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")
  try {
    const data: any = await apiFetch(`/api/parcels/${route.params.id}/full_data/`)
    parcelName.value = data?.parcel?.name || data?.parcel?.parcel_name || "Parcelle"
    const alerts: any[] = data?.weather_data?.alerts ?? []
    rawAlerts.value = alerts
  } catch (e) {
    console.error("Erreur chargement alertes:", e)
  } finally {
    isLoading.value = false
  }
})
</script>