<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Indicateurs S&E">
      <template #subtitle>
        <i class="bx bx-target-lock"></i>
        Définissez les standards de mesure, les indicateurs clés et les seuils d'alerte globaux.
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Admin</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Indicateurs</span>
      </template>
    </PageHeader>

    <div class="flex justify-end -mt-2">
      <button @click="openAddModal"
        class="flex items-center gap-2 px-4 py-2.5 bg-[#10b481] text-white rounded-xl text-sm font-bold hover:bg-emerald-400 transition-all shadow-sm">
        <i class="bx bx-plus-circle text-base"></i>
        Définir un Indicateur
      </button>
    </div>

    <!-- ===== STATS ===== -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div v-for="standard in standards" :key="standard.label"
        class="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg', standard.bg, standard.color]">
            <i :class="standard.icon"></i>
          </div>
          <span class="text-[9px] font-black text-gray-300 uppercase tracking-widest">Global</span>
        </div>
        <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ standard.label }}</p>
        <div class="flex items-baseline gap-1">
          <h3 class="text-2xl font-black text-[#112830]">{{ standard.value }}</h3>
          <span class="text-xs font-bold text-gray-400">{{ standard.unit }}</span>
        </div>
      </div>
    </div>

    <!-- ===== TABLE ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-50 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 class="text-sm font-black text-[#112830]">Référentiel des Indicateurs</h3>
          <p class="text-xs text-gray-400">Catalogue des points de données collectés sur le terrain.</p>
        </div>
        <div class="relative">
          <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
          <input v-model="searchQuery" type="text" placeholder="Rechercher..."
            class="pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 w-56 font-medium" />
        </div>
      </div>

      <div v-if="isLoading" class="py-16 flex justify-center">
        <div class="w-8 h-8 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
      </div>

      <div v-else-if="filteredIndicators.length === 0" class="py-16 text-center space-y-3">
        <i class="bx bx-target-lock text-4xl text-gray-200"></i>
        <p class="text-sm text-gray-400">Aucun indicateur trouvé.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50/70 border-b border-gray-100">
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Indicateur</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Catégorie</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden md:table-cell">Fréquence</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">Cible</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">État</th>
              <th class="px-6 py-4 text-right"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="indicator in filteredIndicators" :key="indicator.uuid"
              class="group hover:bg-gray-50/50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center text-gray-400 group-hover:bg-[#112830] group-hover:text-white transition-all flex-shrink-0">
                    <i class="bx bx-target-lock text-sm"></i>
                  </div>
                  <div>
                    <p class="text-sm font-bold text-[#112830]">{{ indicator.name }}</p>
                    <p class="text-[9px] font-mono text-gray-400 uppercase">{{ indicator.code }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="px-2.5 py-1 bg-blue-50 text-blue-500 border border-blue-100 rounded-lg text-[9px] font-black uppercase tracking-widest">
                  {{ indicator.category_name || 'N/A' }}
                </span>
              </td>
              <td class="px-6 py-4 hidden md:table-cell">
                <span class="flex items-center gap-1.5 text-xs font-bold text-gray-500">
                  <i class="bx bx-time-five text-gray-400"></i>
                  {{ indicator.frequency }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-baseline gap-1">
                  <span class="text-sm font-black text-[#10b481]">{{ indicator.target_value }}</span>
                  <span class="text-[9px] font-bold text-gray-400">{{ indicator.unit }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_6px_rgba(16,180,129,0.5)]"></span>
                  <span class="text-[9px] font-black uppercase tracking-widest text-emerald-600">Actif</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-1.5">
                  <button @click="openEditModal(indicator)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-400 hover:bg-[#112830] hover:text-white hover:border-[#112830] transition-all text-xs font-bold">
                    <i class="bx bx-edit text-sm"></i>
                    <span class="hidden lg:inline">Modifier</span>
                  </button>
                  <button @click="openDeleteModal(indicator)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-400 hover:bg-rose-50 hover:text-rose-500 hover:border-rose-100 transition-all text-xs font-bold">
                    <i class="bx bx-trash text-sm"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ===== ADD/EDIT MODAL ===== -->
    <div v-if="showFormModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-lg rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center gap-3">
          <div class="w-11 h-11 bg-[#112830] rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-target-lock text-white text-lg"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ isEditing ? 'Modifier' : 'Nouvel' }} Indicateur</h2>
            <p class="text-xs text-gray-400">{{ isEditing ? 'Mettez à jour les paramètres.' : 'Définissez un nouvel indicateur de suivi.' }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Nom *</label>
            <input v-model="form.name" type="text" placeholder="Taux de Reboisement"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 font-medium" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Code Unique</label>
            <input v-model="form.code" type="text" placeholder="REFOREST_RATE"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 font-mono uppercase" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Catégorie</label>
            <select v-model="form.category" class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 font-medium appearance-none cursor-pointer">
              <option value="">Sélectionner...</option>
              <option v-for="cat in categories" :key="cat.uuid" :value="cat.uuid">{{ cat.name }}</option>
            </select>
          </div>
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">Unité</label>
            <input v-model="form.unit" type="text" placeholder="%, Ha, Kg..."
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 font-medium" />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">
            Cible / Seuil d'alerte : <span class="text-[#10b481] font-black">{{ form.target_value }} {{ form.unit }}</span>
          </label>
          <input type="range" min="0" max="100" class="w-full accent-[#10b481]" v-model="form.target_value" />
        </div>

        <div class="flex gap-3 pt-2">
          <button @click="closeModal"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="saveIndicator" :disabled="!form.name || isSaving"
            class="flex-1 py-3 rounded-xl bg-[#10b481] text-white font-bold text-sm hover:bg-emerald-400 transition-all disabled:opacity-40 flex items-center justify-center gap-2">
            <div v-if="isSaving" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-save"></i>
            Enregistrer
          </button>
        </div>
      </div>
    </div>

    <!-- ===== DELETE MODAL ===== -->
    <div v-if="indicatorToDelete" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-trash text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">Supprimer cet indicateur ?</h2>
            <p class="text-sm text-gray-400 mt-1">
              "<span class="font-bold text-[#112830]">{{ indicatorToDelete.name }}</span>" sera définitivement supprimé.
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="indicatorToDelete = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="confirmDelete" :disabled="isDeleting"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="isDeleting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            Supprimer
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold"
        :class="toast.type === 'success' ? 'bg-[#112830] text-white' : 'bg-rose-500 text-white'">
        <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'" class="text-lg"
          :style="toast.type === 'success' ? 'color:#10b481' : ''"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();

const isLoading        = ref(true);
const isSaving         = ref(false);
const isDeleting       = ref(false);
const showFormModal    = ref(false);
const isEditing        = ref(false);
const searchQuery      = ref('');
const indicators       = ref<any[]>([]);
const categories       = ref<any[]>([]);
const indicatorToDelete = ref<any>(null);
const editingId        = ref<string | null>(null);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

const defaultForm = () => ({ name: '', code: '', category: '', unit: '', frequency: 'monthly', target_value: 75 });
const form = ref(defaultForm());

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

const filteredIndicators = computed(() => {
  if (!searchQuery.value) return indicators.value;
  const q = searchQuery.value.toLowerCase();
  return indicators.value.filter(i =>
    i.name?.toLowerCase().includes(q) || i.code?.toLowerCase().includes(q)
  );
});

const standards = computed(() => [
  { label: 'Indicateurs Actifs', value: indicators.value.length.toString(),                           unit: 'items',      icon: 'bx bx-target-lock', color: 'text-emerald-600', bg: 'bg-emerald-50' },
  { label: 'Taux de Complétion', value: '88.4',                                                       unit: '% moyenne',  icon: 'bx bx-line-chart',  color: 'text-blue-600',    bg: 'bg-blue-50'    },
  { label: 'Seuils Paramétrés',  value: indicators.value.filter(i => i.target_value).length.toString(), unit: 'actifs',   icon: 'bx bx-bell',        color: 'text-amber-600',   bg: 'bg-amber-50'   },
]);

async function fetchIndicators() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/suivi-evaluation/api/indicators/');
    indicators.value = data.results || data || [];
  } catch (err) {
    console.error('Erreur fetchIndicators:', err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchCategories() {
  try {
    const data: any = await apiFetch('/api/suivi-evaluation/api/indicator-categories/');
    categories.value = data.results || data || [];
  } catch { /* silent */ }
}

function openAddModal() {
  isEditing.value = false;
  editingId.value = null;
  form.value = defaultForm();
  showFormModal.value = true;
}

function openEditModal(indicator: any) {
  isEditing.value = true;
  editingId.value = indicator.uuid;
  form.value = {
    name:         indicator.name || '',
    code:         indicator.code || '',
    category:     indicator.category || '',
    unit:         indicator.unit || '',
    frequency:    indicator.frequency || 'monthly',
    target_value: indicator.target_value || 75,
  };
  showFormModal.value = true;
}

function closeModal() {
  showFormModal.value = false;
  isEditing.value = false;
  editingId.value = null;
  form.value = defaultForm();
}

async function saveIndicator() {
  if (!form.value.name) return;
  isSaving.value = true;
  try {
    if (isEditing.value && editingId.value) {
      await apiFetch(`/api/suivi-evaluation/api/indicators/${editingId.value}/`, { method: 'PATCH', body: form.value });
      showToast('Indicateur mis à jour avec succès');
    } else {
      await apiFetch('/api/suivi-evaluation/api/indicators/', { method: 'POST', body: form.value });
      showToast('Indicateur créé avec succès');
    }
    closeModal();
    fetchIndicators();
  } catch {
    showToast('Erreur lors de l\'enregistrement', 'error');
  } finally {
    isSaving.value = false;
  }
}

function openDeleteModal(indicator: any) { indicatorToDelete.value = indicator; }

async function confirmDelete() {
  if (!indicatorToDelete.value) return;
  isDeleting.value = true;
  try {
    await apiFetch(`/api/suivi-evaluation/api/indicators/${indicatorToDelete.value.uuid}/`, { method: 'DELETE' });
    showToast('Indicateur supprimé');
    indicatorToDelete.value = null;
    fetchIndicators();
  } catch {
    showToast('Erreur lors de la suppression', 'error');
  } finally {
    isDeleting.value = false;
  }
}

onMounted(() => {
  fetchIndicators();
  fetchCategories();
});
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>