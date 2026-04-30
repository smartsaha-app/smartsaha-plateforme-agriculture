<template>
  <div class="p-6 space-y-8 max-w-[1500px] mx-auto text-[#112830]">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight">Configuration Suivi & Évaluation (S&E)</h1>
        <p class="text-gray-500 font-medium">Définissez les standards de mesure, les indicateurs clés et les seuils d’alerte globaux.</p>
      </div>
      <button @click="showAddModal = true" class="px-8 py-4 bg-[#10b481] text-white rounded-[1.5rem] font-black hover:bg-[#0da06a] transition-all duration-300 shadow-xl shadow-[#10b481]/20 flex items-center gap-3 group">
        <i class="bx bx-plus-circle text-2xl group-hover:rotate-90 transition-transform duration-500"></i>
        Définir un Indicateur
      </button>
    </div>

    <!-- ===== KEY STANDARDS OVERVIEW ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="standard in standards" :key="standard.label" class="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm group hover:shadow-xl transition-all">
        <div class="flex justify-between items-start mb-6">
          <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center text-2xl shadow-sm', standard.bg, standard.color]">
            <i :class="standard.icon"></i>
          </div>
          <span class="text-[10px] font-black text-gray-300 uppercase tracking-widest">Global Std</span>
        </div>
        <p class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-1">{{ standard.label }}</p>
        <div class="flex items-baseline gap-2">
           <h3 class="text-3xl font-black text-[#112830]">{{ standard.value }}</h3>
           <span class="text-xs font-bold text-gray-400">{{ standard.unit }}</span>
        </div>
      </div>
    </div>

    <!-- ===== INDICATORS REPOSITORY ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <div class="p-10 border-b border-gray-50 flex flex-col md:flex-row md:items-center justify-between gap-6 bg-gray-50/30">
        <div>
          <h3 class="text-2xl font-black">Référentiel des Indicateurs</h3>
          <p class="text-sm text-gray-400 font-medium tracking-tight">Catalogue exhaustif des points de données collectés sur le terrain.</p>
        </div>
        <div class="flex gap-3">
           <div class="relative">
             <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
             <input v-model="searchQuery" type="text" placeholder="Rechercher..." class="pl-12 pr-6 py-3 bg-white border-none rounded-2xl text-sm font-medium focus:ring-2 focus:ring-[#10b481]/20 w-64 shadow-sm" />
           </div>
           <button class="w-12 h-12 rounded-2xl bg-white border border-gray-100 flex items-center justify-center text-gray-400 hover:text-[#112830] transition-all shadow-sm">
             <i class="bx bx-filter-alt"></i>
           </button>
        </div>
      </div>

      <div v-if="isLoading" class="p-20 text-center">
        <i class="bx bx-loader-alt animate-spin text-5xl text-gray-200"></i>
      </div>

      <div v-else class="px-10 pb-10">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left border-b border-gray-50">
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Indicateur & Code</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Catégorie</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Fréquence</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Cible Système</th>
                <th class="py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">État</th>
                <th class="py-6"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="indicator in filteredIndicators" :key="indicator.uuid" class="group hover:bg-gray-50/50 transition-colors">
                <td class="py-6">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-[#112830] group-hover:text-white transition-all">
                      <i class="bx bx-target-lock"></i>
                    </div>
                    <div>
                      <p class="font-bold text-sm text-[#112830]">{{ indicator.name }}</p>
                      <p class="text-[9px] font-mono text-gray-400 uppercase">{{ indicator.code }}</p>
                    </div>
                  </div>
                </td>
                <td class="py-6">
                  <span class="px-3 py-1 bg-blue-50 text-blue-500 rounded-xl text-[10px] font-black uppercase tracking-widest">{{ indicator.category_name || 'N/A' }}</span>
                </td>
                <td class="py-6 text-xs font-bold text-gray-500">
                  <div class="flex items-center gap-2">
                    <i class="bx bx-time-five"></i>
                    {{ indicator.frequency }}
                  </div>
                </td>
                <td class="py-6">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-black text-[#10b481]">{{ indicator.target_value }}</span>
                    <span class="text-[9px] font-bold text-gray-300 uppercase">{{ indicator.unit }}</span>
                  </div>
                </td>
                <td class="py-6">
                   <div class="flex items-center gap-2">
                     <span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,180,129,0.4)]"></span>
                     <span class="text-[9px] font-black uppercase tracking-widest text-emerald-600">Actif</span>
                   </div>
                </td>
                <td class="py-6 text-right">
                   <button class="p-2 text-gray-300 hover:text-[#112830] transition-colors"><i class="bx bx-edit-alt text-xl"></i></button>
                   <button @click="deleteIndicator(indicator.uuid)" class="p-2 text-gray-300 hover:text-rose-500 transition-colors ml-2"><i class="bx bx-trash text-xl"></i></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ===== CONFIGURATION MODAL (Mockup) ===== -->
    <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-xl bg-black/40">
       <div class="bg-white w-full max-w-2xl rounded-[3rem] p-12 shadow-2xl relative animate-in fade-in zoom-in duration-300">
          <button @click="showAddModal = false" class="absolute top-8 right-8 w-12 h-12 rounded-full hover:bg-gray-100 flex items-center justify-center transition-all bg-white border border-gray-100">
            <i class="bx bx-x text-3xl"></i>
          </button>

          <div class="flex items-center gap-4 mb-10">
            <div class="w-16 h-16 rounded-[1.5rem] bg-[#112830] text-white flex items-center justify-center text-3xl shadow-xl shadow-[#112830]/20">
              <i class="bx bx-target-lock"></i>
            </div>
            <div>
              <h2 class="text-2xl font-black">Nouveau Standard</h2>
              <p class="text-gray-400 font-medium">Définissez un nouvel indicateur de impact.</p>
            </div>
          </div>

          <div class="space-y-6">
             <div class="grid grid-cols-2 gap-6">
                <div class="space-y-1">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Nom de l'indicateur</label>
                  <input v-model="newIndicator.name" type="text" placeholder="Ex: Taux de Reboisement" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 font-bold" />
                </div>
                <div class="space-y-1">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Code Unique</label>
                  <input v-model="newIndicator.code" type="text" placeholder="REFOREST_RATE" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 font-mono text-xs uppercase" />
                </div>
             </div>
             
             <div class="grid grid-cols-2 gap-6">
                <div class="space-y-1">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Catégorie</label>
                  <select v-model="newIndicator.category" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 font-bold">
                    <option v-for="cat in categories" :key="cat.uuid" :value="cat.uuid">{{ cat.name }}</option>
                  </select>
                </div>
                <div class="space-y-1">
                  <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Unité de Mesure</label>
                  <input v-model="newIndicator.unit" type="text" placeholder="Ex: %, Ha, Kg..." class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 font-bold" />
                </div>
             </div>

             <div class="space-y-1">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-2">Cible Platforme (Seuil d'alerte) : {{ newIndicator.target_value }}</label>
                <div class="flex items-center gap-4 bg-amber-50 p-4 rounded-2xl border border-amber-100">
                  <input type="range" class="flex-1 accent-[#10b481]" v-model="newIndicator.target_value" />
                </div>
             </div>
          </div>

          <div class="flex items-center gap-6 pt-10 mt-10 border-t border-gray-50">
             <div class="flex items-center gap-3 text-[#112830]/40">
               <i class="bx bx-info-circle text-2xl"></i>
               <span class="text-[10px] font-bold leading-tight uppercase tracking-tighter">Ce standard sera déployé sur<br/>tous les espaces organisation.</span>
             </div>
             <button @click="saveIndicator" class="ml-auto px-12 py-5 bg-[#10b481] text-white rounded-[2rem] font-black shadow-2xl hover:bg-[#112830] transition-all duration-500">
               Enregistrer l'Indicateur
             </button>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const isLoading = ref(true);
const showAddModal = ref(false);
const searchQuery = ref('');

const indicators = ref<any[]>([]);
const categories = ref<any[]>([]);

// --- Form State ---
const newIndicator = ref({
  name: '',
  code: '',
  category: '', 
  unit: '',
  frequency: 'monthly',
  target_value: 75
});

const filteredIndicators = computed(() => {
  if (!searchQuery.value) return indicators.value;
  const q = searchQuery.value.toLowerCase();
  return indicators.value.filter(i => 
    i.name.toLowerCase().includes(q) || 
    i.code.toLowerCase().includes(q)
  );
});

const standards = computed(() => [
  { label: 'Indicateurs Globaux', value: indicators.value.length.toString(), unit: 'Items Actifs', icon: 'bx bx-target-lock', color: 'text-emerald-600', bg: 'bg-emerald-50' },
  { label: 'Taux de Complétion', value: '88.4', unit: '% Moyenne', icon: 'bx bx-line-chart', color: 'text-blue-600', bg: 'bg-blue-50' },
  { label: 'Seuils d\'Alertes', value: indicators.value.filter(i => i.target_value).length.toString(), unit: 'Paramétrés', icon: 'bx bx-bell', color: 'text-amber-600', bg: 'bg-amber-50' },
]);

async function fetchIndicators() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/suivi-evaluation/api/indicators/');
    indicators.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchIndicators:", err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchCategories() {
  try {
    const data: any = await apiFetch('/api/suivi-evaluation/api/indicator-categories/');
    categories.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchCategories:", err);
  }
}

async function saveIndicator() {
  try {
    await apiFetch('/api/suivi-evaluation/api/indicators/', {
      method: 'POST',
      body: newIndicator.value
    });
    showAddModal.value = false;
    fetchIndicators();
    // Reset form
    newIndicator.value = { name: '', code: '', category: '', unit: '', frequency: 'monthly', target_value: 75 };
  } catch (err) {
    console.error("Erreur saveIndicator:", err);
    alert("Erreur lors de l'enregistrement de l'indicateur.");
  }
}

async function deleteIndicator(uuid: string) {
  if (!confirm("Voulez-vous vraiment supprimer cet indicateur ?")) return;
  try {
    await apiFetch(`/api/suivi-evaluation/api/indicators/${uuid}/`, {
      method: 'DELETE'
    });
    fetchIndicators();
  } catch (err) {
    console.error("Erreur deleteIndicator:", err);
    alert("Erreur lors de la suppression.");
  }
}

onMounted(() => {
  fetchIndicators();
  fetchCategories();
});
</script>
