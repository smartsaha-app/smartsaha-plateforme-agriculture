<template>
  <div class="p-6 space-y-8 max-w-[1500px] mx-auto">

    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Suivi & Évaluation (S&E)</h1>
        <p class="text-gray-500 font-medium tracking-tight">
          Données en temps réel — rendements, producteurs, alertes terrain.
        </p>
      </div>
      <div class="flex gap-3 items-center">
        <!-- Période courante -->
        <span class="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-2xl font-bold text-sm">
          {{ stats?.current_period ?? '...' }}
        </span>
        <!-- Rafraîchir -->
        <button @click="fetchAll" :disabled="isLoading"
          class="px-4 py-3 bg-white border border-gray-100 text-gray-500 rounded-2xl font-bold hover:bg-gray-50 transition flex items-center gap-2 shadow-sm">
          <i :class="['bx bx-refresh text-lg', isLoading && 'animate-spin']"></i>
        </button>
        <!-- Ajouter indicateur -->
        <button @click="showAddModal = true"
          class="px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all duration-300 shadow-xl flex items-center gap-2">
          <i class="bx bx-plus-circle"></i> Ajouter un indicateur
        </button>
      </div>
    </div>

    <!-- ===== MODAL AJOUT INDICATEUR ===== -->
    <div v-if="showAddModal"
      class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
      <div class="bg-white w-full max-w-lg rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative">
        <button @click="showAddModal = false"
          class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center">
          <i class="bx bx-x text-2xl"></i>
        </button>
        <h2 class="text-2xl font-black text-[#112830]">Nouvel Indicateur</h2>
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Nom</label>
            <input v-model="newIndicator.name" type="text"
              class="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/30" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Catégorie</label>
              <select v-model="newIndicator.category"
                class="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/30">
                <option v-for="cat in categories" :key="cat.uuid" :value="cat.uuid">{{ cat.name }}</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Unité</label>
              <input v-model="newIndicator.unit" type="text" placeholder="ex: kg/m²"
                class="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/30" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Fréquence</label>
              <select v-model="newIndicator.frequency"
                class="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/30">
                <option value="daily">Quotidien</option>
                <option value="weekly">Hebdomadaire</option>
                <option value="monthly">Mensuel</option>
                <option value="quarterly">Trimestriel</option>
                <option value="yearly">Annuel</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest ml-2">Valeur cible</label>
              <input v-model.number="newIndicator.target_value" type="number" step="0.01" placeholder="optionnel"
                class="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-[#10b481]/30" />
            </div>
          </div>
        </div>
        <div class="flex gap-4 pt-4">
          <button @click="showAddModal = false" class="flex-1 py-4 text-gray-400 font-bold">Annuler</button>
          <button @click="createIndicator" :disabled="isSubmitting"
            class="flex-2 py-4 px-10 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all disabled:opacity-50">
            {{ isSubmitting ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="flex items-center justify-center py-24">
      <div class="flex flex-col items-center gap-4">
        <i class="bx bx-loader-alt animate-spin text-4xl text-[#10b481]"></i>
        <p class="text-gray-400 font-medium">Calcul des indicateurs en temps réel...</p>
      </div>
    </div>

    <!-- ===== ERREUR ===== -->
    <div v-else-if="loadError" class="bg-rose-50 border border-rose-100 rounded-[2rem] p-8 text-center">
      <i class="bx bx-error-circle text-4xl text-rose-400 mb-3 block"></i>
      <p class="font-bold text-rose-600">Impossible de charger les données</p>
      <p class="text-sm text-rose-400 mt-1">{{ loadError }}</p>
      <button @click="fetchAll" class="mt-4 px-6 py-2 bg-rose-500 text-white rounded-xl font-bold text-sm">
        Réessayer
      </button>
    </div>

    <template v-else-if="stats">

      <!-- ===== KPIs ===== -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div v-for="kpi in kpis" :key="kpi.label"
          class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-lg transition-all">
          <div class="flex justify-between items-start mb-4">
            <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-xl', kpi.bg, kpi.text]">
              <i :class="kpi.icon"></i>
            </div>
            <span :class="['text-[10px] font-black px-2 py-1 rounded-lg',
              kpi.trendUp ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
              {{ kpi.trendUp ? '↑' : '↓' }} {{ kpi.trend }}
            </span>
          </div>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">{{ kpi.label }}</p>
          <h3 class="text-2xl font-black text-[#112830]">{{ kpi.value }}</h3>
          <div class="mt-4 h-1.5 w-full bg-gray-50 rounded-full overflow-hidden">
            <div :class="['h-full transition-all duration-1000', kpi.barColor]"
              :style="{ width: kpi.progress + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- ===== CHARTS + SCORECARD ===== -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

        <!-- Chart rendements -->
        <div class="bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-black text-[#112830]">Évolution des Rendements</h3>
              <p class="text-xs text-gray-400 mt-1">
                Source : {{ stats.kpis.nb_recoltes }} récolte(s) enregistrée(s) · {{ stats.chart.unit }}
              </p>
            </div>
          </div>

          <div class="h-64 relative">
            <div v-if="!chartReady" class="absolute inset-0 flex items-center justify-center">
              <i class="bx bx-loader-alt animate-spin text-3xl text-[#10b481]"></i>
            </div>
            <div v-else-if="stats.chart.data.length === 0"
              class="absolute inset-0 flex flex-col items-center justify-center gap-2 text-gray-300">
              <i class="bx bx-line-chart text-5xl"></i>
              <p class="text-sm font-medium">Aucune récolte enregistrée</p>
              <p class="text-xs text-gray-400 text-center">
                Ajoutez des relevés de rendement dans le module Cultures
              </p>
            </div>
            <component v-else :is="LineChart" :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <!-- Scorecard Impact -->
        <div class="bg-[#112830] rounded-[2.5rem] p-8 text-white shadow-xl flex flex-col">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold">Scorecard Impact Parcelles</h3>
            <span class="text-xs text-white/40">
              {{ stats.scorecard.total_parcelles }} parcelle(s)
            </span>
          </div>

          <div v-if="stats.scorecard.total_parcelles > 0" class="space-y-6 flex-1">
            <!-- Conformité -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-bold text-white/80">Score de Conformité Moyen</span>
                <span class="text-sm font-black text-[#10b481]">
                  {{ stats.scorecard.avg_compliance }} / 100
                </span>
              </div>
              <div class="h-2 bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-emerald-600/50 to-[#10b481] rounded-full transition-all duration-1000"
                  :style="{ width: stats.scorecard.avg_compliance + '%' }"></div>
              </div>
              <p class="mt-1.5 text-[10px] text-white/40 italic">
                Basé sur les alertes météo par parcelle
              </p>
            </div>

            <!-- Rendement -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-bold text-white/80">Score de Rendement Moyen</span>
                <span class="text-sm font-black text-[#10b481]">
                  {{ stats.scorecard.avg_yield_score }} / 100
                </span>
              </div>
              <div class="h-2 bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-emerald-600/50 to-[#10b481] rounded-full transition-all duration-1000"
                  :style="{ width: stats.scorecard.avg_yield_score + '%' }"></div>
              </div>
              <p class="mt-1.5 text-[10px] text-white/40 italic">
                Rendement parcelle vs moyenne globale
              </p>
            </div>

            <!-- Risques -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-bold text-white/80">Parcelles à Faible Risque</span>
                <span class="text-sm font-black text-[#10b481]">
                  {{ stats.scorecard.low_risk_pct.toFixed(0) }}%
                </span>
              </div>
              <div class="h-2 bg-white/5 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-emerald-600/50 to-[#10b481] rounded-full transition-all duration-1000"
                  :style="{ width: stats.scorecard.low_risk_pct + '%' }"></div>
              </div>
              <p class="mt-1.5 text-[10px] text-white/40 italic">
                {{ stats.scorecard.risk_counts.LOW }} faible ·
                {{ stats.scorecard.risk_counts.MEDIUM }} moyen ·
                {{ stats.scorecard.risk_counts.HIGH }} élevé
              </p>
            </div>
          </div>

          <!-- Pas de parcelles -->
          <div v-else class="flex-1 flex flex-col items-center justify-center gap-3 text-white/30">
            <i class="bx bx-map text-4xl"></i>
            <p class="text-sm text-center">
              Aucune parcelle enregistrée.<br>
              Ajoutez des parcelles pour voir le scorecard.
            </p>
          </div>
        </div>
      </div>

      <!-- ===== INDICATEURS MANUELS + VALEURS ===== -->
      <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50 flex items-center justify-between bg-gray-50/30">
          <div>
            <h3 class="text-xl font-black text-[#112830]">Indicateurs Personnalisés</h3>
            <p class="text-xs text-gray-400 mt-1">
              {{ indicatorValues.length }} valeur(s) · {{ indicators.length }} indicateur(s) défini(s)
            </p>
          </div>
          <div class="flex gap-2">
            <select v-model="filterStatus"
              class="px-4 py-2 bg-white border border-gray-100 rounded-xl text-sm font-medium outline-none">
              <option value="">Tous les statuts</option>
              <option value="PENDING">En attente</option>
              <option value="VALIDATED">Validé</option>
              <option value="REJECTED">Rejeté</option>
              <option value="FIXED">Fixé</option>
            </select>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left border-b border-gray-50">
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Indicateur</th>
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Catégorie</th>
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Période</th>
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Valeur</th>
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Évolution</th>
                <th class="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Statut</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-if="filteredValues.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-300">
                  <i class="bx bx-table text-4xl mb-2 block"></i>
                  <p>Aucun indicateur personnalisé</p>
                  <p class="text-xs mt-1">Cliquez sur "Ajouter un indicateur" pour commencer</p>
                </td>
              </tr>
              <tr v-for="val in filteredValues" :key="val.uuid" class="hover:bg-gray-50 transition">
                <td class="px-6 py-4">
                  <p class="font-bold text-[#112830] text-sm">{{ getIndicatorName(val.indicator) }}</p>
                  <p class="text-xs text-gray-400">{{ getIndicatorUnit(val.indicator) }}</p>
                </td>
                <td class="px-6 py-4 text-xs text-gray-500">{{ getIndicatorCategory(val.indicator) }}</td>
                <td class="px-6 py-4 text-sm text-gray-700">{{ val.period }}</td>
                <td class="px-6 py-4 text-sm font-black text-[#112830]">{{ val.value }}</td>
                <td class="px-6 py-4">
                  <span v-if="val.evolution_pct !== null"
                    :class="['text-xs font-bold px-2 py-1 rounded-lg',
                      val.evolution_pct >= 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
                    {{ val.evolution_pct >= 0 ? '↑' : '↓' }} {{ Math.abs(val.evolution_pct).toFixed(1) }}%
                  </span>
                  <span v-else class="text-xs text-gray-300">—</span>
                </td>
                <td class="px-6 py-4">
                  <span :class="['text-[10px] font-black uppercase px-2 py-1 rounded', statusClass(val.status)]">
                    {{ statusLabel(val.status) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== ALERTES ===== -->
      <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50 flex items-center justify-between bg-gray-50/30">
          <div>
            <h3 class="text-xl font-black text-[#112830]">Alertes & Anomalies</h3>
            <p class="text-xs text-gray-400 mt-1">
              Rapports en brouillon · valeurs rejetées · alertes météo critiques
            </p>
          </div>
          <span class="text-sm font-bold"
            :class="stats.alerts.length > 0 ? 'text-rose-500' : 'text-emerald-500'">
            {{ stats.alerts.length }} alerte(s)
          </span>
        </div>

        <div v-if="stats.alerts.length === 0" class="p-12 text-center">
          <i class="bx bx-check-shield text-5xl mb-3 block text-emerald-300"></i>
          <p class="font-medium text-emerald-500">Aucune alerte active — tout est en ordre !</p>
        </div>

        <div v-else class="divide-y divide-gray-50">
          <div v-for="alert in stats.alerts" :key="alert.id"
            class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer">
            <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-xl flex-shrink-0', alertBg(alert.type)]">
              <i :class="alert.icon"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-1">
                <h4 class="font-bold text-[#112830]">{{ alert.title }}</h4>
                <span class="text-[9px] font-black uppercase text-white px-2 py-0.5 rounded"
                  :class="alertBadge(alert.type)">{{ alert.type }}</span>
              </div>
              <p class="text-sm text-gray-500">{{ alert.description }}</p>
              <div class="mt-2 flex items-center gap-4 text-[10px] font-bold text-gray-400">
                <span><i class="bx bx-time-five mr-1"></i>{{ alert.date }}</span>
                <span v-if="alert.location"><i class="bx bx-map-pin mr-1"></i>{{ alert.location }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, shallowRef, computed } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();

// ─── State ────────────────────────────────────────────────────────────────────
const isLoading  = ref(true);
const loadError  = ref('');
const stats      = ref<any>(null);          // réponse de /dashboard-stats/

const indicators      = ref<any[]>([]);
const indicatorValues = ref<any[]>([]);
const categories      = ref<any[]>([]);

const filterStatus    = ref('');
const showAddModal    = ref(false);
const isSubmitting    = ref(false);

const LineChart  = shallowRef<any>(null);
const chartReady = ref(false);

const newIndicator = ref({
  name: '', category: '', unit: '', frequency: 'monthly', target_value: null as number | null, code: '',
});

// ─── Fetch principal ──────────────────────────────────────────────────────────
async function fetchAll() {
  isLoading.value = true;
  loadError.value = '';
  try {
    const [dashRes, indRes, valRes, catRes] = await Promise.all([
      // Endpoint principal : stats calculées depuis les vraies données
      apiFetch('/api/suivi-evaluation/api/dashboard-stats/'),
      // Indicateurs personnalisés (table S&E)
      apiFetch('/api/suivi-evaluation/api/indicators/'),
      apiFetch('/api/suivi-evaluation/api/indicator-values/'),
      apiFetch('/api/suivi-evaluation/api/indicator-categories/'),
    ]);

    stats.value           = dashRes;
    indicators.value      = (indRes as any).results  ?? indRes  ?? [];
    indicatorValues.value = (valRes as any).results  ?? valRes  ?? [];
    categories.value      = (catRes as any).results  ?? catRes  ?? [];
  } catch (err: any) {
    loadError.value = err?.message ?? 'Erreur inconnue';
    console.error('Erreur fetchAll:', err);
  } finally {
    isLoading.value = false;
  }
}

// ─── KPIs calculés depuis stats.kpis ─────────────────────────────────────────
const kpis = computed(() => {
  if (!stats.value) return [];
  const k = stats.value.kpis;
  return [
    {
      label: 'Rendement Moyen',
      value: `${k.avg_yield} kg`,
      trend: `${k.nb_recoltes} récolte(s)`,
      trendUp: k.avg_yield > 0,
      progress: Math.min(k.avg_yield / 10, 100),
      icon: 'bx bx-leaf',
      bg: 'bg-emerald-50', text: 'text-emerald-600', barColor: 'bg-emerald-400',
    },
    {
      label: 'Producteurs Actifs',
      value: k.nb_membres_actifs.toString(),
      trend: `${k.nb_groupes_actifs} groupe(s)`,
      trendUp: k.nb_membres_actifs > 0,
      progress: Math.min(k.nb_membres_actifs * 2, 100),
      icon: 'bx bx-group',
      bg: 'bg-blue-50', text: 'text-blue-600', barColor: 'bg-blue-400',
    },
    {
      label: 'Cultures Actives',
      value: k.nb_cultures_actives.toString(),
      trend: `${k.nb_parcelles} parcelle(s)`,
      trendUp: k.nb_cultures_actives > 0,
      progress: Math.min(k.nb_cultures_actives * 5, 100),
      icon: 'bx bx-map-alt',
      bg: 'bg-amber-50', text: 'text-amber-600', barColor: 'bg-amber-400',
    },
    {
      label: 'Alertes Actives',
      value: k.nb_alertes.toString(),
      trend: `${k.nb_alertes_critiques} critique(s)`,
      trendUp: k.nb_alertes === 0,
      progress: Math.min(k.nb_alertes * 15, 100),
      icon: 'bx bx-error',
      bg: 'bg-rose-50', text: 'text-rose-600', barColor: 'bg-rose-400',
    },
  ];
});

// ─── Chart depuis stats.chart.data ───────────────────────────────────────────
const chartData = computed(() => {
  if (!stats.value?.chart?.data?.length) return null;
  const data = stats.value.chart.data;
  return {
    labels: data.map((d: any) => d.period),
    datasets: [
      {
        label: 'Rendement réel',
        data: data.map((d: any) => d.value),
        borderColor: '#10b481',
        backgroundColor: 'rgba(16,180,129,0.06)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#10b481',
        pointBorderWidth: 2,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { font: { weight: 'bold' }, color: '#9ca3af' } },
    y: { border: { dash: [5, 5] }, grid: { color: '#f3f4f6' }, ticks: { color: '#9ca3af' } },
  },
};

// ─── Lookups indicateurs ──────────────────────────────────────────────────────
const indicatorMap = computed(() => Object.fromEntries(indicators.value.map(i => [i.uuid, i])));
const categoryMap  = computed(() => Object.fromEntries(categories.value.map(c => [c.uuid, c])));

function getIndicatorName(uuid: string)     { return indicatorMap.value[uuid]?.name ?? '—'; }
function getIndicatorUnit(uuid: string)     { return indicatorMap.value[uuid]?.unit ?? ''; }
function getIndicatorCategory(uuid: string) {
  const catUuid = indicatorMap.value[uuid]?.category;
  return categoryMap.value[catUuid]?.name ?? '—';
}

// ─── Filtres table ────────────────────────────────────────────────────────────
const filteredValues = computed(() =>
  filterStatus.value
    ? indicatorValues.value.filter(v => v.status === filterStatus.value)
    : indicatorValues.value
);

// ─── Helpers statut ───────────────────────────────────────────────────────────
function statusLabel(s: string) {
  return { PENDING: 'En attente', VALIDATED: 'Validé', REJECTED: 'Rejeté', FIXED: 'Fixé' }[s] ?? s;
}
function statusClass(s: string) {
  return {
    PENDING:   'bg-amber-100 text-amber-700',
    VALIDATED: 'bg-emerald-100 text-emerald-700',
    REJECTED:  'bg-rose-100 text-rose-700',
    FIXED:     'bg-blue-100 text-blue-700',
  }[s] ?? 'bg-gray-100 text-gray-500';
}
function alertBg(t: string) {
  return { critical: 'bg-rose-50 text-rose-500', warning: 'bg-amber-50 text-amber-500', info: 'bg-blue-50 text-blue-500' }[t] ?? 'bg-gray-50 text-gray-400';
}
function alertBadge(t: string) {
  return { critical: 'bg-rose-500', warning: 'bg-amber-500', info: 'bg-blue-400' }[t] ?? 'bg-gray-400';
}

// ─── Créer indicateur ─────────────────────────────────────────────────────────
async function createIndicator() {
  if (!newIndicator.value.name || !newIndicator.value.category) {
    alert('Nom et Catégorie obligatoires.');
    return;
  }
  isSubmitting.value = true;
  try {
    newIndicator.value.code = newIndicator.value.name
      .toUpperCase().replace(/\s+/g, '_').replace(/[^A-Z0-9_]/g, '').substring(0, 50);
    await apiFetch('/api/suivi-evaluation/api/indicators/', {
      method: 'POST',
      body: {
        name: newIndicator.value.name,
        category: newIndicator.value.category,
        unit: newIndicator.value.unit || 'N/A',
        frequency: newIndicator.value.frequency,
        target_value: newIndicator.value.target_value || null,
        code: newIndicator.value.code,
      },
    });
    showAddModal.value = false;
    newIndicator.value = { name: '', category: '', unit: '', frequency: 'monthly', target_value: null, code: '' };
    await fetchAll();
  } catch (err) {
    alert("Erreur lors de la création. Vérifiez que le code est unique.");
  } finally {
    isSubmitting.value = false;
  }
}

// ─── Mount ────────────────────────────────────────────────────────────────────
onMounted(async () => {
  fetchAll();
  const chartjs    = await import('chart.js');
  const vueChartjs = await import('vue-chartjs');
  chartjs.Chart.register(
    chartjs.CategoryScale, chartjs.LinearScale, chartjs.PointElement,
    chartjs.LineElement, chartjs.Title, chartjs.Tooltip, chartjs.Legend, chartjs.Filler,
  );
  LineChart.value = vueChartjs.Line;
  chartReady.value = true;
});
</script>