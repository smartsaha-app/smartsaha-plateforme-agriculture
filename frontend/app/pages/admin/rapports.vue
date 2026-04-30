<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto text-[#112830]">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold">Reporting & Intelligence</h1>
        <p class="text-gray-500 font-medium">Générez des rapports consolidés pour vos investisseurs, partenaires et audits.</p>
      </div>
      <div class="flex bg-white p-1 rounded-2xl border border-gray-100 shadow-sm">
        <button class="px-6 py-2 bg-[#112830] text-white rounded-xl text-xs font-bold shadow-lg">Mes Rapports</button>
        <button class="px-6 py-2 text-gray-400 hover:text-[#112830] rounded-xl text-xs font-bold transition-all">Modèles</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- ===== GENERATION PANEL ===== -->
      <div class="lg:col-span-1 bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm space-y-6">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-[#10b481] flex items-center justify-center text-2xl">
            <i class="bx bx-cog"></i>
          </div>
          <h3 class="text-xl font-bold">Configuration</h3>
        </div>

        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Type de Rapport</label>
            <select v-model="selectedType" class="w-full p-4 bg-gray-50 rounded-2xl border-none font-bold text-sm outline-none focus:ring-2 focus:ring-[#10b481]/30 appearance-none cursor-pointer overflow-hidden">
              <option value="IMPACT">Impact & Social</option>
              <option value="PROGRESS">Rendement & Production</option>
              <option value="FINANCIAL">Bilan Financier</option>
              <option value="AUDIT">Conformité Audit</option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Périmètre (Groupe/Région)</label>
            <select class="w-full p-4 bg-gray-50 rounded-2xl border-none font-bold text-sm outline-none focus:ring-2 focus:ring-[#10b481]/30 appearance-none cursor-pointer">
              <option>Organisation entière</option>
              <option>Direction Vakinankaratra</option>
              <option>Coopérative Analamanga</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-3">
             <div class="space-y-1">
               <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Début</label>
              <input v-model="dateStart" type="date" class="w-full p-4 bg-gray-50 rounded-2xl border-none font-bold text-[10px] outline-none" />
             </div>
             <div class="space-y-1">
               <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Fin</label>
               <input v-model="dateEnd" type="date" class="w-full p-4 bg-gray-50 rounded-2xl border-none font-bold text-[10px] outline-none" />
             </div>
          </div>
        </div>

        <div class="p-4 bg-emerald-50 rounded-2xl border border-emerald-100 flex items-center gap-3">
          <i class="bx bx-check-circle text-emerald-600"></i>
          <span class="text-[10px] font-bold text-emerald-700 leading-tight">Votre rapport sera généré au format PDF et Excel dynamiquement.</span>
        </div>

        <button @click="generateReport" :disabled="isGenerating" 
                class="w-full py-5 bg-[#112830] text-white rounded-[1.5rem] font-black shadow-xl shadow-[#112830]/10 hover:bg-[#10b481] transition-all duration-500 flex items-center justify-center gap-3">
          <i :class="['bx text-xl', isGenerating ? 'bx-loader-alt animate-spin' : 'bx-rocket']"></i>
          {{ isGenerating ? 'Génération...' : 'Lancer l\'export' }}
        </button>
      </div>

      <!-- ===== REPORT TYPES CARDS ===== -->
      <div class="lg:col-span-2 space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="t in reportTypes" :key="t.name" class="group bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all cursor-pointer relative overflow-hidden">
            <div :class="['absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity', t.color]">
              <i :class="[t.icon, 'text-6xl']"></i>
            </div>
            <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl mb-4', t.bg, t.color]">
              <i :class="t.icon"></i>
            </div>
            <h4 class="font-black text-lg mb-1">{{ t.name }}</h4>
            <p class="text-xs text-gray-400 font-medium leading-relaxed">{{ t.desc }}</p>
          </div>
        </div>

        <!-- ===== HISTORY TABLE ===== -->
        <div class="bg-white rounded-[2.5rem] p-8 border border-gray-100 shadow-sm">
           <h3 class="font-black text-xl mb-6">Archives Récentes</h3>
           <div class="overflow-x-auto">
             <table class="w-full">
               <thead>
                 <tr class="text-left border-b border-gray-50">
                    <th class="pb-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Document</th>
                    <th class="pb-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Période</th>
                    <th class="pb-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Format</th>
                    <th class="pb-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
                    <th class="pb-4"></th>
                 </tr>
               </thead>
               <tbody class="divide-y divide-gray-50">
                 <tr v-for="history in reportsHistory" :key="history.id" class="group hover:bg-gray-50/50 transition-colors">
                   <td class="py-5">
                     <div class="flex items-center gap-3">
                       <i class="bx bxs-file-pdf text-rose-500 text-xl"></i>
                       <span class="text-sm font-bold group-hover:text-[#10b481] transition-colors">{{ history.name }}</span>
                     </div>
                   </td>
                   <td class="py-5 text-xs text-gray-500 font-medium">{{ history.period }}</td>
                   <td class="py-5">
                     <span class="px-2 py-0.5 bg-gray-100 text-gray-400 rounded-lg text-[9px] font-black">PDF</span>
                   </td>
                   <td class="py-5">
                     <span :class="['px-2 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest', history.status === 'OK' ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600']">
                       {{ history.status === 'OK' ? 'Disponible' : 'Erreur' }}
                     </span>
                   </td>
                   <td class="py-5 text-right">
                      <a v-if="history.file" :href="history.file" target="_blank" class="w-8 h-8 rounded-lg bg-gray-50 hover:bg-[#112830] hover:text-white transition-all flex items-center justify-center">
                        <i class="bx bx-download"></i>
                      </a>
                      <button v-else @click="alert('Le fichier est en cours de génération ou non disponible.')" class="w-8 h-8 rounded-lg bg-gray-50 text-gray-300 cursor-not-allowed">
                        <i class="bx bx-time"></i>
                      </button>
                   </td>
                 </tr>
               </tbody>
             </table>
           </div>
           
           <!-- Pagination Footer -->
           <div v-if="!isLoading && totalCount > 20" class="mt-6 border-t border-gray-50 pt-4">
             <PaginationBase 
               :totalCount="totalCount" 
               :perPage="20" 
               v-model:currentPage="currentPage" 
               @change-page="(p) => currentPage = p" 
             />
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';
import PaginationBase from '~/components/ui/PaginationBase.vue';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const authStore = useAuthStore();

const selectedType = ref('PROGRESS');
const dateStart = ref('');
const dateEnd = ref('');
const isGenerating = ref(false);
const isLoading = ref(true);
const totalCount = ref(0);
const currentPage = ref(1);

const reportTypes = [
  { id: 'PROGRESS', name: 'Rapport d’avancement', desc: 'Suivi hebdomadaire des activités terrain et logs de production.', icon: 'bx bx-line-chart', bg: 'bg-emerald-50', color: 'text-emerald-600' },
  { id: 'IMPACT', name: 'Rapport d’impact', desc: 'Analyse des KPIs annuels pour les investisseurs et certifications.', icon: 'bx bx-world', bg: 'bg-blue-50', color: 'text-blue-600' },
  { id: 'FINANCIAL', name: 'Rapport financier', desc: 'Bilan complet des coûts intrants et revenus de vente estimés.', icon: 'bx bx-money', bg: 'bg-amber-50', color: 'text-amber-600' },
  { id: 'AUDIT', name: 'Rapport d’audit', desc: 'Preuves de conformité pour le renouvellement des labels.', icon: 'bx bx-shield-quarter', bg: 'bg-rose-50', color: 'text-rose-600' },
];

const reportsHistory = ref<any[]>([]);
const organisationId = ref<number | null>(null);

async function fetchUserData() {
  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    organisationId.value = data.organisation_id || 1; // Default to 1 if not found
  } catch (err) {
    console.error("Erreur fetchUserData:", err);
  }
}

async function fetchHistory() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch(`/api/suivi-evaluation/api/reporting/?page=${currentPage.value}`);
    const results = data.results || data || [];
    totalCount.value = data.count || results.length;
    reportsHistory.value = results.map((r: any) => ({
      id: r.uuid,
      name: r.name,
      period: `${r.period_start} - ${r.period_end}`,
      status: r.status === 'APPROVED' ? 'OK' : 'PENDING',
      file: r.attachments?.[0]?.file_path || null
    }));
  } catch (err) {
    console.error("Erreur fetchHistory:", err);
  } finally {
    isLoading.value = false;
  }
}

watch(currentPage, () => {
  fetchHistory();
});

async function generateReport() {
  if (!dateStart.value || !dateEnd.value) {
    alert("Veuillez sélectionner une période.");
    return;
  }
  
  if (!organisationId.value) {
    await fetchUserData();
  }
  
  isGenerating.value = true;
  try {
    await apiFetch('/api/suivi-evaluation/api/reporting/', {
      method: 'POST',
      body: {
        name: `Rapport ${selectedType.value} ${new Date().toLocaleDateString()}`,
        type: selectedType.value,
        period_start: dateStart.value,
        period_end: dateEnd.value,
        organisation_id: organisationId.value
      }
    });
    alert("Rapport créé avec succès.");
    fetchHistory();
  } catch (err) {
    console.error("Erreur generateReport:", err);
    alert("Erreur lors de la création du rapport.");
  } finally {
    isGenerating.value = false;
  }
}

onMounted(async () => {
  await Promise.all([
    fetchHistory(),
    fetchUserData()
  ]);
});
</script>
