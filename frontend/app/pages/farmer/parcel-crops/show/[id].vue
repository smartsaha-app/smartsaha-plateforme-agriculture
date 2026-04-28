<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <NuxtLink to="/farmer/parcel-crops" class="hover:text-[#10b481] transition-colors">Parcel crops</NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481]">Détails sur parcel crops</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">Détails sur parcel crops</h1>
      </div>

      <div class="flex items-center gap-3">
        <button @click="goBack" class="p-3 bg-white border border-gray-100 rounded-2xl text-gray-400 hover:text-[#10b481] transition-all shadow-sm">
          <i class="bx bx-arrow-back text-xl"></i>
        </button>
        <NuxtLink
          :to="`/farmer/parcel-crops/edit/${parcelCrop.id}`"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg"
        >
          <i class="bx bx-edit-alt text-lg"></i> {{ t("edit") }}
        </NuxtLink>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- MAIN DETAILS -->
      <div class="lg:col-span-2 space-y-8">
        <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
            <!-- Parcel Item -->
            <div class="flex items-start gap-5 p-6 bg-gray-50 rounded-[2rem] border border-gray-50 group hover:border-[#10b481]/20 transition-all">
              <div class="w-14 h-14 rounded-2xl bg-white flex items-center justify-center text-2xl text-[#10b481] shadow-sm">
                <i class="bx bx-map-alt"></i>
              </div>
              <div class="space-y-1">
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("parcel") }}</p>
                <p class="text-xl font-black tracking-tight">{{ parcelCrop.parcel_name }}</p>
              </div>
            </div>

            <!-- Crop Item -->
            <div class="flex items-start gap-5 p-6 bg-gray-50 rounded-[2rem] border border-gray-50 group hover:border-[#10b481]/20 transition-all">
              <div class="w-14 h-14 rounded-2xl bg-white flex items-center justify-center text-2xl text-[#10b481] shadow-sm">
                <i class="bx bx-leaf"></i>
              </div>
              <div class="space-y-1">
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("crop") }}</p>
                <p class="text-xl font-black tracking-tight">{{ parcelCrop.crop?.name }} <span class="text-sm font-medium text-gray-400">({{ parcelCrop.crop?.variety?.name || "-" }})</span></p>
              </div>
            </div>

            <!-- Dates Item -->
            <div class="flex items-start gap-5 p-6 bg-gray-50 rounded-[2rem] border border-gray-50 lg:col-span-2">
              <div class="grid grid-cols-2 gap-8 w-full">
                <div class="space-y-1">
                  <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("plantingdate") }}</p>
                  <p class="text-lg font-bold text-[#112830]">{{ formatDate(parcelCrop.planting_date) }}</p>
                </div>
                <div class="space-y-1">
                  <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("harvestdate") }}</p>
                  <p class="text-lg font-bold" :class="parcelCrop.harvest_date ? 'text-[#112830]' : 'text-gray-300 italic font-medium'">
                    {{ parcelCrop.harvest_date ? formatDate(parcelCrop.harvest_date) : "Non définie" }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Area & Status -->
            <div class="flex items-start gap-5 p-6 bg-[#112830] rounded-[2rem] shadow-xl shadow-[#112830]/10 text-white">
              <div class="w-14 h-14 rounded-2xl bg-white/10 flex items-center justify-center text-2xl text-[#10b481]">
                <i class="bx bx-area"></i>
              </div>
              <div class="space-y-1">
                <p class="text-[10px] font-black uppercase tracking-widest text-emerald-400/50">Surface exploitée</p>
                <p class="text-3xl font-black tracking-tighter">{{ parcelCrop.area }} <span class="text-sm font-medium tracking-normal text-emerald-400/50">m²</span></p>
              </div>
            </div>

            <div class="flex items-start gap-5 p-6 bg-white rounded-[2rem] border-2 border-gray-50">
               <div class="space-y-3 w-full">
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("status") }}</p>
                <div class="w-full h-2 bg-gray-50 rounded-full overflow-hidden">
                  <div class="h-full bg-[#10b481] transition-all duration-1000" :style="{ width: getStatusProgress(parcelCrop.status?.name) + '%' }"></div>
                </div>
                <span :class="['inline-flex px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border', statusColorClass(parcelCrop.status?.name)]">
                  {{ parcelCrop.status?.name || "-" }}
                </span>
               </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SIDEBAR / FORECAST -->
      <div class="space-y-8">
        <div v-if="forecastData" class="bg-[#112830] rounded-[3rem] p-8 text-white relative overflow-hidden group shadow-2xl">
          <!-- Decorators -->
          <div class="absolute -right-10 -top-10 w-40 h-40 bg-[#10b481] opacity-10 rounded-full filter blur-3xl group-hover:opacity-20 transition-opacity"></div>
          
          <div class="relative space-y-8 text-center flex flex-col items-center">
            <div class="w-20 h-20 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center text-4xl text-[#10b481]">
              <i class="bx bx-radar animate-pulse"></i>
            </div>
            
            <div class="space-y-2">
              <h3 class="text-xs font-black uppercase tracking-[0.3em] text-[#10b481]">{{ t("titleyieldforcast") }}</h3>
              <p class="text-sm text-gray-400 italic">Prévision générée pour le {{ formatDate(forecastData.forecast_date) }}</p>
            </div>

            <div class="space-y-1">
              <p class="text-5xl font-black tracking-tighter">{{ forecastData.predicted_yield.toFixed(1) }}</p>
              <p class="text-xs font-black uppercase text-emerald-400 tracking-widest">Kilogrammes estimés</p>
            </div>

            <!-- Mini Chart / Abstract Visual -->
            <div class="w-full h-40 pt-4">
              <canvas ref="chartRef"></canvas>
            </div>
          </div>
        </div>
        
        <div class="bg-emerald-50 rounded-[2rem] p-6 text-[#10b481] border border-emerald-100/50 flex items-center justify-between">
            <div class="space-y-1">
              <p class="text-[10px] font-black uppercase tracking-widest opacity-60">Historique</p>
              <p class="text-sm font-bold">{{ yieldRecords.length }} récoltes enregistrées</p>
            </div>
            <i class="bx bx-history text-2xl"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
import Chart from "chart.js/auto";

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const parcelCrop = ref<any>({});
const forecastData = ref<any>(null);
const yieldRecords = ref<any[]>([]);
const chartRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  try {
    const data: any = await apiFetch(`/api/parcel-crops/${route.params.id}//`);
    const parcels: any = await apiFetch('/api/parcels/');
    const parcel = parcels.find((p: any) => p.uuid === data.parcel);
    
    parcelCrop.value = { ...data, parcel_name: parcel?.parcel_name || data.parcel };
    forecastData.value = await apiFetch(`/forecast/${route.params.id}/`);
    
    const allYields: any = await apiFetch('/api/yield-records/');
    yieldRecords.value = allYields.filter((y: any) => y.parcelCrop === parcelCrop.value.id);

    await nextTick();
    renderChart();
  } catch (err) {}
});

const renderChart = () => {
  if (!chartRef.value || !yieldRecords.value.length) return;
  const labels = yieldRecords.value.map((y) => formatDateShort(y.date));
  const data = yieldRecords.value.map((y) => y.yield_amount);

  if (chartInstance) chartInstance.destroy();
  const ctx = chartRef.value.getContext("2d");
  if (!ctx) return;

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Rendement (kg)",
        data,
        borderColor: "#10b481",
        backgroundColor: "rgba(16, 180, 129, 0.1)",
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointBackgroundColor: "#10b481",
        pointRadius: 0,
        pointHoverRadius: 6,
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
          padding: 12,
          cornerRadius: 12,
          displayColors: false
        }
      },
      scales: {
        x: { display: false },
        y: { display: false }
      },
    },
  });
};

const formatDate = (date: string | null) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "long", day: "numeric" });
};

const formatDateShort = (date: string | null) => {
  if (!date) return "";
  return new Date(date).toLocaleDateString(locale.value, { month: "short", day: "numeric" });
};

const statusColorClass = (status: string | undefined) => {
  switch (status) {
    case "Planned": return "bg-sky-50 text-sky-600 border-sky-100";
    case "Planted": return "bg-emerald-50 text-emerald-600 border-emerald-100";
    case "Growing": return "bg-amber-50 text-amber-600 border-amber-100";
    case "Harvested": return "bg-gray-50 text-gray-600 border-gray-100";
    case "Failed": return "bg-rose-50 text-rose-600 border-rose-100";
    default: return "bg-gray-50 text-gray-400 border-gray-100";
  }
};

const getStatusProgress = (status: string | undefined) => {
  const steps: Record<string, number> = { "Planned": 10, "Planted": 40, "Growing": 70, "Harvested": 100, "Failed": 100 };
  return steps[status || ""] || 0;
};

const goBack = () => router.push("/farmer/parcel-crops");
</script>

<style scoped>
</style>
