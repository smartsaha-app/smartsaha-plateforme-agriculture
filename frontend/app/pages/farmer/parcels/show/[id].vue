<template>
  <div class="p-6 space-y-8 text-[#112830] min-h-screen">
    
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">
            {{ t("parcels") }}
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481]">{{ t("details") }}</span>
        </nav>
        <div class="flex items-center gap-4">
          <h1 class="text-4xl font-black tracking-tighter">{{ parcelData.name || "Détails Parcelle" }}</h1>
          <span class="px-3 py-1 bg-emerald-50 text-[#10b481] text-[10px] font-black uppercase tracking-widest rounded-full border border-emerald-100">Actif</span>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <NuxtLink
          :to="`/farmer/parcels/edit/${id}`"
          class="flex items-center gap-2 px-6 py-3 bg-white border border-gray-100 rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-gray-50 transition-all shadow-sm"
        >
          <i class="bx bx-edit text-lg"></i>
          {{ t("edit") }}
        </NuxtLink>
        <button class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg">
          <i class="bx bx-share-alt text-lg"></i>
          Partager
        </button>
      </div>
    </div>

    <!-- ===== TOP GRID: WEATHER & QUICK METRICS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Weather Dashboard (8/12) -->
      <div v-if="currentWeather" class="lg:col-span-8 bg-gradient-to-br from-[#112830] to-[#1a3d4a] rounded-[3rem] p-10 text-white shadow-2xl relative overflow-hidden group">
        <!-- Background Decoration -->
        <div class="absolute -right-20 -top-20 w-80 h-80 bg-white/5 rounded-full blur-3xl group-hover:bg-white/10 transition-colors duration-700"></div>
        
        <div class="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-12 h-full">
          <!-- Current Weather -->
          <div class="flex flex-col justify-between">
            <div class="space-y-1">
              <p class="text-[10px] font-black uppercase tracking-[0.2em] text-[#10b481]">{{ getDayName(todayForecast.date) }} <span class="text-white/40 ml-2">{{ currentTime }}</span></p>
              <h2 class="text-7xl font-black tracking-tighter flex items-start">
                {{ Math.round(currentWeather.temp_c) }}<span class="text-3xl mt-2 text-[#10b481]">°C</span>
              </h2>
              <p class="text-xs font-bold text-white/60 capitalize">{{ translatedCurrentCondition || currentWeather.condition?.text }}</p>
            </div>

            <div class="grid grid-cols-2 gap-6 mt-8">
              <div class="space-y-1">
                <p class="text-[8px] font-black uppercase text-white/40 tracking-widest">{{ t("humidity") }}</p>
                <p class="text-sm font-bold">{{ currentWeather.humidity }}%</p>
              </div>
              <div class="space-y-1">
                <p class="text-[8px] font-black uppercase text-white/40 tracking-widest">{{ t("vent") }}</p>
                <p class="text-sm font-bold">{{ currentWeather.wind_kph }} km/h</p>
              </div>
            </div>
          </div>

          <!-- 3-Day Forecast -->
          <div class="bg-white/5 backdrop-blur-md rounded-[2.5rem] p-8 border border-white/10 flex flex-col justify-between">
            <p class="text-[10px] font-black uppercase tracking-[0.2em] mb-6 text-center text-white/60">Prévisions 3 jours</p>
            <div class="flex justify-between gap-4">
              <div v-for="day in forecastDays" :key="day.date" class="flex-1 flex flex-col items-center gap-3 group/day">
                <p class="text-[10px] font-black uppercase text-white/40 group-hover/day:text-[#10b481] transition-colors">{{ getDayNameShort(day.date) }}</p>
                <span class="text-4xl filter drop-shadow-md group-hover/day:scale-125 transition-transform duration-500">{{ getWeatherIcon(day.day?.condition?.text) }}</span>
                <div class="text-center">
                  <p class="text-xs font-black">{{ Math.round(day.day?.maxtemp_c) }}°</p>
                  <p class="text-[9px] font-bold text-white/30">{{ day.day?.daily_chance_of_rain }}%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Surface & Owner (4/12) -->
      <div class="lg:col-span-4 grid grid-cols-1 gap-8">
        <div class="bg-white p-8 rounded-[3rem] border border-gray-100 shadow-sm flex flex-col justify-center items-center text-center space-y-2 hover:shadow-lg transition-all border-b-8 border-b-[#10b481]">
          <div class="w-16 h-16 bg-emerald-50 rounded-2xl flex items-center justify-center text-[#10b481] text-3xl mb-2">
            <i class="bx bx-area"></i>
          </div>
          <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest">{{ t("Area") }}</p>
          <p class="text-4xl font-black tracking-tighter">{{ formatM2(parcelAreaHa) }}</p>
          <p class="text-[10px] font-bold text-gray-300">{{ (Number(parcelAreaHa)).toFixed(2) }} Hectares</p>
        </div>

        <div class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm flex items-center gap-5 hover:bg-gray-50 transition-colors">
          <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center text-gray-400 text-2xl border border-gray-50 flex-shrink-0">
            <i class="bx bx-user"></i>
          </div>
          <div class="flex-1 overflow-hidden">
            <p class="text-[9px] font-black uppercase text-gray-400 tracking-widest">{{ t("owner") }}</p>
            <p class="font-bold text-[#112830] truncate">{{ ownerData.first_name }} {{ ownerData.last_name }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== MIDDLE GRID: MAP & ANALYTICS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Interactive Map & Data Tabs (8/12) -->
      <div class="lg:col-span-8 bg-white rounded-[3.5rem] border border-gray-100 shadow-sm overflow-hidden flex flex-col h-[600px]">
        <!-- Map Navigation Tabs -->
        <div class="px-10 py-6 border-b border-gray-50 flex items-center justify-between">
          <div class="flex items-center gap-8">
            <button @click="selectedTab = 'points'" :class="['text-[10px] font-black uppercase tracking-widest transition-all pb-1 border-b-2', selectedTab === 'points' ? 'text-[#10b481] border-[#10b481]' : 'text-gray-300 border-transparent hover:text-[#112830]']">
              Points GPS
            </button>
            <button @click="selectedTab = 'crops'" :class="['text-[10px] font-black uppercase tracking-widest transition-all pb-1 border-b-2', selectedTab === 'crops' ? 'text-[#10b481] border-[#10b481]' : 'text-gray-300 border-transparent hover:text-[#112830]']">
              Cultures assignées
            </button>
          </div>
          <div class="flex items-center gap-2">
            <i class="bx bx-current-location text-[#10b481] text-lg"></i>
            <span class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Temps réel</span>
          </div>
        </div>

        <div class="flex-1 relative flex">
          <!-- Sidebar Info Panel (Optional/Conditional) -->
          <div class="w-1/3 border-r border-gray-50 p-6 overflow-y-auto scrollbar-hidden bg-gray-50/30">
            <div v-if="selectedTab === 'points'" class="space-y-4">
              <div v-for="(p, i) in parcelPoints" :key="i" class="p-4 bg-white rounded-2xl border border-gray-100 shadow-sm hover:translate-x-1 transition-transform group">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-[8px] font-black px-2 py-0.5 bg-[#112830] text-white rounded-md tracking-widest">POINT {{ i+1 }}</span>
                  <i class="bx bx-target-lock text-gray-200 group-hover:text-[#10b481] transition-colors"></i>
                </div>
                <p class="font-mono text-[10px] text-gray-400">{{ p.lat.toFixed(6) }}, {{ p.lng.toFixed(6) }}</p>
              </div>
            </div>
            <div v-else class="space-y-4">
              <div v-for="crop in parcelCropsFromFullData" :key="crop.parcel_crop_id" class="p-5 bg-white rounded-[2rem] border border-gray-100 shadow-sm flex items-center gap-4">
                <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center text-[#10b481]">
                  <i class="bx bx-leaf text-xl"></i>
                </div>
                <div>
                  <p class="text-[10px] font-black uppercase tracking-tighter">{{ crop.crop?.name }}</p>
                  <p class="text-[10px] font-bold text-gray-300">{{ crop.area }} m²</p>
                </div>
              </div>
            </div>
          </div>
          <!-- The Actual Map -->
          <div id="map" class="flex-1 bg-gray-100"></div>
        </div>
      </div>

      <!-- Soil & Analytics Side (4/12) -->
      <div class="lg:col-span-4 space-y-8 flex flex-col justify-start">
        <!-- Yield Analytics -->
        <div v-if="selectedParcel" class="bg-[#112830] rounded-[3rem] p-8 text-white space-y-8 shadow-xl">
          <div class="flex items-center justify-between border-b border-white/10 pb-6">
            <p class="text-[10px] font-black uppercase tracking-widest text-[#10b481]">{{ t("titleanalytics") }}</p>
            <i class="bx bx-line-chart text-2xl text-[#10b481]"></i>
          </div>
          <div class="space-y-6">
            <div class="flex items-end justify-between">
              <div class="space-y-1">
                <p class="text-[8px] font-black uppercase text-white/40 tracking-[0.2em]">{{ t("meanyield") }}</p>
                <p class="text-4xl font-black tracking-tighter">{{ selectedParcel.mean_yield?.toFixed(2) }} <span class="text-lg text-white/30">kg</span></p>
              </div>
              <div class="flex flex-col items-center">
                <div class="h-10 w-1.5 bg-white/10 rounded-full overflow-hidden mb-2">
                  <div class="h-2/3 w-full bg-[#10b481]"></div>
                </div>
                <span class="text-[8px] font-black uppercase text-white/30">Max</span>
              </div>
            </div>
            <div class="bg-white/5 rounded-2xl p-5 border border-white/10 flex items-center justify-between">
              <p class="text-[9px] font-bold text-white/60 tracking-widest lowercase">{{ t("meanyieldperarea") }}</p>
              <p class="text-xl font-black">{{ selectedParcel.mean_yield_per_area?.toFixed(1) }} <span class="text-[10px] text-white/30">kg/ha</span></p>
            </div>
          </div>
        </div>

        <!-- Soil Quality Card -->
        <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 space-y-6">
          <div class="flex items-center justify-between">
            <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("soilinfo") }}</p>
            <div class="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center border border-gray-100">
               <i class="bx bxs-vial text-lg text-[#10b481]"></i>
            </div>
          </div>
          <div class="space-y-3">
             <div
              v-for="(quality, index) in soilQualities"
              :key="index"
              class="p-4 rounded-2xl flex justify-between items-center group transition-all"
              :style="{ 
                background: `linear-gradient(to right, ${colorMap[quality.name]}10, #ffffff)`,
                borderLeft: `3px solid ${colorMap[quality.name]}`
              }"
            >
              <div class="space-y-0.5">
                <p class="text-[10px] font-bold text-[#112830]">{{ quality.name }}</p>
                <p class="text-[8px] font-black uppercase text-gray-400 tracking-tighter">{{ quality.unit }}</p>
              </div>
              <p class="text-xl font-black tracking-tighter group-hover:scale-110 transition-transform" :style="{ color: colorMap[quality.name] }">{{ quality.value }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== BOTTOM GRID: TASKS & CHARTS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Task Performance (4/12) -->
      <div class="lg:col-span-4 bg-white rounded-[3rem] border border-gray-100 shadow-sm p-10 flex flex-col items-center justify-center">
        <h3 class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-8 self-start">{{ t("charttitletask") }}</h3>
        <div class="w-full relative aspect-square">
          <canvas id="taskPerformanceChart"></canvas>
          <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
             <p class="text-5xl font-black tracking-tighter">{{ nearestTasks.length }}</p>
             <p class="text-[8px] font-black uppercase text-gray-400">Total Tâches</p>
          </div>
        </div>
      </div>

      <!-- Nearest Tasks List (8/12) -->
      <div class="lg:col-span-8 bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden flex flex-col">
        <div class="px-10 py-8 border-b border-gray-50 flex items-center justify-between">
          <div class="space-y-1">
            <h3 class="text-lg font-black tracking-tighter">{{ t("titletaskperform") }}</h3>
            <p class="text-[10px] font-medium text-gray-400">Suivi opérationnel en cours</p>
          </div>
          <NuxtLink to="/tasks/create" class="px-6 py-2 bg-emerald-50 text-[#10b481] rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#10b481] hover:text-white transition-all">
            {{ t("addtask") }}
          </NuxtLink>
        </div>
        <div class="flex-1 p-6 space-y-4">
          <div
            v-for="task in nearestTasks"
            :key="task.id"
            class="group p-6 bg-gray-50/50 rounded-[2.5rem] border border-gray-100 flex items-center gap-6 hover:bg-white hover:shadow-xl hover:-translate-y-1 transition-all duration-500"
          >
            <div :class="['w-16 h-16 rounded-[1.5rem] flex items-center justify-center text-2xl shadow-sm transition-transform group-hover:scale-110', 
              task.priority === 'High' ? 'bg-rose-50 text-rose-500 border border-rose-100' :
              task.priority === 'Medium' ? 'bg-amber-50 text-amber-500 border border-amber-100' :
                                           'bg-emerald-50 text-[#10b481] border border-emerald-100']">
              <i class="bx bx-task"></i>
            </div>
            <div class="flex-1">
              <h4 class="font-black text-[#112830] text-lg tracking-tight mb-1">{{ task.name }}</h4>
              <div class="flex items-center gap-4">
                <span class="text-[9px] font-black uppercase tracking-widest text-gray-300 flex items-center gap-1">
                  <i class="bx bx-calendar text-sm"></i> {{ formatDate(task.due_date) }}
                </span>
                <span class="w-1.5 h-1.5 bg-gray-200 rounded-full"></span>
                <span :class="['text-[9px] font-black uppercase tracking-widest', 
                  task.priority === 'High' ? 'text-rose-400' : task.priority === 'Medium' ? 'text-amber-400' : 'text-emerald-400']">
                  {{ t("priority" + task.priority) }}
                </span>
              </div>
            </div>
            <div class="flex flex-col items-end gap-3">
               <span :class="['px-4 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border border-white shadow-sm', 
                  task.status === 'Pending' ? 'bg-gray-100 text-gray-400' :
                  task.status === 'Done' ? 'bg-emerald-500 text-white' :
                                           'bg-[#112830] text-white']">
                {{ t("status" + task.status.replace(/ /g, "")) }}
              </span>
              <NuxtLink :to="`/tasks/show/${task.id}`" class="text-[10px] font-black text-gray-300 hover:text-[#112830] transition-colors">Détails <i class="bx bx-right-arrow-alt"></i></NuxtLink>
            </div>
          </div>
          <div v-if="!nearestTasks.length" class="p-20 text-center space-y-4">
             <i class="bx bx-list-check text-6xl text-gray-100"></i>
             <p class="text-[10px] font-black uppercase tracking-widest text-gray-300 italic">Aucune tâche planifiée</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== EVOLUTION CHART & HARVEST HISTORY ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
      
      <!-- Yield Evolution Chart (8/12) -->
      <div class="lg:col-span-8 bg-[#112830] rounded-[3.5rem] p-10 shadow-xl overflow-hidden group">
        <div class="flex items-center justify-between mb-10 decoration-white/10 decoration-wavy">
          <div class="space-y-1">
            <h3 class="text-lg font-black tracking-tighter text-white">{{ t("charttitleyield") }}</h3>
            <p class="text-[10px] font-medium text-white/40">Progression pluriannuelle</p>
          </div>
          <div class="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-xl border border-white/5">
            <span class="w-2 h-2 bg-[#10b481] rounded-full"></span>
            <span class="text-[9px] font-black text-white/60 uppercase tracking-widest">Rendement Actualisé</span>
          </div>
        </div>
        <div class="h-[400px] w-full">
           <canvas id="yieldEvolutionChart"></canvas>
        </div>
      </div>

      <!-- Harvest History Table (4/12) -->
      <div class="lg:col-span-4 bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden flex flex-col">
        <div class="px-8 py-8 border-b border-gray-50 flex items-center justify-between">
          <h3 class="text-sm font-black uppercase tracking-widest text-gray-400">{{ t("harvesthistory") }}</h3>
          <button @click="exportCSV" class="text-gray-300 hover:text-[#112830] transition-colors">
            <i class="bx bx-download text-xl"></i>
          </button>
        </div>
        <div class="flex-1 overflow-y-auto scrollbar-hidden">
          <table class="w-full text-left">
            <tbody class="divide-y divide-gray-50 italic">
               <tr v-for="record in paginatedHarvest" :key="record.id" class="group hover:bg-gray-50/50 transition-colors">
                <td class="px-8 py-5">
                  <p class="text-[10px] font-black text-[#112830]">{{ record.date }}</p>
                  <p class="text-[8px] font-bold text-gray-300">Récolte validée</p>
                </td>
                <td class="px-8 py-5 text-right flex flex-col items-end">
                   <div class="flex items-center gap-2">
                     <span class="text-lg font-black text-[#112830]">{{ record.quantity }}</span>
                     <span class="text-[8px] font-black text-gray-300">KG</span>
                   </div>
                   <div :class="['text-[8px] font-black uppercase tracking-widest flex items-center gap-1', 
                    record.trend === 'up' ? 'text-[#10b481]' : record.trend === 'down' ? 'text-rose-500' : 'text-gray-200']">
                     <i :class="['bx', record.trend === 'up' ? 'bx-trending-up' : record.trend === 'down' ? 'bx-trending-down' : 'bx-minus']"></i>
                     {{ record.trend !== 'neutral' ? record.trendValue + ' kg' : '-' }}
                   </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!paginatedHarvest.length" class="p-10 text-center italic text-[10px] text-gray-200 uppercase tracking-[0.2em]">Historique vide</div>
        </div>
        <!-- Pagination Mini -->
        <div v-if="totalPages > 1" class="px-8 py-6 bg-gray-50/50 border-t border-gray-50 flex items-center justify-center gap-4">
           <button @click="prevPage" :disabled="currentPage === 1" class="text-gray-400 disabled:opacity-20 hover:text-[#112830]"><i class="bx bx-chevron-left text-2xl"></i></button>
           <span class="text-[9px] font-black uppercase text-gray-300 tracking-[0.2em]">{{ currentPage }} / {{ totalPages }}</span>
           <button @click="nextPage" :disabled="currentPage === totalPages" class="text-gray-400 disabled:opacity-20 hover:text-[#112830]"><i class="bx bx-chevron-right text-2xl"></i></button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" })

import { reactive, ref, computed, onMounted, onUnmounted, watch, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"
import Chart from "chart.js/auto"

const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const currentLocale = computed(() => locale.value)

const route = useRoute()
const fieldIdParam = route.params.id as string ?? null

// ===== ÉTAT =====
const currentWeather = ref<any>(null)
const forecastDays = ref<any[]>([])
const parcelPoints = ref<any[]>([])
const alerts = ref<any[]>([])
const translatedAlerts = ref<any[]>([])
const metadata = ref<any>({})
const selectedTab = ref("points")
const translatedCurrentCondition = ref("")
const currentTime = ref("")
const parcelFullData = reactive<any>({})
const parcelData = reactive<any>({})
const ownerData = reactive<any>({})
const soilQualities = reactive<any[]>([])
// ✅ FIX: tasks vient de fullData.tasks.tasks (tableau à la racine)
const tasks = ref<any[]>([])
const harvestHistory = ref<any[]>([])
const analyticsData = ref<any[]>([])
const selectedParcel = ref<any>(null)
const parcelCrops = ref<any[]>([])
const paginatedHarvest = ref<any[]>([])
const itemsPerPage = 5
const currentPage = ref(1)

const colorMap: Record<string, string> = {
  nitrogen: "#10b481",
  soc:      "#c99383",
  clay:     "#6d4c41",
  phh2o:    "#5fd4a2",
  sand:     "#f4a261",
  silt:     "#219ebc",
}

// ===== HORLOGE =====
let intervalId: ReturnType<typeof setInterval>

onMounted(() => {
  updateTime()
  intervalId = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})

// ===== MAP INITIALIZATION =====
let L: any;
let map: any;

async function initMap() {
  if (!process.client || map) return;
  
  L = await import("leaflet");
  await import("leaflet/dist/leaflet.css");
  
  const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", { attribution: "Esri" });
  map = L.map("map", {
    center: [-18.8792, 47.5079],
    zoom: 6,
    layers: [satellite],
    zoomControl: false
  });

  if (parcelPoints.value.length >= 3) {
    const latlngs = parcelPoints.value.map(p => [p.lat, p.lng]);
    const poly = L.polygon(latlngs, {
      color: "#10b481",
      fillColor: "#10b481",
      fillOpacity: 0.2,
      weight: 3
    }).addTo(map);
    map.fitBounds(poly.getBounds(), { padding: [40, 40] });
  } else if (parcelPoints.value.length > 0) {
    map.setView([parcelPoints.value[0].lat, parcelPoints.value[0].lng], 15);
  }
}

function updateTime() {
  const now = new Date()
  currentTime.value = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`
}

// ===== MÉTÉO =====
// ✅ FIX: mapping complet depuis la vraie structure API
function updateWeatherForecast(data: any) {
  const weatherData = data?.weather_data?.data
  if (!weatherData) {
    currentWeather.value = null
    forecastDays.value = []
    parcelPoints.value = []
    alerts.value = []
    metadata.value = {}
    return
  }

  // ✅ current est directement weatherData.current (temp_c, wind_kph, humidity, uv, condition.text)
  currentWeather.value = weatherData.current ?? null

  // ✅ forecastday est dans weatherData.forecast.forecastday (pas daily_forecast)
  forecastDays.value = weatherData.forecast?.forecastday ?? []

  parcelPoints.value = data?.parcel?.points ?? []

  const today = new Date().toISOString().split("T")[0]
  alerts.value = (data?.weather_data?.analysis?.alerts ?? []).filter(
    (alert: any) => alert.date === today
  )

  const meta = data?.weather_data?.metadata
  metadata.value = meta ? {
    location:        meta.location_name,
    forecast_period: `${meta.start} → ${meta.end}`,
    risk_level:      meta.risk_level,
  } : {}
}

// ✅ FIX: todayForecast cherche dans forecastday[] qui sont des objets { date, day, hour, astro }
const todayForecast = computed(() => {
  if (!forecastDays.value.length) return null
  const today = new Date().toISOString().split("T")[0]
  return forecastDays.value.find((d: any) => d.date === today) ?? forecastDays.value[0] ?? null
})

function getDayName(dateStr: string) {
  return new Date(dateStr).toLocaleDateString(currentLocale.value, { weekday: "long" })
}

function getDayNameShort(dateStr: string) {
  return new Date(dateStr).toLocaleDateString(currentLocale.value, { weekday: "short" })
}

// Dictionnaire complet des 65 conditions officielles WeatherAPI en français
const weatherIconMap: Record<string, string> = {
  // ☀️ Soleil / Ciel clair
  "Ensoleillé":                               "☀️",
  "Clair":                                    "🌙",

  // ⛅ Partiellement nuageux
  "Partiellement nuageux":                    "⛅",

  // ☁️ Nuageux / Couvert
  "Nuageux":                                  "☁️",
  "Couvert":                                  "☁️",

  // 🌫️ Brume / Brouillard
  "Brume":                                    "🌫️",
  "Brouillard":                               "🌫️",
  "Brouillard givrant":                       "🌫️",

  // 🌦️ Pluie légère / Bruine
  "Pluie éparse à proximité":                 "🌦️",
  "Bruine légère éparse":                     "🌦️",
  "Bruine légère":                            "🌦️",
  "Pluie légère éparse":                      "🌦️",
  "Pluie légère":                             "🌦️",
  "Averses légères":                          "🌦️",

  // 🌧️ Pluie modérée à forte
  "Pluie modérée par moments":                "🌧️",
  "Pluie modérée":                            "🌧️",
  "Pluie forte par moments":                  "🌧️",
  "Pluie forte":                              "🌧️",
  "Averses modérées ou fortes":               "🌧️",
  "Averses torrentielles":                    "🌧️",

  // ❄️ Neige / Verglas / Grésil
  "Neige éparse à proximité":                 "❄️",
  "Grésil épars à proximité":                 "🌨️",
  "Bruine verglaçante éparse à proximité":    "❄️",
  "Rafales de neige":                         "🌨️",
  "Blizzard":                                 "🌨️",
  "Bruine verglaçante":                       "❄️",
  "Forte bruine verglaçante":                 "❄️",
  "Pluie verglaçante légère":                 "❄️",
  "Pluie verglaçante modérée à forte":        "❄️",
  "Léger grésil":                             "🌨️",
  "Grésil modéré à fort":                     "🌨️",
  "Neige légère éparse":                      "❄️",
  "Neige légère":                             "❄️",
  "Neige modérée éparse":                     "❄️",
  "Neige modérée":                            "❄️",
  "Neige forte éparse":                       "❄️",
  "Neige forte":                              "❄️",
  "Averses de grésil léger":                  "🌨️",
  "Averses de grésil modéré ou fort":         "🌨️",
  "Averses de neige légère":                  "❄️",
  "Averses de neige modérée ou forte":        "❄️",

  // ⛈️ Orages / Grêle
  "Foyers orageux à proximité":               "⛈️",
  "Grêle":                                    "⛈️",
  "Averses de grêle légère":                  "⛈️",
  "Averses de grêle modérée ou forte":        "⛈️",
  "Pluie légère éparse avec orages":          "⛈️",
  "Pluie modérée ou forte avec orages":       "⛈️",
  "Neige légère éparse avec orages":          "⛈️",
  "Neige modérée ou forte avec orages":       "⛈️",
}

function getWeatherIcon(condition?: string): string {
  if (!condition) return "🌡️"

  // 1. Correspondance exacte (conditions officielles WeatherAPI FR)
  if (weatherIconMap[condition]) return weatherIconMap[condition]

  // 2. Fallback par mots-clés pour variantes non officielles (ex: "Orage", "Orage avec grêle légère")
  const c = condition.toLowerCase()
  if (c.includes("orage") || c.includes("grêle") || c.includes("tempête")) return "⛈️"
  if (c.includes("neige") || c.includes("grésil") || c.includes("blizzard"))  return "❄️"
  if (c.includes("averse") || c.includes("bruine"))                            return "🌦️"
  if (c.includes("pluie forte") || c.includes("forte pluie"))                 return "🌧️"
  if (c.includes("pluie"))                                                     return "🌧️"
  if (c.includes("brouillard") || c.includes("brume"))                        return "🌫️"
  if (c.includes("partiellement") || c.includes("partly"))                    return "⛅"
  if (c.includes("couvert") || c.includes("nuageux") || c.includes("cloudy")) return "☁️"
  if (c.includes("clair") || c.includes("clear"))                             return "🌙"
  if (c.includes("ensoleillé") || c.includes("sunny") || c.includes("sun"))  return "☀️"

  return "🌡️"
}

// ===== TRADUCTIONS =====
const translationCache = useState("translationCache", () => ({} as Record<string, string>))

const removeEmojis = (text: string) =>
  text.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|[\uD83C-\uDBFF\uDC00-\uDFFF])/g, "")

async function translateText(text: string, sourceLang = "fr") {
  const targetLang = currentLocale.value || "en"
  if (sourceLang === targetLang) return { translated: text, original: text }
  if (translationCache.value[text]) return { translated: translationCache.value[text], original: text }

  try {
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang}|${targetLang}`
    const res = await fetch(url)
    const json = await res.json()
    const translatedText = json?.responseData?.translatedText || text
    translationCache.value[text] = translatedText
    return { translated: translatedText, original: text }
  } catch {
    translationCache.value[text] = text
    return { translated: text, original: text }
  }
}

async function translateAlerts(alertList: any[]) {
  translatedAlerts.value = await Promise.all(
    alertList.map(async (alert) => {
      const messageRes = await translateText(removeEmojis(alert.message))
      const actionRes  = await translateText(removeEmojis(alert.action))
      return {
        ...alert,
        message:         messageRes.translated,
        messageOriginal: messageRes.original,
        action:          actionRes.translated,
        actionOriginal:  actionRes.original,
      }
    })
  )
}

async function translateCurrentWeatherCondition() {
  // ✅ FIX: condition est un objet { text, code, icon } dans l'API WeatherAPI
  const conditionText = currentWeather.value?.condition?.text
  if (conditionText) {
    const res = await translateText(removeEmojis(conditionText))
    translatedCurrentCondition.value = res.translated
    currentWeather.value.conditionOriginal = res.original
  } else {
    translatedCurrentCondition.value = ""
  }
}

watch(alerts, (val) => { if (val.length) translateAlerts(val) })
watch(currentWeather, () => { translateCurrentWeatherCondition() })

// ===== SOL =====
function updateSoilQualities(layers: any[]) {
  if (!layers || !Array.isArray(layers)) return
  soilQualities.length = 0
  layers.forEach((layer) => {
    soilQualities.push({
      name:  layer.name,
      value: layer.depths?.[0]?.values?.mean ?? null,
      unit:  layer.unit_measure?.mapped_units ?? "",
    })
  })
}

// ===== TÂCHES =====
// ✅ FIX: tasks viennent de fullData.tasks.tasks (pas parcel_crops[].tasks)
function updateTasks(fullData: any) {
  tasks.value = fullData.tasks?.tasks ?? []
}

const formatDate = (date: string) =>
  new Date(date).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" })

const nearestTasks = computed(() =>
  [...tasks.value]
    .filter((t) => t.status !== "Cancelled" && t.status !== "Done")
    .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
    .slice(0, 3)
)

// ===== CULTURES depuis fullData =====
// ✅ FIX: parcel_crops est à la racine de fullData avec parcel_crop_id, crop.name, area
const parcelCropsFromFullData = computed(() =>
  Array.isArray(parcelFullData.parcel_crops) ? parcelFullData.parcel_crops : []
)

// ===== GRAPHIQUES =====
let taskChart: Chart | null = null
let yieldChart: Chart | null = null

function updateTaskChart() {
  // ✅ FIX: utilise tasks.value directement
  const statusCount = tasks.value.reduce((acc: Record<string, number>, t) => {
    acc[t.status] = (acc[t.status] || 0) + 1
    return acc
  }, {})

  const ctx = document.getElementById("taskPerformanceChart") as HTMLCanvasElement
  if (!ctx) return
  if (taskChart) taskChart.destroy()

  taskChart = new Chart(ctx.getContext("2d")!, {
    type: "doughnut",
    data: {
      labels: Object.keys(statusCount).map((s) => t(`status${s.replace(/\s+/g, "")}`)),
      datasets: [{
        label: t("chartTasksByStatus"),
        data: Object.values(statusCount),
        backgroundColor: ["#10b481", "#112830", "#f43f5e", "#fbbf24"],
        borderWidth: 0,
        hoverOffset: 10
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "80%",
      plugins: { 
        legend: { display: false } 
      },
    },
  })
}

function updateYieldEvolutionChart() {
  // ✅ FIX: yield_records à la racine de fullData, champ "yield" (pas r.yield → r.yield)
  const records = parcelFullData.yield_records ?? []
  if (!records.length) return

  const grouped: Record<string, number> = {}
  records.forEach((r: any) => {
    const monthYear = new Date(r.date).toLocaleString("default", { month: "short", year: "numeric" })
    grouped[monthYear] = (grouped[monthYear] || 0) + (r.yield ?? 0)
  })

  const labels = Object.keys(grouped).sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
  const data   = labels.map((l) => grouped[l])

  const ctx = document.getElementById("yieldEvolutionChart") as HTMLCanvasElement
  if (!ctx) return
  if (yieldChart) yieldChart.destroy()

  yieldChart = new Chart(ctx.getContext("2d")!, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: t("chartYieldEvolution"),
        data,
        backgroundColor: "#10b481",
        borderRadius: 12,
        borderSkipped: false,
        barThickness: 24,
        hoverBackgroundColor: "#ffffff",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#ffffff",
          titleColor: "#112830",
          bodyColor: "#112830",
          titleFont: { weight: 'bold' },
          padding: 12,
          cornerRadius: 12,
          displayColors: false
        },
      },
      scales: {
        x: { 
          grid: { display: false }, 
          ticks: { color: "rgba(255,255,255,0.4)", font: { size: 10, weight: "bold" } } 
        },
        y: { 
          beginAtZero: true, 
          grid: { color: "rgba(255,255,255,0.05)" },
          ticks: { color: "rgba(255,255,255,0.4)", font: { size: 10, weight: "bold" } } 
        },
      },
    },
  })
}

// ===== HARVEST =====
function calculateTrends() {
  if (!harvestHistory.value.length) return

  const grouped = harvestHistory.value.reduce((acc: Record<string, any[]>, r) => {
    const key = r.parcel_crop_id
    if (!acc[key]) acc[key] = []
    acc[key].push(r)
    return acc
  }, {})

  Object.values(grouped).forEach((records) => {
    records.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    records.forEach((r, i) => {
      if (i === 0) { r.trend = "neutral"; r.trendValue = 0; return }
      const diff = r.yield - records[i - 1].yield
      r.trend      = diff > 0 ? "up" : diff < 0 ? "down" : "neutral"
      r.trendValue = Math.abs(diff)
    })
  })

  harvestHistory.value = Object.values(grouped).flat()
}

function updatePaginatedHarvest() {
  const start = (currentPage.value - 1) * itemsPerPage
  paginatedHarvest.value = (harvestHistory.value ?? []).slice(start, start + itemsPerPage).map((r, idx) => ({
    // ✅ FIX: yield_records n'a pas d'id → on génère un id stable
    id:         r.id ?? `${r.parcel_crop_id}-${r.date}-${idx}`,
    date:       r.date,
    quantity:   r.yield,
    observation:r.notes,
    trend:      r.trend ?? "neutral",
    trendValue: r.trendValue ?? 0,
  }))
}

const totalPages = computed(() =>
  Math.max(1, Math.ceil((harvestHistory.value ?? []).length / itemsPerPage))
)

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  return pages
})

watch(harvestHistory, updatePaginatedHarvest, { immediate: true })
watch(currentPage,   updatePaginatedHarvest)

function prevPage()  { if (currentPage.value > 1) currentPage.value-- }
function nextPage()  { if (currentPage.value < totalPages.value) currentPage.value++ }
function goToPage(p: number | string) { if (typeof p === "number") currentPage.value = p }

async function deleteRecord(id: string) {
  try {
    await apiFetch(`/api/yield-records/${id}/`, { method: "DELETE" })
    harvestHistory.value = harvestHistory.value.filter((r) => r.id !== id)
  } catch (e) {
    console.error("Erreur suppression record:", e)
  }
}

function exportCSV() {
  const data = paginatedHarvest.value
  if (!data.length) return
  const headers = Object.keys(data[0])
  const csv = [headers.join(","), ...data.map((r) => headers.map((h) => `"${(r as any)[h]}"`).join(","))].join("\n")
  const link = Object.assign(document.createElement("a"), {
    href: URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" })),
    download: "harvest_history.csv",
  })
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// ===== SURFACE =====
// ✅ FIX: parcel.points utilise lat/lng (pas latitude/longitude)
const parcelAreaHa = computed(() => calculateParcelArea(parcelData.points))

function calculateParcelArea(points: any[]) {
  if (!points || points.length < 3) return 0
  let area = 0
  const n = points.length
  for (let i = 0; i < n; i++) {
    // ✅ FIX: lat/lng (pas latitude/longitude)
    const { lat: x1, lng: y1 } = points[i]
    const { lat: x2, lng: y2 } = points[(i + 1) % n]
    area += x1 * y2 - x2 * y1
  }
  area = Math.abs(area / 2)
  const avgLat = points.reduce((s, p) => s + p.lat, 0) / points.length
  const areaM2 = area * 111_000 * 111_000 * Math.cos((avgLat * Math.PI) / 180)
  return (areaM2 / 10_000).toFixed(2)
}

function formatM2(areaInHa: any) {
  if (!areaInHa) return "- m²"
  return `${(Number(areaInHa) * 10000).toLocaleString()} m²`
}

// ===== ANALYTICS =====
async function fetchAnalyticsData() {
  if (!authStore.isAuthenticated) return
  try {
    const data: any = await apiFetch("/api/analytics/yields/")
    analyticsData.value = Object.values(data).map((parcel: any) => ({
      ...parcel,
      mean_yield:          parcel.mean_yield ?? 0,
      mean_yield_per_area: parcel.mean_yield_per_area ?? 0,
      parcel_name:         parcel.parcel_name ?? "Unknown Parcel",
    }))
  } catch (e) {
    console.error("Erreur fetchAnalyticsData:", e)
  }
}

// ✅ FIX: parcelData.name au lieu de parcelData.parcel_name
watch(() => parcelData.name, (name) => {
  if (!name) return
  selectedParcel.value = analyticsData.value.find(
    (p) => p.parcel_name?.trim().toLowerCase() === String(name).trim().toLowerCase()
  ) ?? null
})

// ===== CHARGEMENT PRINCIPAL =====
async function fetchParcelData() {
  if (!authStore.isAuthenticated || !fieldIdParam) return

  try {
    const fullData: any = await apiFetch(`/api/parcels/${fieldIdParam}/full_data/`)

    Object.assign(parcelFullData, fullData)
    // ✅ FIX: parcel est directement fullData.parcel (name, points, uuid, created_at)
    Object.assign(parcelData, fullData.parcel ?? {})

    if (fullData.weather_data) updateWeatherForecast(fullData)

    // ✅ FIX: soil layers dans fullData.soil_data.data.properties.layers
    updateSoilQualities(fullData.soil_data?.data?.properties?.layers)

    // ✅ FIX: tasks depuis fullData.tasks.tasks
    updateTasks(fullData)

    await nextTick()
    updateTaskChart()
    updateYieldEvolutionChart()
    await initMap()

    // ✅ FIX: yield_records à la racine de fullData
    harvestHistory.value = fullData.yield_records ?? []
    calculateTrends()
    updatePaginatedHarvest()

    // ✅ FIX: parcel n'a pas de champ owner → on ne fait pas l'appel si undefined
    const ownerId = fullData.parcel?.owner
    if (ownerId) {
      try {
        const uData: any = await apiFetch(`/api/users/${ownerId}/`)
        Object.assign(ownerData, uData)
      } catch {
        // owner endpoint peut ne pas exister
      }
    }

  } catch (error) {
    console.error("Erreur fetchParcelData:", error)
  }
}

async function fetchParcelCrops() {
  // ✅ parcel_crops vient déjà de fullData → cet appel reste pour la compatibilité filteredParcelCrops
  if (!authStore.isAuthenticated || !fieldIdParam) return
  try {
    const data: any = await apiFetch("/api/parcel-crops/")
    parcelCrops.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Erreur fetchParcelCrops:", e)
    parcelCrops.value = []
  }
}

onMounted(() => {
  fetchParcelData()
  fetchAnalyticsData()
  fetchParcelCrops()
})
</script>

<style scoped>
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

#map {
  height: 100%;
  width: 100%;
}

:deep(.leaflet-bar) {
  border: none;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

:deep(.leaflet-bar a) {
  background-color: white;
  color: #112830;
  border-radius: 12px !important;
  margin-bottom: 5px;
  border: none;
}

.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>