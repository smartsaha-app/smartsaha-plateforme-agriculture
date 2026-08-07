<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

<!-- ===== BANNIÈRE DE BIENVENUE ADMIN ===== -->
  <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#112830] via-[#163540] to-[#10b481] p-6 md:p-8 text-white shadow-xl mb-8">
    <!-- Cercles décoratifs en arrière-plan -->
    <div class="absolute -right-10 -bottom-10 w-48 h-48 rounded-full bg-[#10b481]/20 blur-2xl pointer-events-none"></div>
    <div class="absolute right-1/3 -top-10 w-32 h-32 rounded-full bg-emerald-400/10 blur-xl pointer-events-none"></div>

    <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
      
      <!-- Texte & Titre Admin -->
      <div class="space-y-2 max-w-xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-emerald-300 text-xs font-semibold">
          <span>Espace Administration</span>
        </div>
        
        <h1 class="text-2xl md:text-3xl font-black tracking-tight">
          Bienvenue, <span class="text-[#10b481]">{{ useAuthStore().firstName }}</span>
        </h1>
        
        <p class="text-gray-300 text-sm md:text-base leading-relaxed">
          {{ t('admin.dashboardDesc') }}
        </p>
      </div>

      <!-- Actions & Fil d'Ariane -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 self-start lg:self-auto">

        <!-- Bouton Liste des Utilisateurs -->
        <NuxtLink 
          to="/admin/subscriptions"
          class="inline-flex items-center gap-2 px-4 py-2.5 bg-[#10b481] hover:bg-[#0e9f72] rounded-2xl text-xs font-bold text-white transition-all shadow-md active:scale-95"
        >
          <span>{{ t('admin.dashboardBtn') }}</span>
          <i class="bx bx-chevron-right text-base text-emerald-300"></i>
        </NuxtLink>
      </div>

    </div>
  </div>

    <!-- Loading -->
    <div v-if="isLoading" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="i in 8" :key="i" class="h-28 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
    </div>

    <template v-else>
      <!-- ===== GOUVERNANCE ===== -->
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-[#10b481] rounded-full"></div>
          <h2 class="text-sm font-black text-[#112830] uppercase tracking-widest">{{ t('admin.sectionGovernance') }}</h2>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="metric in globalMetrics.slice(0, 4)" :key="metric.label"
            class="group bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden">
            <div class="flex items-center justify-between mb-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg group-hover:scale-110 transition-transform', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ metric.label }}</p>
            <h3 class="text-2xl font-black text-[#112830]">{{ metric.value }}</h3>
            <div :class="['absolute -bottom-6 -right-6 w-20 h-20 rounded-full opacity-[0.04] group-hover:opacity-[0.08] transition-opacity', metric.bg]"></div>
          </div>
        </div>
      </div>

      <!-- ===== OPÉRATIONS ===== -->
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-blue-500 rounded-full"></div>
          <h2 class="text-sm font-black text-[#112830] uppercase tracking-widest">{{ t('admin.sectionOperations') }}</h2>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="metric in globalMetrics.slice(4, 8)" :key="metric.label"
            class="group bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden">
            <div class="flex items-center justify-between mb-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg group-hover:scale-110 transition-transform', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ metric.label }}</p>
            <h3 class="text-2xl font-black text-[#112830]">{{ metric.value }}</h3>
            <div :class="['absolute -bottom-6 -right-6 w-20 h-20 rounded-full opacity-[0.04] group-hover:opacity-[0.08] transition-opacity', metric.bg]"></div>
          </div>
        </div>
      </div>

      <!-- ===== MARKETPLACE ===== -->
      <div v-if="marketplaceMetrics.length" class="space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-1.5 h-6 bg-purple-500 rounded-full"></div>
          <h2 class="text-sm font-black text-[#112830] uppercase tracking-widest">{{ t('admin.sectionMarketplace') }}</h2>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="metric in marketplaceMetrics" :key="metric.label"
            class="group bg-white p-5 rounded-2xl border border-purple-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer relative overflow-hidden">
            <div class="flex items-center justify-between mb-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg group-hover:scale-110 transition-transform', metric.bg, metric.text]">
                <i :class="metric.icon"></i>
              </div>
            </div>
            <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ metric.label }}</p>
            <h3 class="text-2xl font-black text-[#112830]">{{ metric.value }}</h3>
            <div :class="['absolute -bottom-6 -right-6 w-20 h-20 rounded-full opacity-[0.04] group-hover:opacity-[0.08] transition-opacity', metric.bg]"></div>
          </div>
        </div>
      </div>

      <!-- ===== ACCÈS RAPIDES ===== -->
      <!-- <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <NuxtLink to="/admin/users"
          class="group bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all flex items-center gap-4 cursor-pointer">
          <div class="w-11 h-11 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center text-xl group-hover:bg-blue-500 group-hover:text-white transition-colors flex-shrink-0">
            <i class="bx bx-group"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-black text-[#112830]">{{ t('admin.usersLink') }}</p>
            <p class="text-xs text-gray-400">{{ t('admin.manageAccounts') }}</p>
          </div>
          <i class="bx bx-chevron-right text-gray-300 group-hover:text-[#10b481] transition-colors"></i>
        </NuxtLink>

        <NuxtLink to="/admin/audits"
          class="group bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all flex items-center gap-4 cursor-pointer">
          <div class="w-11 h-11 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center text-xl group-hover:bg-amber-500 group-hover:text-white transition-colors flex-shrink-0">
            <i class="bx bx-shield-quarter"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-black text-[#112830]">{{ t('admin.auditsLink') }}</p>
            <p class="text-xs text-gray-400">{{ t('admin.auditsLinkDesc') }}</p>
          </div>
          <i class="bx bx-chevron-right text-gray-300 group-hover:text-[#10b481] transition-colors"></i>
        </NuxtLink>

        <NuxtLink to="/admin/rapports"
          class="group bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all flex items-center gap-4 cursor-pointer">
          <div class="w-11 h-11 bg-rose-50 text-rose-500 rounded-xl flex items-center justify-center text-xl group-hover:bg-rose-500 group-hover:text-white transition-colors flex-shrink-0">
            <i class="bx bx-file-find"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-black text-[#112830]">{{ t('admin.reportsLink') }}</p>
            <p class="text-xs text-gray-400">{{ t('admin.reportsLinkDesc') }}</p>
          </div>
          <i class="bx bx-chevron-right text-gray-300 group-hover:text-[#10b481] transition-colors"></i>
        </NuxtLink>
      </div> -->
    </template>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { apiFetch } = useApi();

const isLoading          = ref(true);
const globalMetrics      = ref<any[]>([]);
const marketplaceMetrics = ref<any[]>([]);

async function fetchData() {
  try {
    const [dashData, mkData] = await Promise.all([
      apiFetch('/api/dashboard/admin_dashboard/'),
      apiFetch('/api/dashboard/marketplace_stats/'),
    ]);

    globalMetrics.value = (dashData as any).metrics.map((m: any) => ({
      label: m.title,
      value: m.value,
      icon:  m.icon,
      bg:    m.bg    || 'bg-gray-50',
      text:  m.color || 'text-gray-600',
    }));

    const mk = mkData as any;
    marketplaceMetrics.value = [
      { label: t('seller.statActiveProducts'), value: mk.active_sellers,  icon: 'bx bx-store-alt',  bg: 'bg-purple-100', text: 'text-purple-600' },
      { label: t('dashboard.myProducts'),      value: mk.total_posts,     icon: 'bx bx-package',    bg: 'bg-purple-100', text: 'text-purple-600' },
      { label: t('seller.statOrders'),         value: mk.total_orders,    icon: 'bx bx-cart',       bg: 'bg-green-100',  text: 'text-green-600'  },
      { label: 'Volume (MGA)',                 value: (mk.marketplace_volume || 0).toLocaleString('fr-MG'), icon: 'bx bx-line-chart', bg: 'bg-blue-100', text: 'text-blue-600' },
    ];
  } catch (err) {
    console.error('Erreur dashboard admin:', err);
  } finally {
    isLoading.value = false;
  }
}

// function exportReport() {
//   const config = useRuntimeConfig();
//   const base   = config.public.apiBase || 'http://127.0.0.1:8000';
//   window.open(`${base}/api/dashboard/export_marketplace_report/`, '_blank');
// }

onMounted(() => fetchData());
</script>