<template>
  <div class="p-6 space-y-8 max-w-[1600px] mx-auto">

    <!-- ===== Indicateur de chargement global ===== -->
    <div v-if="isLoading" class="fixed inset-0 bg-white/60 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="flex flex-col items-center gap-4">
        <i class="bx bx-loader-alt animate-spin text-5xl text-[#10b481]"></i>
        <p class="text-sm font-bold text-[#112830]">Chargement des données...</p>
      </div>
    </div>

    <!-- ===== KPI GRID PREMIUM ===== -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="kpi in biKpis" :key="kpi.label" 
           class="group bg-white p-8 rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all duration-500 relative overflow-hidden">
        <div :class="['absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl opacity-0 group-hover:opacity-10 transition-opacity duration-700', kpi.bgLight]"></div>
        
        <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mb-6 shadow-lg transition-transform duration-500 group-hover:scale-110', kpi.bg, kpi.text]">
          <i :class="[kpi.icon, 'text-2xl']"></i>
        </div>
        
        <div class="space-y-1">
          <p class="text-sm font-bold text-gray-400 uppercase tracking-widest">{{ kpi.label }}</p>
          <div class="flex items-baseline gap-2">
            <h3 class="text-3xl font-black text-[#112830]">{{ kpi.value }}</h3>
            <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', kpi.trendUp ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
              {{ kpi.trendUp ? '↑' : '↓' }} {{ kpi.trend }}
            </span>
          </div>
        </div>
        
        <div class="mt-6 h-1 w-full bg-gray-50 rounded-full overflow-hidden">
          <div :class="['h-full transition-all duration-1000', kpi.barColor]" :style="{ width: kpi.progress + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- ===== CHARTS SECTIONS ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Production Trend -->
      <div class="lg:col-span-2 bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h3 class="text-2xl font-bold text-[#112830]">Volume de Production</h3>
            <p class="text-sm text-gray-400 font-medium">
              {{ activeTimeframe === 'Mois' ? 'Évolution journalière du mois en cours (en kg)' : 'Évolution annuelle par type de culture (en kg)' }}
            </p>
          </div>
          <div class="flex bg-gray-50 p-1.5 rounded-2xl border border-gray-100">
            <button 
              v-for="v in timeframeOptions" 
              :key="v.label" 
              @click="setTimeframe(v)"
              class="px-5 py-2 rounded-xl text-xs font-bold transition-all"
              :class="activeTimeframe === v.label ? 'bg-[#112830] text-white shadow-lg' : 'text-gray-400 hover:text-gray-600'">
              {{ v.label }}
            </button>
          </div>
        </div>
        
        <div class="h-[400px] relative">
          <div v-if="!chartReady || isRefreshing" class="absolute inset-0 flex items-center justify-center">
            <i class="bx bx-loader-alt animate-spin text-4xl text-[#10b481]"></i>
          </div>
          <component 
            v-else
            :is="BarChart" 
            :data="productionChartData" 
            :options="commonChartOptions"
          />
        </div>
      </div>

      <!-- Focus Impact — dynamique -->
      <div class="bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm flex flex-col">
        <h3 class="text-2xl font-bold text-[#112830] mb-2">Focus Impact</h3>
        <p class="text-sm text-gray-400 font-medium mb-8">Répartition par culture principale</p>
        
        <div class="flex-1 flex flex-col justify-center">
          <div class="h-[250px] mb-8">
            <component 
              v-if="chartReady && impactChartData.datasets[0].data.length > 0"
              :is="DoughnutChart" 
              :data="impactChartData" 
              :options="doughnutOptions"
            />
            <div v-else class="h-full flex items-center justify-center">
              <i class="bx bx-loader-alt animate-spin text-3xl text-[#10b481]"></i>
            </div>
          </div>
          
          <div class="space-y-4">
            <div v-for="item in impactMetrics" :key="item.label" class="flex items-center justify-between p-4 rounded-3xl bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer group">
              <div class="flex items-center gap-3">
                <div :class="['w-3 h-3 rounded-full shadow-sm', item.color]"></div>
                <span class="text-sm font-bold text-[#112830]">{{ item.label }}</span>
              </div>
              <span class="text-sm font-black text-gray-400 group-hover:text-[#10b481]">{{ item.pct }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== GEOGRAPHIC & DISTRIBUTION ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Region Analysis -->
      <div class="bg-[#112830] rounded-[2.5rem] p-8 text-white relative overflow-hidden group">
        <div class="relative z-10 flex flex-col h-full">
          <h3 class="text-2xl font-bold mb-2">Analyse Régionale</h3>
          <p class="text-white/40 text-sm mb-8">Performance topographique des coopératives</p>
          
          <div class="flex-1 space-y-6">
            <div v-if="regions.length === 0" class="flex items-center justify-center h-32 text-white/50 text-sm font-medium">
              Aucune donnée régionale disponible
            </div>
            <div v-for="region in regions" :key="region.name" class="space-y-2">
              <div class="flex justify-between text-sm font-bold text-white/80">
                <span>{{ region.name }}</span>
                <span>{{ region.total.toLocaleString() }} kg</span>
              </div>
              <div class="h-2 bg-white/5 rounded-full overflow-hidden border border-white/5">
                <div class="h-full bg-gradient-to-r from-[#10b481]/60 to-[#10b481] rounded-full transition-all duration-[2000ms] group-hover:w-[var(--w)]" 
                     :style="{ '--w': region.pct + '%', width: '0%' }"></div>
              </div>
            </div>
          </div>
          
          <!-- <button 
            @click="navigateToMap"
            class="mt-8 py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-sm font-bold transition-all border border-white/10 flex items-center justify-center gap-2">
            Ouvrir la Carte Interactive <i class="bx bx-right-arrow-alt"></i>
          </button> -->
        </div>
        
        <i class="bx bx-map-alt absolute top-10 right-10 text-[10rem] text-white/5 pointer-events-none group-hover:text-white/10 transition-colors duration-1000"></i>
      </div>

      <!-- AI Recommendations — dynamiques -->
      <div class="bg-gradient-to-tr from-[#10b481]/5 to-[#219ebc]/5 rounded-[2.5rem] p-8 border border-[#10b481]/10 flex flex-col">
        <div class="flex items-center gap-4 mb-8">
          <div class="w-14 h-14 rounded-2xl bg-white shadow-xl flex items-center justify-center text-[#10b481]">
            <i class="bx bxs-bot text-3xl"></i>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-[#112830]">IA Insights</h3>
            <p class="text-sm text-gray-400 font-medium italic">Recommandations basées sur vos données</p>
          </div>
        </div>
        
        <div class="space-y-4 flex-1">
          <div v-if="aiInsights.length === 0" class="flex items-center justify-center h-32 text-gray-400 text-sm font-medium">
            <i class="bx bx-loader-alt animate-spin text-2xl mr-2"></i> Chargement des recommandations...
          </div>
          <div v-for="insight in aiInsights" :key="insight.id" class="p-6 bg-white rounded-[2rem] shadow-sm border border-gray-50 hover:border-[#10b481]/30 transition-all cursor-pointer group">
            <div class="flex gap-4">
              <div class="flex-shrink-0 mt-1">
                <i :class="['bx text-xl', insight.icon, insight.iconColor]"></i>
              </div>
              <div>
                <h4 class="font-bold text-[#112830] mb-1 group-hover:text-[#10b481] transition-colors">{{ insight.title }}</h4>
                <p class="text-sm text-gray-500 leading-relaxed">{{ insight.text }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- <button 
          @click="navigateToOrg"
          class="mt-8 py-5 bg-[#112830] text-white rounded-[2rem] font-bold shadow-xl hover:shadow-[#112830]/20 hover:-translate-y-1 transition-all">
          Consulter le Rapport Global
        </button> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, shallowRef } from 'vue';
import { useApi } from '~/composables/useApi';
import { useRouter } from 'vue-router';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const router = useRouter();

// --- STATE ---
const orgName = ref('Business Intelligence');
const biKpis = ref<any[]>([]);
const productionChartData = ref<any>({ labels: [], datasets: [] });
const regions = ref<any[]>([]);
const impactChartData = ref<any>({ labels: [], datasets: [{ data: [], backgroundColor: [], borderWidth: 0, hoverOffset: 20 }] });
const impactMetrics = ref<any[]>([]);
const aiInsights = ref<any[]>([]);

const activeTimeframe = ref('Année');
const chartReady = ref(false);
const isLoading = ref(false);
const isRefreshing = ref(false);

const BarChart = shallowRef<any>(null);
const DoughnutChart = shallowRef<any>(null);

// Options de filtre
const timeframeOptions = [
  { label: 'Année', value: 'annee' },
  { label: 'Mois',  value: 'mois'  },
];

// Fallback KPIs (affichés tant que les données backend ne sont pas chargées)
const fallbackKpis = [
  { label: 'Volume Total',         value: '—',  trend: '—', trendUp: true,  progress: 0,   icon: 'bx bx-package',   bg: 'bg-emerald-500', bgLight: 'bg-emerald-400', text: 'text-white', barColor: 'bg-emerald-500' },
  { label: 'Revenu Estimé',        value: '—',  trend: '—', trendUp: true,  progress: 0,   icon: 'bx bx-money',     bg: 'bg-blue-500',    bgLight: 'bg-blue-400',    text: 'text-white', barColor: 'bg-blue-500' },
  { label: 'Groupes Actifs',value: '—',  trend: '—', trendUp: false, progress: 0,   icon: 'bx bx-buildings', bg: 'bg-amber-500',   bgLight: 'bg-amber-400',   text: 'text-white', barColor: 'bg-amber-500' },
  { label: 'Membres Actifs',       value: '—',  trend: '—', trendUp: true,  progress: 0,   icon: 'bx bx-user',      bg: 'bg-[#10b481]',   bgLight: 'bg-[#10b481]',   text: 'text-white', barColor: 'bg-[#10b481]' },
];

const commonChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { 
      padding: 15,
      backgroundColor: '#112830',
      titleFont: { size: 14, weight: 'bold' },
      cornerRadius: 15
    }
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { weight: 'bold' }, color: '#9ca3af' } },
    y: { border: { dash: [5, 5] }, grid: { color: '#f3f4f6' }, ticks: { color: '#9ca3af' } }
  }
};

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: { legend: { display: false } }
};

// --- ACTIONS ---
async function setTimeframe(option: { label: string; value: string }) {
  if (activeTimeframe.value === option.label) return;
  activeTimeframe.value = option.label;
  isRefreshing.value = true;
  await fetchData(option.value);
  isRefreshing.value = false;
}

function navigateToMap() {
  router.push('/parcels');
}

function navigateToOrg() {
  router.push('/group');
}

async function fetchData(timeframe: string = 'annee') {
  try {
    const data: any = await apiFetch(`/api/dashboard/bi_dashboard/?timeframe=${timeframe}`);
    
    biKpis.value = data.kpis?.length ? data.kpis : fallbackKpis;
    productionChartData.value = data.production_chart;
    regions.value = data.regions ?? [];
    orgName.value = data.org_name ?? 'Business Intelligence';
    
    // Focus Impact (répartition par culture)
    if (data.impact?.chart_data) {
      impactChartData.value = data.impact.chart_data;
    }
    if (data.impact?.metrics) {
      impactMetrics.value = data.impact.metrics;
    }
    
    // IA Insights
    if (data.ai_insights) {
      aiInsights.value = data.ai_insights;
    }

  } catch (err) {
    console.error('Error fetching BI data:', err);
    biKpis.value = fallbackKpis;
  }
}

onMounted(async () => {
  isLoading.value = true;
  biKpis.value = fallbackKpis;

  const [chartjs, vueChartjs] = await Promise.all([
    import('chart.js'),
    import('vue-chartjs')
  ]);
  
  chartjs.Chart.register(
    chartjs.CategoryScale,
    chartjs.LinearScale,
    chartjs.BarElement,
    chartjs.ArcElement,
    chartjs.Title,
    chartjs.Tooltip,
    chartjs.Legend
  );
  
  BarChart.value = vueChartjs.Bar;
  DoughnutChart.value = vueChartjs.Doughnut;
  
  await fetchData('annee');
  chartReady.value = true;
  isLoading.value = false;
});
</script>

<style scoped>
.group:hover div[style*="--w"] {
  width: var(--w) !important;
}
</style>
