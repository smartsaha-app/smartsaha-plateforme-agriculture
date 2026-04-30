<template>
  <div class="p-6 space-y-8 max-w-[1600px] mx-auto">
    <!-- ===== HEADER WITH EXPORT BUTTON ===== -->
    <!-- <div class="flex justify-end mb-4">
      <button 
        @click="exportMarketplaceReport" 
        class="flex items-center gap-2 bg-[#10b481] hover:bg-[#0da070] text-white font-bold py-2 px-6 rounded-full shadow hover:-translate-y-1 transition-all duration-300"
      >
        <i class='bx bx-export text-xl'></i> Export Rapport Marketplace (Excel)
      </button>
    </div> -->
    <!-- ===== GOUVERNANCE SECTION ===== -->
    <div class="space-y-6">
      <div class="flex items-center gap-4 mb-2">
        <div class="w-2 h-8 bg-[#10b481] rounded-full"></div>
        <h2 class="text-2xl font-black text-[#112830]">Gouvernance & Réseau</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div v-for="metric in globalMetrics.slice(0, 4)" :key="metric.label" 
             class="group bg-white p-8 rounded-[3rem] border border-gray-50 shadow-sm hover:shadow-[0_20px_50px_rgba(0,0,0,0.05)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden">
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-8">
              <div :class="['w-16 h-16 rounded-[1.5rem] flex items-center justify-center text-3xl shadow-lg transition-all duration-700 group-hover:scale-110 group-hover:rotate-6', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">{{ metric.label }}</p>
            <h3 class="text-4xl font-black text-[#112830] tracking-tighter">{{ metric.value }}</h3>
          </div>
          <!-- Card Background Accent -->
          <div :class="['absolute -bottom-10 -right-10 w-32 h-32 rounded-full opacity-[0.03] group-hover:opacity-[0.08] transition-opacity duration-700', metric.bg]"></div>
        </div>
      </div>
    </div>

    <!-- ===== EXPLOITATION SECTION ===== -->
    <div class="space-y-6 pt-8">
      <div class="flex items-center gap-4 mb-2">
        <div class="w-2 h-8 bg-blue-500 rounded-full"></div>
        <h2 class="text-2xl font-black text-[#112830]">Ressources & Opérations</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div v-for="metric in globalMetrics.slice(4, 8)" :key="metric.label" 
             class="group bg-gray-50/50 backdrop-blur-sm p-8 rounded-[3rem] border border-gray-100 shadow-sm hover:bg-white hover:shadow-[0_20px_50px_rgba(0,0,0,0.05)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden">
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-8">
              <div :class="['w-16 h-16 rounded-[1.5rem] flex items-center justify-center text-3xl shadow-lg transition-all duration-700 group-hover:scale-110 group-hover:-rotate-6', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">{{ metric.label }}</p>
            <h3 class="text-4xl font-black text-[#112830] tracking-tighter">{{ metric.value }}</h3>
          </div>
          <!-- Card Background Accent -->
          <div :class="['absolute -bottom-10 -right-10 w-32 h-32 rounded-full opacity-[0.03] group-hover:opacity-[0.08] transition-opacity duration-700', metric.bg]"></div>
        </div>
      </div>
    </div>
    <!-- ===== MARKETPLACE SECTION ===== -->
    <div class="space-y-6 pt-8" v-if="marketplaceMetrics.length">
      <div class="flex items-center gap-4 mb-2">
        <div class="w-2 h-8 bg-purple-500 rounded-full"></div>
        <h2 class="text-2xl font-black text-[#112830]">Marketplace & Commerce</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div v-for="metric in marketplaceMetrics" :key="metric.label" 
             class="group bg-purple-50/30 backdrop-blur-sm p-8 rounded-[3rem] border border-purple-100 shadow-sm hover:bg-white hover:shadow-[0_20px_50px_rgba(0,0,0,0.05)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden">
          <div class="relative z-10">
            <div class="flex justify-between items-start mb-8">
              <div :class="['w-16 h-16 rounded-[1.5rem] flex items-center justify-center text-3xl shadow-lg transition-all duration-700 group-hover:scale-110 group-hover:rotate-6', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">{{ metric.label }}</p>
            <h3 class="text-4xl font-black text-[#112830] tracking-tighter">{{ metric.value }}</h3>
          </div>
          <div :class="['absolute -bottom-10 -right-10 w-32 h-32 rounded-full opacity-[0.03] group-hover:opacity-[0.08] transition-opacity duration-700', metric.bg]"></div>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();

// --- STATE ---
const globalMetrics = ref<any[]>([]);
const marketplaceMetrics = ref<any[]>([]);


async function fetchData() {
  try {
    const data: any = await apiFetch('/api/dashboard/admin_dashboard/');
    globalMetrics.value = data.metrics.map((m: any) => ({
      label:   m.title,
      value:   m.value,
      icon:    m.icon,
      bg:      m.bg || 'bg-gray-50',
      text:    m.color || 'text-gray-600'
    }));

    const mk_data: any = await apiFetch('/api/dashboard/marketplace_stats/');
    marketplaceMetrics.value = [
      { label: 'Vendeurs Actifs', value: mk_data.active_sellers, icon: 'bx bx-store-alt', bg: 'bg-purple-100', text: 'text-purple-600' },
      { label: 'Annonces Total', value: mk_data.total_posts, icon: 'bx bx-package', bg: 'bg-purple-100', text: 'text-purple-600' },
      { label: 'Commandes Effectuées', value: mk_data.total_orders, icon: 'bx bx-cart', bg: 'bg-green-100', text: 'text-green-600' },
      { label: 'Volume (MGA)', value: mk_data.marketplace_volume.toLocaleString(), icon: 'bx bx-line-chart', bg: 'bg-blue-100', text: 'text-blue-600' }
    ];
  } catch (err) {
    console.error("Error fetching admin data:", err);
  }
}

async function exportMarketplaceReport() {
  try {
    const config = useRuntimeConfig();
    const baseUrl = config.public.apiBase || 'http://127.0.0.1:8000';
    window.location.href = `${baseUrl}/api/dashboard/export_marketplace_report/`;
  } catch(err) {
    console.error("Export failed:", err);
  }
}

// ✅ onMounted correctement fermé
onMounted(async () => {
  await fetchData();
});
</script>