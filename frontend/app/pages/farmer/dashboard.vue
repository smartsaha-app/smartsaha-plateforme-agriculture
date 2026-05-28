<template>
  <ClientOnly>
    <div class="min-h-screen bg-[#f8fafc] p-2 sm:p-6 space-y-5 mb-10 sm:mb-2">

      <!-- ===== SKELETON ===== -->
      <div v-if="pending" class="space-y-5">
        <div class="h-24 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
        <div class="flex gap-3">
          <div v-for="i in 3" :key="i" class="h-10 w-40 bg-white rounded-xl animate-pulse shadow-sm"></div>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="h-24 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div class="lg:col-span-2 h-72 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
          <div class="h-72 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
        </div>
        <div class="h-96 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
      </div>

      <template v-else>

        <!-- ===== EN-TÊTE ===== -->
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h2 class="text-3xl sm:text-4xl font-black text-[#112830] tracking-tight leading-tight">
              {{ t("dashboard") }}
            </h2>
          </div>
          <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
            <NuxtLink :to="localePath('/farmer/dashboard')" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
              <i class="bx bx-home text-sm"></i>
              <span>{{ t("home") }}</span>
            </NuxtLink>
            <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
            <span class="text-[#10b481]">{{ t("dashboard") }}</span>
          </nav>
        </div>

        <!-- ===== KPI CARDS ===== -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

          <!-- Parcelles -->
          <NuxtLink
            :to="localePath('/farmer/parcels')"
            class="group relative flex items-center gap-4 p-5 rounded-2xl border border-gray-100 bg-white shadow-sm hover:shadow-md hover:border-[#10b481]/30 transition-all duration-300 hover:-translate-y-0.5"
          >
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white flex-shrink-0 bg-[#10b481] shadow-md shadow-[#10b481]/25 group-hover:scale-110 transition-transform">
              <i class="bx bx-map text-xl"></i>
            </div>
            <div class="min-w-0">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-0.5">Parcelles</p>
              <p class="text-2xl sm:text-3xl font-black text-[#112830] leading-none">{{ totalParcels }}</p>
            </div>
            <i class="bx bx-right-arrow-alt text-[#10b481] text-base absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity"></i>
          </NuxtLink>

          <!-- Tâches + badge retard -->
          <div class="group relative flex items-center gap-4 p-5 rounded-2xl border border-gray-100 bg-white shadow-sm hover:shadow-md hover:border-[#c99383]/30 transition-all duration-300 hover:-translate-y-0.5">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white flex-shrink-0 bg-[#c99383] shadow-md shadow-[#c99383]/25 group-hover:scale-110 transition-transform">
              <i class="bx bx-task text-xl"></i>
            </div>
            <div class="min-w-0 flex-1">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-0.5">{{ t("tasks") }}</p>
              <div class="flex items-baseline gap-2 flex-wrap">
                <p class="text-2xl sm:text-3xl font-black text-[#112830] leading-none">{{ totalTasks }}</p>
                <span
                  v-if="overdueCount > 0"
                  class="text-[9px] font-black uppercase tracking-wider px-1.5 py-0.5 bg-red-50 text-red-500 rounded-lg border border-red-100 leading-none"
                >
                  {{ overdueCount }} retard{{ overdueCount > 1 ? 's' : '' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Plantations actives -->
          <div class="group relative flex items-center gap-4 p-5 rounded-2xl border border-gray-100 bg-white shadow-sm hover:shadow-md hover:border-[#219ebc]/30 transition-all duration-300 hover:-translate-y-0.5">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white flex-shrink-0 bg-[#219ebc] shadow-md shadow-[#219ebc]/25 group-hover:scale-110 transition-transform">
              <i class="bx bx-leaf text-xl"></i>
            </div>
            <div class="min-w-0">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-0.5">Plantations</p>
              <p class="text-2xl sm:text-3xl font-black text-[#112830] leading-none">{{ activePlantations }}</p>
              <p class="text-[9px] text-gray-400 font-semibold mt-0.5">en cours</p>
            </div>
          </div>

          <!-- Total récolte kg -->
          <div class="group relative flex items-center gap-4 p-5 rounded-2xl border border-gray-100 bg-white shadow-sm hover:shadow-md hover:border-[#6d4c41]/30 transition-all duration-300 hover:-translate-y-0.5">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white flex-shrink-0 bg-[#6d4c41] shadow-md shadow-[#6d4c41]/25 group-hover:scale-110 transition-transform">
              <i class="bx bx-package text-xl"></i>
            </div>
            <div class="min-w-0">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-0.5">{{ t("yield") }}</p>
              <p class="text-2xl sm:text-3xl font-black text-[#112830] leading-none">{{ formatYield(totalYieldKg) }}</p>
              <p class="text-[9px] text-gray-400 font-semibold mt-0.5">kg total</p>
            </div>
          </div>
        </div>

        <!-- ===== TÂCHES PAR STATUT + PROCHAINES RÉCOLTES ===== -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">

          <!-- Statut des tâches (2/3) -->
          <div class="lg:col-span-2 bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-start justify-between mb-6 gap-4">
              <div>
                <h3 class="font-black text-[#112830] text-lg tracking-tight">{{ t("productivity") }}</h3>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mt-1">{{ t("taskStatusBreakdown") }}</p>
              </div>
              <div class="flex items-center gap-3">
                <select
                  v-model="selectedParcelId"
                  class="text-[11px] font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-3 py-2.5 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
                >
                  <option value="">{{ t("allParcels") }}</option>
                  <option v-for="entry in dashboard.task_summary" :key="entry.parcel_id" :value="entry.parcel_id">
                    {{ getParcelName(entry.parcel_id) }}
                  </option>
                </select>
                <div class="px-3 py-2.5 bg-[#112830] text-white text-[10px] font-black uppercase tracking-widest rounded-xl whitespace-nowrap">
                  {{ filteredTotalTasks }} {{ t("tasks") }}
                </div>
              </div>
            </div>

            <!-- 4 statuts -->
            <div v-if="taskStatsPending" class="space-y-4">
              <div v-for="i in 4" :key="i" class="h-10 bg-gray-50 rounded-xl animate-pulse"></div>
            </div>
            <div v-else class="space-y-5">
              <div v-for="status in taskStatusList" :key="status.key">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-3">
                    <div
                      class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
                      :style="{ background: status.color + '20', color: status.color }"
                    >
                      <i :class="status.icon"></i>
                    </div>
                    <div>
                      <span class="text-[13px] font-bold text-[#112830] block">{{ status.label }}</span>
                      <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ status.count }} {{ t("taskUnits") }}</span>
                    </div>
                  </div>
                  <span class="text-base font-black" :style="{ color: status.color }">{{ status.pct }}%</span>
                </div>
                <div class="h-2 bg-gray-50 rounded-full overflow-hidden border border-gray-100">
                  <div
                    class="h-full rounded-full transition-all duration-1000 ease-out"
                    :style="{ width: status.pct + '%', background: status.color }"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Alerte retard -->
            <div v-if="overdueCount > 0" class="mt-5 flex items-center gap-3 p-3 bg-red-50 rounded-xl border border-red-100">
              <i class="bx bx-error-circle text-red-400 text-xl flex-shrink-0"></i>
              <p class="text-[12px] font-bold text-red-600">
                {{ overdueCount }} tâche{{ overdueCount > 1 ? 's' : '' }} en retard — vérifiez votre planning
              </p>
            </div>
          </div>

          <!-- Prochaines récoltes (1/3) -->
          <div class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
            <div class="flex items-center justify-between mb-5">
              <div>
                <h3 class="font-black text-[#112830] text-lg tracking-tight">Prochaines récoltes</h3>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mt-1">Calendrier</p>
              </div>
              <div class="w-9 h-9 bg-amber-50 rounded-xl flex items-center justify-center text-amber-500">
                <i class="bx bx-calendar-check text-lg"></i>
              </div>
            </div>

            <!-- Skeleton -->
            <div v-if="parcelCropsPending" class="space-y-3">
              <div v-for="i in 4" :key="i" class="h-14 bg-gray-50 rounded-xl animate-pulse"></div>
            </div>

            <!-- Empty -->
            <div
              v-else-if="!upcomingHarvests.length"
              class="h-36 flex flex-col items-center justify-center bg-gray-50 rounded-xl border border-dashed border-gray-200"
            >
              <i class="bx bx-calendar text-2xl text-gray-300 mb-2"></i>
              <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Aucune récolte prévue</p>
            </div>

            <!-- List -->
            <div v-else class="space-y-2.5">
              <div
                v-for="(harvest, index) in upcomingHarvests"
                :key="index"
                class="flex items-center gap-3 p-3 rounded-xl border border-gray-50 hover:bg-gray-50 transition-colors cursor-default"
              >
                <div
                  class="w-11 h-11 rounded-xl flex flex-col items-center justify-center flex-shrink-0"
                  :class="harvest.daysLeft <= 7 ? 'bg-red-50 text-red-500' : harvest.daysLeft <= 30 ? 'bg-amber-50 text-amber-500' : 'bg-emerald-50 text-emerald-600'"
                >
                  <span class="text-[15px] font-black leading-none">{{ harvest.daysLeft }}</span>
                  <span class="text-[8px] font-black uppercase tracking-wider">j</span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-[13px] font-bold text-[#112830] truncate">{{ harvest.cropName }}</p>
                  <p class="text-[10px] text-gray-400 font-semibold truncate">{{ harvest.harvestDateStr }}</p>
                </div>
                <div
                  v-if="harvest.statusName"
                  class="text-[9px] font-black px-2 py-1 bg-emerald-50 text-emerald-600 rounded-lg uppercase tracking-wider flex-shrink-0 border border-emerald-100"
                >
                  {{ harvest.statusName }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== GRAPHE RENDEMENT + TOP YIELDS ===== -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">

          <!-- Yield Chart (2/3) -->
          <div class="lg:col-span-2 bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
            <div class="flex flex-col xl:flex-row xl:items-start justify-between mb-8 gap-4">
              <div>
                <h3 class="font-black text-[#112830] text-lg tracking-tight">{{ t("yieldIntelligence") }}</h3>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mt-1">{{ t("comparativeHarvestAnalysis") }}</p>
              </div>

              <div class="flex flex-wrap items-center gap-3">
                <!-- Mode Total/Moy -->
                <div class="flex p-1 bg-gray-50 rounded-xl border border-gray-100">
                  <button
                    @click="yieldMetric = 'total'"
                    class="px-3 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all"
                    :class="yieldMetric === 'total' ? 'bg-[#112830] text-white shadow-md' : 'text-gray-400 hover:text-[#112830]'"
                  >{{ t("total") }}</button>
                  <button
                    @click="yieldMetric = 'avg'"
                    class="px-3 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all"
                    :class="yieldMetric === 'avg' ? 'bg-[#112830] text-white shadow-md' : 'text-gray-400 hover:text-[#112830]'"
                  >{{ t("avg") }}</button>
                </div>

                <!-- Bar/Line toggle -->
                <div class="flex p-1 bg-gray-50 rounded-xl border border-gray-100">
                  <button
                    @click="yieldChartType = 'bar'"
                    class="px-3 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all flex items-center gap-1.5"
                    :class="yieldChartType === 'bar' ? 'bg-[#10b481] text-white shadow-md' : 'text-gray-400 hover:text-[#10b481]'"
                  >
                    <i class="bx bx-bar-chart-alt-2 text-sm"></i> {{ t("bar") }}
                  </button>
                  <button
                    @click="yieldChartType = 'line'"
                    class="px-3 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all flex items-center gap-1.5"
                    :class="yieldChartType === 'line' ? 'bg-[#10b481] text-white shadow-md' : 'text-gray-400 hover:text-[#10b481]'"
                  >
                    <i class="bx bx-line-chart text-sm"></i> {{ t("line") }}
                  </button>
                </div>

                <!-- Filtres -->
                <div class="flex items-center gap-2 w-full sm:w-auto">
                  <select
                    v-model="yieldParcelFilter"
                    class="flex-1 sm:flex-none text-[11px] font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-3 py-2.5 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
                  >
                    <option value="">{{ t("allParcels") }}</option>
                    <option v-for="parcel in uniqueParcels" :key="parcel" :value="parcel">{{ parcel }}</option>
                  </select>
                  <select
                    v-model="yieldCropFilter"
                    class="flex-1 sm:flex-none text-[11px] font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-3 py-2.5 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
                  >
                    <option value="">{{ t("allCrops") }}</option>
                    <option v-for="crop in uniqueCropsForSelectedParcel" :key="crop" :value="crop">{{ crop }}</option>
                  </select>
                </div>
              </div>
            </div>

            <div v-if="!chartReady || !filteredYieldSummary.length" class="h-[340px] flex items-center justify-center bg-gray-50/50 rounded-2xl border border-dashed border-gray-200">
              <div class="text-center">
                <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm">
                  <i class="bx bx-bar-chart-alt-2 text-2xl text-gray-300"></i>
                </div>
                <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest">{{ t("noDataAvailable") }}</p>
              </div>
            </div>

            <div v-else class="h-[340px] w-full">
              <component
                :is="currentChartComponent"
                :data="yieldChartData"
                :options="yieldChartOptions"
                :key="chartKey"
              />
            </div>
          </div>

          <!-- Top Yields (1/3) -->
          <div class="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h3 class="font-black text-[#112830] text-lg tracking-tight">{{ t("topYields") }}</h3>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mt-1">{{ t("harvestPerformance") }}</p>
              </div>
              <div class="w-9 h-9 bg-[#f0fdf4] rounded-xl flex items-center justify-center text-[#10b481]">
                <i class="bx bx-trending-up text-lg"></i>
              </div>
            </div>

            <div v-if="!topYield.length" class="space-y-4">
              <div v-for="i in 5" :key="i" class="animate-pulse flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-100 rounded-xl"></div>
                <div class="flex-1 space-y-2">
                  <div class="h-3.5 bg-gray-100 rounded-lg w-3/4"></div>
                  <div class="h-2.5 bg-gray-50 rounded-lg w-1/2"></div>
                </div>
              </div>
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="(item, index) in topYield"
                :key="index"
                class="group flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-all border border-transparent hover:border-gray-100"
              >
                <div
                  class="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-black flex-shrink-0 shadow-sm transition-transform group-hover:scale-110"
                  :class="{
                    'bg-[#112830] text-white': index === 0,
                    'bg-gray-100 text-[#112830]': index === 1,
                    'bg-[#f4a26120] text-[#f4a261]': index === 2,
                    'bg-gray-50 text-gray-400': index > 2,
                  }"
                >{{ index + 1 }}</div>
                <div class="flex-1 min-w-0">
                  <p class="text-[13px] font-bold text-[#112830] truncate group-hover:text-[#10b481] transition-colors">{{ item.parcel_name }}</p>
                  <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest flex items-center gap-1 truncate mt-0.5">
                    <i class="bx bx-leaf text-[#10b481] text-xs"></i>
                    {{ item.crop_name || '—' }}
                  </p>
                </div>
                <div class="text-right flex-shrink-0">
                  <p class="text-[15px] font-black text-[#10b481]">{{ formatYield(item.total_yield) }}</p>
                  <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest -mt-0.5">kg</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </template>
    </div>
  </ClientOnly>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, computed, watch, onMounted, shallowRef, nextTick } from "vue";
import { useAuthStore } from "~/stores/auth";
import { useLanguageStore } from "~/stores/language";
import { useApi } from "~/composables/useApi";

interface DashboardData {
  parcels: any[];
  task_summary: any[];
  yield_summary: any[];
  soil_summary: any[];
  crop_summary: any[];
}

const { t: nuxtT, locale } = useI18n();
const localePath = useLocalePath();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const authStore = useAuthStore();
const languageStore = useLanguageStore();
const { apiFetch } = useApi();

// ── Chart setup ────────────────────────────────────────────────────────────
const BarChart   = shallowRef<any>(null);
const LineChart  = shallowRef<any>(null);
const chartReady = ref(false);
const chartKey   = ref(0);

// ── Full dashboard data ────────────────────────────────────────────────────
const dashboardState = useState<DashboardData>("dashboardData", () => ({
  parcels: [],
  task_summary: [],
  yield_summary: [],
  soil_summary: [],
  crop_summary: [],
}));

const dashboard = ref<DashboardData>(dashboardState.value);

const { data, pending } = useLazyAsyncData<DashboardData>(
  "dashboard-data",
  () => apiFetch("/api/dashboard/full_dashboard/"),
  { server: false }
);

watch(data, (newData) => {
  if (newData) {
    dashboard.value = newData;
    dashboardState.value = newData;
  }
}, { immediate: true });

// ── Task stats (4 statuses + overdue) ─────────────────────────────────────
// Géré manuellement pour être réactif au filtre parcelle (voir fetchTaskStats)
const taskStatsData    = ref<any>(null);
const taskStatsPending = ref(false);

// ── Parcel crops (upcoming harvests + active plantations) ──────────────────
const parcelCropsData = ref<any[]>([]);

const { data: rawParcelCrops, pending: parcelCropsPending } = useLazyAsyncData<any[]>(
  "parcel-crops-dashboard",
  () => apiFetch("/api/parcel-crops/"),
  { server: false }
);

watch(rawParcelCrops, (v) => { if (v) parcelCropsData.value = v; }, { immediate: true });

// ── Filters state ──────────────────────────────────────────────────────────
const selectedParcelId  = ref<string>("");
const yieldMetric       = ref<"total" | "avg">("total");
const yieldChartType    = ref<"bar" | "line">("bar");
const yieldParcelFilter = ref<string>("");
const yieldCropFilter   = ref<string>("");

watch(yieldParcelFilter, () => {
  if (!uniqueCropsForSelectedParcel.value.includes(yieldCropFilter.value)) {
    yieldCropFilter.value = "";
  }
});

watch(yieldChartType, async () => {
  await nextTick();
  chartKey.value++;
});

// ── Fetch task stats (réactif au filtre parcelle) ──────────────────────────
async function fetchTaskStats(parcelId: string = "") {
  taskStatsPending.value = true;
  try {
    const url = parcelId
      ? `/api/tasks/dashboard/?parcel_id=${parcelId}`
      : "/api/tasks/dashboard/";
    taskStatsData.value = await apiFetch(url);
  } catch (e) {
    console.error("fetchTaskStats error:", e);
  } finally {
    taskStatsPending.value = false;
  }
}

watch(selectedParcelId, (newId) => {
  fetchTaskStats(newId);
});

// ── Greeting ───────────────────────────────────────────────────────────────
const greetingLabel = computed(() => {
  const h = new Date().getHours();
  if (h < 12) return "Bonjour";
  if (h < 18) return "Bon après-midi";
  return "Bonsoir";
});

const greetingName = computed(() => {
  // Priorité : first_name > username > salutation seule
  const name = authStore.firstName || authStore.username;
  return name ? `${greetingLabel.value}, ${name} 👋` : `${greetingLabel.value} 👋`;
});

const formattedDate = computed(() =>
  new Date().toLocaleDateString(locale.value, { weekday: 'long', day: 'numeric', month: 'long' })
);

// ── Helpers ────────────────────────────────────────────────────────────────
function getParcelName(parcelId: string): string {
  const found = dashboard.value.parcels?.find((p: any) => p.id === parcelId);
  return found?.name ?? parcelId;
}

function formatYield(value: number): string {
  if (value >= 1000) return (value / 1000).toFixed(1) + "k";
  return value.toLocaleString("fr");
}

// ── KPI computeds ──────────────────────────────────────────────────────────
const totalParcels = computed(() => dashboard.value.parcels?.length || 0);

const totalTasks = computed(() =>
  dashboard.value.task_summary?.reduce((sum: number, e: any) => sum + (e.task_summary?.total_tasks || 0), 0) || 0
);

const activePlantations = computed(() =>
  (parcelCropsData.value || []).filter((pc: any) => pc.is_active).length
);

const totalYieldKg = computed(() =>
  (dashboard.value.yield_summary || []).reduce((sum: number, y: any) => sum + (y.summary?.total_yield || 0), 0)
);

const overdueCount = computed(() => taskStatsData.value?.overdue_count || 0);

// ── Task status chart (4 statuses) ─────────────────────────────────────────
const filteredTaskSummary = computed(() => {
  if (!selectedParcelId.value) return dashboard.value.task_summary || [];
  return (dashboard.value.task_summary || []).filter((e: any) => e.parcel_id === selectedParcelId.value);
});

const filteredTotalTasks = computed(() =>
  filteredTaskSummary.value.reduce((sum: number, e: any) => sum + (e.task_summary?.total_tasks || 0), 0)
);

const taskStatusList = computed(() => {
  const byStatus = taskStatsData.value?.by_status || {};
  const values = Object.values(byStatus) as number[];
  const total = values.reduce((s, v) => s + (v || 0), 0) || 1;
  const pct = (n: number) => Math.round(((n || 0) / total) * 100);

  return [
    {
      key: "Pending",
      label: "En attente",
      count: byStatus["Pending"] || 0,
      pct: pct(byStatus["Pending"]),
      color: "#f59e0b",
      icon: "bx bx-time-five",
    },
    {
      key: "In Progress",
      label: "En cours",
      count: byStatus["In Progress"] || 0,
      pct: pct(byStatus["In Progress"]),
      color: "#219ebc",
      icon: "bx bx-loader-circle",
    },
    {
      key: "Done",
      label: "Terminées",
      count: byStatus["Done"] || 0,
      pct: pct(byStatus["Done"]),
      color: "#10b481",
      icon: "bx bx-check-double",
    },
    {
      key: "Cancelled",
      label: "Annulées",
      count: byStatus["Cancelled"] || 0,
      pct: pct(byStatus["Cancelled"]),
      color: "#9ca3af",
      icon: "bx bx-x-circle",
    },
  ];
});

// ── Upcoming harvests ──────────────────────────────────────────────────────
const upcomingHarvests = computed(() =>
  (parcelCropsData.value || [])
    .filter((pc: any) => pc.days_until_harvest !== null && pc.days_until_harvest >= 0)
    .sort((a: any, b: any) => a.days_until_harvest - b.days_until_harvest)
    .slice(0, 6)
    .map((pc: any) => ({
      cropName: pc.crop?.name || "—",
      daysLeft: pc.days_until_harvest as number,
      harvestDateStr: pc.harvest_date
        ? new Date(pc.harvest_date).toLocaleDateString("fr", { day: "numeric", month: "short" })
        : "—",
      statusName: pc.status?.name || null,
    }))
);

// ── Yield chart ────────────────────────────────────────────────────────────
const topYield = computed(() =>
  (dashboard.value.yield_summary || [])
    .map((y: any) => ({
      parcel_name: y.parcel_name || "—",
      crop_name:   y.crop_name   || "—",
      total_yield: y.summary?.total_yield || 0,
    }))
    .sort((a: any, b: any) => b.total_yield - a.total_yield)
    .slice(0, 5)
);

const uniqueParcels = computed(() => {
  const parcels = (dashboard.value.yield_summary || []).map((y: any) => y.parcel_name).filter(Boolean);
  return [...new Set(parcels)] as string[];
});

const uniqueCropsForSelectedParcel = computed(() => {
  const raw = dashboard.value.yield_summary || [];
  const scoped = yieldParcelFilter.value ? raw.filter((y: any) => y.parcel_name === yieldParcelFilter.value) : raw;
  return [...new Set(scoped.map((y: any) => y.crop_name).filter(Boolean))] as string[];
});

const filteredYieldSummary = computed(() => {
  let raw = dashboard.value.yield_summary || [];
  if (yieldParcelFilter.value) raw = raw.filter((y: any) => y.parcel_name === yieldParcelFilter.value);
  if (yieldCropFilter.value)   raw = raw.filter((y: any) => y.crop_name   === yieldCropFilter.value);
  return raw;
});

const currentChartComponent = computed(() =>
  yieldChartType.value === "bar" ? BarChart.value : LineChart.value
);

const yieldChartData = computed(() => {
  const d = filteredYieldSummary.value;
  if (!d.length) return { labels: [], datasets: [] };
  const labels = d.map((y: any) => y.crop_name ? `${y.parcel_name} – ${y.crop_name}` : y.parcel_name);
  const values = d.map((y: any) =>
    yieldMetric.value === "total" ? y.summary?.total_yield || 0 : y.summary?.avg_yield || 0
  );
  const color = "#10b481";
  return {
    labels,
    datasets: [{
      label: yieldMetric.value === "total" ? "Total yield (kg)" : "Avg yield (kg)",
      data: values,
      backgroundColor: yieldChartType.value === "bar" ? color : "rgba(16,180,129,0.15)",
      borderColor: color,
      borderWidth: yieldChartType.value === "bar" ? 0 : 2,
      borderRadius: yieldChartType.value === "bar" ? 6 : 0,
      fill: yieldChartType.value !== "bar",
      tension: 0.4,
    }],
  };
});

const yieldChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { color: "#9ca3af", font: { size: 11 } } },
    y: { beginAtZero: true, grid: { color: "#f3f4f6" }, ticks: { color: "#9ca3af", font: { size: 11 } } },
  },
};

onMounted(async () => {
  // Chargement initial des stats tâches (global, sans filtre parcelle)
  fetchTaskStats();

  const [vueChartjs, chartjs] = await Promise.all([
    import("vue-chartjs"),
    import("chart.js"),
  ]);

  BarChart.value  = vueChartjs.Bar;
  LineChart.value = vueChartjs.Line;

  chartjs.Chart.register(
    chartjs.CategoryScale,
    chartjs.LinearScale,
    chartjs.BarElement,
    chartjs.LineElement,
    chartjs.PointElement,
    chartjs.Title,
    chartjs.Tooltip,
    chartjs.Legend,
    chartjs.Filler,
  );
  chartReady.value = true;
});
</script>