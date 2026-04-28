<template>
  <ClientOnly>
    <div class="p-1 sm:p-6 space-y-4 sm:space-y-6 mb-10 sm:mb-1 items-center justify-center">
    
    <!-- Skeleton Loading State -->
    <div v-if="pending" class="space-y-6 sm:p-6 p-1">
      <div class="h-10 w-48 bg-gray-100 rounded-lg animate-pulse mb-8"></div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div v-for="i in 4" :key="i" class="h-28 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div class="lg:col-span-2 h-80 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
        <div class="h-80 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
      </div>
      <div class="h-80 bg-white border border-gray-100 rounded-2xl animate-pulse shadow-sm"></div>
    </div>

    <template v-else>
      <!-- Main Content -->
      <!-- ===== EN-TÊTE ===== -->
      <div class="mb-8">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h2 class="text-3xl sm:text-4xl font-black text-[#112830] tracking-tight mb-2">
              {{ t("dashboard") }}
            </h2>
            <p class="text-gray-500 font-medium text-sm flex items-center gap-2">
              <i class="bx bx-calendar text-[#10b481]"></i>
              {{ new Date().toLocaleDateString(languageStore.lang, { weekday: 'long', day: 'numeric', month: 'long' }) }}
            </p>
          </div>
          
          <nav class="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
            <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
              <i class="bx bx-home text-base"></i>
              <span>Home</span>
            </NuxtLink>
            <i class="bx bx-chevron-right text-gray-300 text-sm"></i>
            <span class="text-[#10b481]">{{ t("dashboard") }}</span>
          </nav>
        </div>
      </div>

      <!-- ===== KPI CARDS ===== -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(16,180,129,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#10b481] shadow-lg shadow-[#10b481]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-location-alt text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">{{ t("parcels") }}</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ totalParcels }}</p>
          </div>
          <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <i class="bx bx-right-arrow-alt text-[#10b481] text-xl"></i>
          </div>
        </div>

        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(201,147,131,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#c99383] shadow-lg shadow-[#c99383]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-task text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">{{ t("tasks") }}</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ totalTasks }}</p>
          </div>
          <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <i class="bx bx-right-arrow-alt text-[#c99383] text-xl"></i>
          </div>
        </div>

        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(33,158,188,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#219ebc] shadow-lg shadow-[#219ebc]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-leaf text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">{{ t("crops") }}</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ totalCrops }}</p>
          </div>
          <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <i class="bx bx-right-arrow-alt text-[#219ebc] text-xl"></i>
          </div>
        </div>

        <div class="group relative flex items-center gap-4 p-6 rounded-3xl border border-white bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(109,76,65,0.08)] transition-all duration-500 hover:-translate-y-1">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-white flex-shrink-0 bg-[#6d4c41] shadow-lg shadow-[#6d4c41]/20 group-hover:scale-110 transition-transform">
            <i class="bx bx-layers text-2xl"></i>
          </div>
          <div class="min-w-0">
            <p class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">{{ t("yield") }}</p>
            <p class="text-3xl font-black text-[#112830] leading-none">{{ totalParcelCrops }}</p>
          </div>
          <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <i class="bx bx-right-arrow-alt text-[#6d4c41] text-xl"></i>
          </div>
        </div>
      </div>

      <!-- ===== GRAPHE TÂCHES + TOP YIELD ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
          <div class="flex flex-col sm:flex-row sm:items-start justify-between mb-8 gap-4">
            <div>
              <h3 class="font-black text-[#112830] text-xl tracking-tight">{{ t("productivity") }}</h3>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Task status breakdown</p>
            </div>
            <div class="flex items-center gap-3">
              <select
                v-model="selectedParcelId"
                class="text-xs font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-4 py-3 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
              >
                <option value="">{{ t("allParcels") }}</option>
                <option v-for="entry in dashboard.task_summary" :key="entry.parcel_id" :value="entry.parcel_id">
                  {{ getParcelName(entry.parcel_id) }}
                </option>
              </select>
              <div class="px-4 py-3 bg-[#112830] text-white text-[10px] font-black uppercase tracking-widest rounded-xl whitespace-nowrap">
                {{ filteredTotalTasks }} {{ t("tasks") }}
              </div>
            </div>
          </div>

          <div class="space-y-8">
            <div v-for="status in taskStatusList" :key="status.key" class="group">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg" :style="{ background: status.color + '15', color: status.color }">
                    <i :class="status.key === 'completed' ? 'bx bx-check-double' : 'bx bx-time-five'"></i>
                  </div>
                  <div>
                    <span class="text-sm font-bold text-[#112830] block">{{ status.label }}</span>
                    <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ status.count }} {{ t("taskUnits") }}</span>
                  </div>
                </div>
                <div class="text-right">
                  <span class="text-lg font-black text-[#112830]" :style="{ color: status.color }">{{ status.pct }}%</span>
                </div>
              </div>
              <div class="h-3 bg-gray-50 rounded-full overflow-hidden p-0.5 border border-gray-100">
                <div
                  class="h-full rounded-full transition-all duration-1000 ease-out shadow-sm"
                  :style="{ width: status.pct + '%', background: `linear-gradient(to right, ${status.color}, ${status.color}dd)` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
          <div class="flex items-center justify-between mb-8">
            <div>
              <h3 class="font-black text-[#112830] text-xl tracking-tight">Top Yields</h3>
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mt-1">Harvest performance</p>
            </div>
            <div class="w-10 h-10 bg-[#f0fdf4] rounded-xl flex items-center justify-center text-[#10b481]">
              <i class="bx bx-trending-up text-xl"></i>
            </div>
          </div>

          <div v-if="!topYield.length" class="space-y-6">
            <div v-for="i in 5" :key="i" class="animate-pulse flex items-center gap-4">
              <div class="w-10 h-10 bg-gray-100 rounded-xl"></div>
              <div class="flex-1 space-y-2">
                <div class="h-4 bg-gray-100 rounded-lg w-3/4"></div>
                <div class="h-3 bg-gray-50 rounded-lg w-1/2"></div>
              </div>
            </div>
          </div>

          <div v-else class="space-y-6">
            <div
              v-for="(item, index) in topYield"
              :key="index"
              class="group flex items-center gap-4 p-4 rounded-2xl hover:bg-gray-50 transition-all border border-transparent hover:border-gray-100"
            >
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center text-sm font-black flex-shrink-0 shadow-sm transition-transform group-hover:scale-110"
                :class="{
                  'bg-[#112830] text-white': index === 0,
                  'bg-gray-100 text-[#112830]': index === 1,
                  'bg-[#f4a26120] text-[#f4a261]': index === 2,
                  'bg-gray-50 text-gray-400': index > 2,
                }"
              >{{ index + 1 }}</div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-[#112830] truncate group-hover:text-[#10b481] transition-colors">{{ item.parcel_name }}</p>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest flex items-center gap-1.5 truncate mt-0.5">
                  <i class="bx bx-leaf text-[#10b481]"></i>
                  {{ item.crop_name || '—' }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-base font-black text-[#10b481]">{{ formatYield(item.total_yield) }}</p>
                <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest -mt-1">kg</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== GRAPHE RENDEMENT PAR PARCELLE ===== -->
      <div class="bg-white rounded-3xl border border-gray-100 p-8 shadow-sm">
        <div class="flex flex-col xl:flex-row xl:items-start justify-between mb-10 gap-6">
          <div>
            <h3 class="font-black text-[#112830] text-2xl tracking-tight">{{ t("yield") }} Intelligence</h3>
            <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Comparative harvest analysis</p>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <!-- Mode Toggle -->
            <div class="flex p-1 bg-gray-50 rounded-xl border border-gray-100">
              <button
                @click="yieldMetric = 'total'"
                class="px-4 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all"
                :class="yieldMetric === 'total' ? 'bg-[#112830] text-white shadow-lg' : 'text-gray-400 hover:text-[#112830]'"
              >Total</button>
              <button
                @click="yieldMetric = 'avg'"
                class="px-4 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all"
                :class="yieldMetric === 'avg' ? 'bg-[#112830] text-white shadow-lg' : 'text-gray-400 hover:text-[#112830]'"
              >Avg</button>
            </div>

            <!-- Visualization Toggle -->
            <div class="flex p-1 bg-gray-50 rounded-xl border border-gray-100">
              <button
                @click="yieldChartType = 'bar'"
                class="px-4 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all flex items-center gap-1.5"
                :class="yieldChartType === 'bar' ? 'bg-[#10b481] text-white shadow-lg' : 'text-gray-400 hover:text-[#10b481]'"
              >
                <i class="bx bx-bar-chart-alt-2 text-sm"></i> Bar
              </button>
              <button
                @click="yieldChartType = 'line'"
                class="px-4 py-2 font-black text-[10px] uppercase tracking-widest rounded-lg transition-all flex items-center gap-1.5"
                :class="yieldChartType === 'line' ? 'bg-[#10b481] text-white shadow-lg' : 'text-gray-400 hover:text-[#10b481]'"
              >
                <i class="bx bx-line-chart text-sm"></i> Line
              </button>
            </div>

            <!-- Filters -->
            <div class="flex items-center gap-3 w-full sm:w-auto">
              <select
                v-model="yieldParcelFilter"
                class="flex-1 sm:flex-none text-xs font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-4 py-3 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
              >
                <option value="">{{ t("allParcels") }}</option>
                <option v-for="parcel in uniqueParcels" :key="parcel" :value="parcel">{{ parcel }}</option>
              </select>

              <select
                v-model="yieldCropFilter"
                class="flex-1 sm:flex-none text-xs font-bold uppercase tracking-wider border-none bg-gray-50 rounded-xl px-4 py-3 text-gray-500 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition cursor-pointer"
              >
                <option value="">{{ t("allCrops") }}</option>
                <option v-for="crop in uniqueCropsForSelectedParcel" :key="crop" :value="crop">{{ crop }}</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="!chartReady || !filteredYieldSummary.length" class="h-[400px] flex items-center justify-center bg-gray-50/50 rounded-3xl border border-dashed border-gray-200">
          <div class="text-center group">
            <div class="w-16 h-16 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm group-hover:scale-110 transition-transform">
              <i class="bx bx-bar-chart-alt-2 text-3xl text-gray-300"></i>
            </div>
            <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">Aucune donnée disponible</p>
          </div>
        </div>

        <div v-else class="h-[400px] w-full">
          <component
            :is="currentChartComponent"
            :data="yieldChartData"
            :options="yieldChartOptions"
            :key="chartKey"
          />
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

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const authStore = useAuthStore();
const languageStore = useLanguageStore();
const { apiFetch } = useApi();

const BarChart   = shallowRef<any>(null);
const LineChart  = shallowRef<any>(null);
const chartReady = ref(false);
const chartKey   = ref(0);

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

function getParcelName(parcelId: string): string {
  const found = dashboard.value.parcels?.find((p: any) => p.id === parcelId);
  return found?.name ?? parcelId;
}

function formatYield(value: number): string {
  if (value >= 1000) return (value / 1000).toFixed(1) + "k";
  return value.toLocaleString("fr");
}

const totalParcels = computed(() => dashboard.value.parcels?.length || 0);
const totalTasks = computed(() =>
  dashboard.value.task_summary?.reduce((sum: number, e: any) => sum + (e.task_summary?.total_tasks || 0), 0) || 0
);
const totalCrops = computed(() => {
  const names = new Set(dashboard.value.yield_summary?.map((y: any) => y.crop_name).filter(Boolean) || []);
  return names.size;
});
const totalParcelCrops = computed(() => dashboard.value.yield_summary?.length || 0);

const filteredTaskSummary = computed(() => {
  if (!selectedParcelId.value) return dashboard.value.task_summary || [];
  return (dashboard.value.task_summary || []).filter((e: any) => e.parcel_id === selectedParcelId.value);
});

const filteredTotalTasks = computed(() =>
  filteredTaskSummary.value.reduce((sum: number, e: any) => sum + (e.task_summary?.total_tasks || 0), 0)
);

const taskStatusList = computed(() => {
  let completed = 0, remaining = 0;
  filteredTaskSummary.value.forEach((e: any) => {
    const s = e.task_summary || {};
    completed += s.completed_tasks || 0;
    remaining += (s.total_tasks || 0) - (s.completed_tasks || 0);
  });
  const total = completed + remaining || 1;
  const pct = (n: number) => Math.round((n / total) * 100);
  return [
    { key: "completed", label: "Completed", count: completed, pct: pct(completed), color: "#10b481" },
    { key: "remaining", label: "Remaining",  count: remaining,  pct: pct(remaining),  color: "#c99383" },
  ];
});

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
  const crops = scoped.map((y: any) => y.crop_name).filter(Boolean);
  return [...new Set(crops)] as string[];
});

const filteredYieldSummary = computed(() => {
  let raw = dashboard.value.yield_summary || [];
  if (yieldParcelFilter.value) raw = raw.filter((y: any) => y.parcel_name === yieldParcelFilter.value);
  if (yieldCropFilter.value) raw = raw.filter((y: any) => y.crop_name === yieldCropFilter.value);
  return raw;
});

const currentChartComponent = computed(() => yieldChartType.value === "bar" ? BarChart.value : LineChart.value);

const yieldChartData = computed(() => {
  const data = filteredYieldSummary.value;
  if (!data.length) return { labels: [], datasets: [] };
  const labels = data.map((y: any) => y.crop_name ? `${y.parcel_name} – ${y.crop_name}` : y.parcel_name);
  const values = data.map((y: any) => yieldMetric.value === "total" ? y.summary?.total_yield || 0 : y.summary?.avg_yield || 0);
  const color = "#10b481";
  return {
    labels,
    datasets: [{
      label: yieldMetric.value === "total" ? "Total yield (kg)" : "Avg yield (kg)",
      data: values,
      backgroundColor: yieldChartType.value === 'bar' ? color : "rgba(16,180,129,0.15)",
      borderColor: color,
      borderWidth: yieldChartType.value === 'bar' ? 0 : 2,
      borderRadius: yieldChartType.value === 'bar' ? 6 : 0,
      fill: yieldChartType.value !== 'bar',
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
  const [vueChartjs, chartjs] = await Promise.all([
    import("vue-chartjs"),
    import("chart.js")
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
    chartjs.Filler
  );
  chartReady.value = true;
});
</script>