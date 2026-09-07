<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen font-sans">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Données d'irrigation FAO-56">
      <template #subtitle>
        <i class="bx bx-water text-emerald-600"></i>
        Besoins en eau et suivi de santé du {{ faoData?.crop?.name || 'Riz' }}
      </template>

      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">
          Parcelles
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink :to="`/farmer/parcels/crops/show/${cropId}`" class="hover:text-[#10b481] transition-colors">
          {{ faoData?.crop?.name || cropData?.crop?.name || 'Plantation' }}
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Irrigation FAO-56</span>
      </template>
    </PageHeader>

    <!-- ===== TOP BAR ACTIONS ===== -->
    <div class="flex items-center justify-between gap-4 mb-6">
      <button
        @click="goBack"
        class="p-2.5 bg-white border border-gray-200 rounded-xl text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-all shadow-sm"
        title="Retour aux détails"
      >
        <i class="bx bx-arrow-back text-lg"></i>
      </button>

      <button
        @click="refreshData"
        :disabled="pending"
        class="flex items-center gap-2 px-4 py-2.5 bg-white border border-gray-200 text-gray-700 rounded-xl text-[13px] font-medium hover:bg-gray-50 transition-colors shadow-sm disabled:opacity-50"
      >
        <i class="bx bx-refresh text-base" :class="{ 'animate-spin': pending }"></i>
        {{ pending ? 'Calcul en cours...' : 'Recalculer' }}
      </button>
    </div>

    <!-- ===== ETAT DE CHARGEMENT ===== -->
    <div
      v-if="pending"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 flex flex-col items-center justify-center text-gray-400"
    >
      <i class="bx bx-loader-alt animate-spin text-3xl mb-2 text-emerald-600"></i>
      <span class="text-[13px]">Calcul des métriques FAO-56 en cours...</span>
    </div>

    <!-- ===== ETAT D'ERREUR ===== -->
    <div
      v-else-if="error"
      class="bg-rose-50 border border-rose-100 rounded-2xl p-6 text-rose-600 flex items-center gap-3"
    >
      <i class="bx bx-error-circle text-2xl"></i>
      <div>
        <p class="font-semibold text-[14px]">Erreur de calcul FAO-56</p>
        <p class="text-[12px] opacity-80">Impossible de récupérer les métriques d'irrigation pour cette culture.</p>
        <p v-if="error.message" class="text-[11px] mt-1 opacity-70">{{ error.message }}</p>
      </div>
    </div>

    <!-- ===== CONTENU PRINCIPAL ===== -->
    <div v-else-if="faoData && faoData.data?.length" class="space-y-6">

      <!-- ===== CARDS DE METRIQUES ===== -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1">Soif du Climat (ETo)</p>
            <p class="text-[22px] font-bold text-gray-900">
              {{ latestRecord?.et0_fao_evapotranspiration?.toFixed(2) ?? '—' }}
              <span class="text-[12px] font-normal text-gray-400">mm/j</span>
            </p>
          </div>
          <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center text-blue-500">
            <i class="bx bx-sun text-xl"></i>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1">Eau Absorbée (ETc adj)</p>
            <p class="text-[22px] font-bold text-emerald-600">
              {{ latestRecord?.etc_adj?.toFixed(2) ?? '—' }}
              <span class="text-[12px] font-normal text-gray-400">mm/j</span>
            </p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
            <i class="bx bx-droplet text-xl"></i>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1">Manque d'eau Sol (Dr)</p>
            <p class="text-[22px] font-bold text-amber-600">
              {{ latestRecord?.depletion?.toFixed(1) ?? '—' }}
              <span class="text-[12px] font-normal text-gray-400">mm</span>
            </p>
          </div>
          <div class="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center text-amber-600">
            <i class="bx bx-layer text-xl"></i>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-1">Niveau de Forme (Ks)</p>
            <p class="text-[22px] font-bold" :class="latestRecord && latestRecord.ks < 0.8 ? 'text-rose-600' : 'text-emerald-600'">
              {{ latestRecord?.ks ? (latestRecord.ks * 100).toFixed(0) : '—' }}
              <span class="text-[12px] font-normal text-gray-400">%</span>
            </p>
          </div>
          <div class="w-10 h-10 bg-purple-50 rounded-xl flex items-center justify-center text-purple-600">
            <i class="bx bx-heart-circle text-xl"></i>
          </div>
        </div>
      </div>

      <!-- ===== GRAPHIQUES (GRID 2x2) ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Graph 1: Réservoir & Pluie -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <h4 class="text-[14px] font-bold text-gray-800 mb-1 flex items-center gap-2">
            <i class="bx bx-water text-amber-500"></i> 1. Réserve d'eau du sol & Pluie
          </h4>
          <p class="text-[11px] text-gray-400 mb-4">Évolution du manque d'eau (mm) face aux précipitations</p>
          <div class="relative h-[260px] w-full">
            <canvas ref="chartDepletionCanvas"></canvas>
          </div>
        </div>

        <!-- Graph 2: Stress de la plante -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <h4 class="text-[14px] font-bold text-gray-800 mb-1 flex items-center gap-2">
            <i class="bx bx-pulse text-rose-500"></i> 2. Forme et Stress Hydrique (Ks)
          </h4>
          <p class="text-[11px] text-gray-400 mb-4">Capacité de la plante à s'alimenter (100% = parfait, &lt;80% = stress)</p>
          <div class="relative h-[260px] w-full">
            <canvas ref="chartStressCanvas"></canvas>
          </div>
        </div>

        <!-- Graph 3: Demande vs Consommation -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <h4 class="text-[14px] font-bold text-gray-800 mb-1 flex items-center gap-2">
            <i class="bx bx-analyse text-blue-500"></i> 3. Climat (ETo) vs Absorbe Réelle (ETc)
          </h4>
          <p class="text-[11px] text-gray-400 mb-4">Comparaison entre la demande météo et ce que la plante boit</p>
          <div class="relative h-[260px] w-full">
            <canvas ref="chartEtcCanvas"></canvas>
          </div>
        </div>

        <!-- Graph 4: Températures -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
          <h4 class="text-[14px] font-bold text-gray-800 mb-1 flex items-center gap-2">
            <i class="bx bx-thermometer text-orange-500"></i> 4. Températures Min / Max
          </h4>
          <p class="text-[11px] text-gray-400 mb-4">Variation thermique quotidienne sur la parcelle (°C)</p>
          <div class="relative h-[260px] w-full">
            <canvas ref="chartTempCanvas"></canvas>
          </div>
        </div>

      </div>

      <!-- ===== SECTION INTERPRÉTATION POUR AGRICULTEUR ===== -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-4">
        <div class="flex items-center gap-2 border-b border-gray-100 pb-3">
          <i class="bx bx-bulb text-xl text-amber-500"></i>
          <h3 class="text-[16px] font-bold text-gray-900">
            Interprétation & Recommandations Agricoles (Parcelle {{ faoData.parcel?.name }})
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-[13px] text-gray-600">
          
          <div class="p-4 bg-slate-50 rounded-xl space-y-2">
            <p class="font-bold text-gray-800 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-amber-500"></span> État de la réserve du sol
            </p>
            <p>
              Le sol enregistre un déficit d'eau cumulé de <span class="font-semibold text-amber-600">{{ latestRecord?.depletion?.toFixed(1) }} mm</span>. 
              Les précipitations cumulées ({{ totalPrecipitation.toFixed(1) }} mm) n'ont pas permis de recharger la réserve utile du sol face à l'évaporation.
            </p>
          </div>

          <div class="p-4 bg-slate-50 rounded-xl space-y-2">
            <p class="font-bold text-gray-800 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full" :class="latestRecord && latestRecord.ks < 0.8 ? 'bg-rose-500' : 'bg-emerald-500'"></span>
              Santé et comportement de la culture
            </p>
            <p>
              Stade actuel : <span class="font-semibold text-gray-800">{{ latestRecord?.stage }}</span>. 
              Le niveau de forme de la plante est estimé à <span class="font-semibold" :class="latestRecord && latestRecord.ks < 0.8 ? 'text-rose-600' : 'text-emerald-600'">{{ (latestRecord?.ks * 100).toFixed(0) }}%</span>. 
              <span v-if="latestRecord && latestRecord.ks < 0.8">La culture subit un stress hydrique : elle ferme ses orifices pour préserver son eau, ce qui ralentit sa croissance.</span>
              <span v-else>La culture absorbe l'eau de manière optimale sans contrainte importante.</span>
            </p>
          </div>

        </div>

        <!-- Alerte / Recommandation finale -->
        <div 
          class="p-4 rounded-xl flex items-start gap-3 border"
          :class="latestRecord && latestRecord.ks < 0.8 ? 'bg-rose-50 border-rose-100 text-rose-800' : 'bg-emerald-50 border-emerald-100 text-emerald-800'"
        >
          <i class="bx text-2xl" :class="latestRecord && latestRecord.ks < 0.8 ? 'bx-error-circle text-rose-600' : 'bx-check-circle text-emerald-600'"></i>
          <div>
            <p class="font-bold text-[14px]">
              {{ latestRecord && latestRecord.ks < 0.8 ? 'Action recommandée : Irrigation requise' : 'Situation sous contrôle' }}
            </p>
            <p class="text-[12px] mt-0.5 opacity-90">
              {{ latestRecord && latestRecord.ks < 0.8 
                ? `Il est conseillé d'apporter environ ${latestRecord?.depletion?.toFixed(0)} mm d'eau par irrigation pour annuler le déficit et rétablir le confort optimal de la culture.` 
                : 'Les apports en eau actuels sont suffisants pour couvrir la demande d\'évapotranspiration.' 
              }}
            </p>
          </div>
        </div>

      </div>

    </div>

    <!-- ===== DONNÉES ABSENTES ===== -->
    <div v-else class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 flex flex-col items-center justify-center text-gray-400">
      <i class="bx bx-data text-4xl mb-3"></i>
      <p class="text-[13px]">Aucune donnée FAO-56 disponible.</p>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useApi } from "~/composables/useApi"
import { Chart, registerables } from "chart.js"

Chart.register(...registerables)

definePageMeta({ layout: "dashboard" })

const route = useRoute()
const router = useRouter()
const { apiFetch } = useApi()

const cropId = route.params.id

interface DailyFaoData {
  day_since_start: number
  depletion: number
  et0_fao_evapotranspiration: number
  etc_adj: number
  etc_daily: number
  kc: number
  ks: number
  precipitation_sum: number
  stage: string
  status: string
  temperature_2m_max: number
  temperature_2m_min: number
  time: string
}

interface FaoApiResponse {
  success: boolean
  parcel_crop_id: number
  parcel: { uuid: string; name: string }
  crop: { id: number; name: string; fao56_name: string }
  location: { lat: number; long: number }
  start_date: string
  irrigation: boolean
  irrigation_count: number
  data: DailyFaoData[]
}

interface CropData {
  crop?: { name?: string }
}

// Canvas References
const chartDepletionCanvas = ref<HTMLCanvasElement | null>(null)
const chartStressCanvas = ref<HTMLCanvasElement | null>(null)
const chartEtcCanvas = ref<HTMLCanvasElement | null>(null)
const chartTempCanvas = ref<HTMLCanvasElement | null>(null)

// Chart Instances
let chartDepletion: Chart | null = null
let chartStress: Chart | null = null
let chartEtc: Chart | null = null
let chartTemp: Chart | null = null

// Fetch Crop metadata
const { data: cropData } = await useAsyncData<CropData | null>(
  `crop-info-${cropId}`,
  () => apiFetch<CropData>(`/parcel-crops/${cropId}/`)
)

// Fetch FAO-56 metrics
const {
  data: faoData,
  pending,
  error,
  refresh: refreshData,
} = await useAsyncData<FaoApiResponse | null>(
  `fao56-${cropId}`,
  async () => {
    return await apiFetch<FaoApiResponse>(`/api/parcel-crops/${cropId}/fao56/`, {
      method: "POST",
      body: { irrigation: true, irrigation_count: 10 },
    })
  }
)

// Computeds
const latestRecord = computed(() => {
  if (!faoData.value?.data?.length) return null
  return faoData.value.data[faoData.value.data.length - 1]
})

const totalPrecipitation = computed(() => {
  if (!faoData.value?.data) return 0
  return faoData.value.data.reduce((acc, curr) => acc + (curr.precipitation_sum || 0), 0)
})

// Function to destroy previous chart instances
function destroyCharts() {
  if (chartDepletion) chartDepletion.destroy()
  if (chartStress) chartStress.destroy()
  if (chartEtc) chartEtc.destroy()
  if (chartTemp) chartTemp.destroy()
}

// Render all 4 charts
function renderCharts() {
  if (!faoData.value?.data) return
  destroyCharts()

  const labels = faoData.value.data.map((d) => {
    const date = new Date(d.time)
    return `${date.getDate()}/${date.getMonth() + 1}`
  })

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'top' as const, labels: { boxWidth: 12, font: { size: 11 } } }
    },
    scales: {
      x: { grid: { display: false }, ticks: { font: { size: 10 } } },
      y: { grid: { color: "#f1f5f9" }, ticks: { font: { size: 10 } } }
    }
  }

  // 1. Graphique Epuisement vs Pluie
  if (chartDepletionCanvas.value) {
    chartDepletion = new Chart(chartDepletionCanvas.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            type: 'bar',
            label: 'Pluie (mm)',
            data: faoData.value.data.map(d => d.precipitation_sum),
            backgroundColor: '#0284c7',
            yAxisID: 'y1'
          },
          {
            type: 'line',
            label: 'Manque d\'eau (mm)',
            data: faoData.value.data.map(d => d.depletion),
            borderColor: '#d97706',
            backgroundColor: '#d97706',
            borderWidth: 2,
            pointRadius: 2,
            yAxisID: 'y'
          }
        ]
      },
      options: {
        ...commonOptions,
        scales: {
          ...commonOptions.scales,
          y1: { position: 'right', grid: { display: false }, title: { display: true, text: 'Pluie mm' } }
        }
      }
    })
  }

  // 2. Graphique Stress Plante (Ks)
  if (chartStressCanvas.value) {
    chartStress = new Chart(chartStressCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Forme du riz (%)',
            data: faoData.value.data.map(d => d.ks * 100),
            borderColor: '#dc2626',
            backgroundColor: 'rgba(220, 38, 38, 0.1)',
            fill: true,
            tension: 0.2,
            pointRadius: 3
          }
        ]
      },
      options: {
        ...commonOptions,
        scales: {
          x: commonOptions.scales.x,
          y: { min: 40, max: 105, grid: { color: "#f1f5f9" }, title: { display: true, text: 'Forme (%)' } }
        }
      }
    })
  }

  // 3. Graphique Climat vs Consommation (ETo vs ETc adj)
  if (chartEtcCanvas.value) {
    chartEtc = new Chart(chartEtcCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Soif climat (ETo)',
            data: faoData.value.data.map(d => d.et0_fao_evapotranspiration),
            borderColor: '#2563eb',
            backgroundColor: '#2563eb',
            tension: 0.2,
            pointRadius: 2
          },
          {
            label: 'Absorbe réelle (ETc)',
            data: faoData.value.data.map(d => d.etc_adj),
            borderColor: '#16a34a',
            backgroundColor: '#16a34a',
            tension: 0.2,
            pointRadius: 2
          }
        ]
      },
      options: commonOptions
    })
  }

  // 4. Graphique Températures Min / Max
  if (chartTempCanvas.value) {
    chartTemp = new Chart(chartTempCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Temp. Max (°C)',
            data: faoData.value.data.map(d => d.temperature_2m_max),
            borderColor: '#ea580c',
            backgroundColor: '#ea580c',
            tension: 0.2,
            pointRadius: 2
          },
          {
            label: 'Temp. Min (°C)',
            data: faoData.value.data.map(d => d.temperature_2m_min),
            borderColor: '#0284c7',
            backgroundColor: '#0284c7',
            tension: 0.2,
            pointRadius: 2
          }
        ]
      },
      options: commonOptions
    })
  }
}

watch(
  () => faoData.value,
  async () => {
    await nextTick()
    renderCharts()
  },
  { deep: true }
)

onMounted(async () => {
  await nextTick()
  renderCharts()
})

function goBack() {
  router.push(`/farmer/parcels/crops/show/${cropId}`)
}
</script>