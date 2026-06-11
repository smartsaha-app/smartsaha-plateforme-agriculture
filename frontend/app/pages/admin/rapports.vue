<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('admin.rapportsPageTitle')">
      <template #subtitle>
        <i class="bx bx-file-find"></i>
        {{ t('admin.rapportsPageDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Admin</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('admin.reportsLink') }}</span>
      </template>
    </PageHeader>

    <!-- Onglets -->
    <div class="flex gap-1 bg-gray-100 p-1.5 rounded-2xl w-fit">
      <button @click="activeTab = 'reports'"
        :class="['px-5 py-2 rounded-xl text-xs font-bold transition-all', activeTab === 'reports' ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600']">
        Mes Rapports
      </button>
      <button @click="activeTab = 'templates'"
        :class="['px-5 py-2 rounded-xl text-xs font-bold transition-all', activeTab === 'templates' ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600']">
        Modèles
      </button>
    </div>

    <!-- ===== TAB: MES RAPPORTS ===== -->
    <div v-if="activeTab === 'reports'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Panneau de configuration -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-emerald-50 text-[#10b481] rounded-xl flex items-center justify-center">
            <i class="bx bx-cog text-lg"></i>
          </div>
          <h3 class="text-sm font-black text-[#112830]">{{ t('admin.generateReportLabel') }}</h3>
        </div>

        <div class="space-y-4">
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.reportTypeLabel') }}</label>
            <div class="relative">
              <select v-model="selectedType" class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm font-bold outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer">
                <option value="IMPACT">Impact & Social</option>
                <option value="PROGRESS">Rendement & Production</option>
                <option value="FINANCIAL">Bilan Financier</option>
                <option value="AUDIT">Conformité Audit</option>
              </select>
              <i class="bx bx-chevron-down absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.scopeLabel') }}</label>
            <div class="relative">
              <select v-model="selectedScope" class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm font-bold outline-none focus:ring-2 focus:ring-[#10b481]/20 appearance-none cursor-pointer">
                <option value="">{{ t('admin.allOrganisations') }}</option>
                <option v-for="org in organisations" :key="org.id" :value="org.id">{{ org.name }}</option>
              </select>
              <i class="bx bx-chevron-down absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.dateStartLabel') }}</label>
              <input v-model="dateStart" type="date"
                class="w-full px-3 py-3 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold outline-none focus:ring-2 focus:ring-[#10b481]/20" />
            </div>
            <div class="space-y-1.5">
              <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.dateEndLabel') }}</label>
              <input v-model="dateEnd" type="date"
                class="w-full px-3 py-3 bg-gray-50 border border-gray-100 rounded-xl text-xs font-bold outline-none focus:ring-2 focus:ring-[#10b481]/20" />
            </div>
          </div>
        </div>

        <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-100 flex items-center gap-2">
          <i class="bx bx-check-circle text-[#10b481] flex-shrink-0"></i>
          <span class="text-xs font-bold text-emerald-700 leading-tight">{{ t('admin.pdfExcelNote') }}</span>
        </div>

        <button @click="generateReport" :disabled="isGenerating || !dateStart || !dateEnd"
          class="w-full py-3 bg-[#112830] text-white rounded-xl font-bold text-sm hover:bg-[#10b481] transition-all shadow-sm disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2">
          <div v-if="isGenerating" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          <i v-else class="bx bx-rocket text-base"></i>
          {{ isGenerating ? t('admin.generatingLabel') : t('admin.generateBtn') }}
        </button>
      </div>

      <!-- Contenu droite -->
      <div class="lg:col-span-2 space-y-5">

        <!-- Types de rapport -->
        <div class="grid grid-cols-2 gap-4">
          <div v-for="rt in reportTypes" :key="rrt.id"
            @click="selectedType = rt.id"
            :class="['group bg-white p-5 rounded-2xl border shadow-sm hover:shadow-md transition-all cursor-pointer relative overflow-hidden', selectedType === rt.id ? 'border-[#10b481]/40 bg-emerald-50/20' : 'border-gray-100']">
            <div class="absolute top-0 right-0 p-5 opacity-5 group-hover:opacity-10 transition-opacity">
              <i :class="[rt.icon, 'text-5xl', rt.color]"></i>
            </div>
            <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-lg mb-3', rt.bg, rt.color]">
              <i :class="rt.icon"></i>
            </div>
            <h4 class="text-sm font-black text-[#112830] mb-0.5">{{ rt.name }}</h4>
            <p class="text-xs text-gray-400 leading-relaxed">{{ rt.desc }}</p>
            <i v-if="selectedType === rt.id" class="bx bx-check-circle absolute top-3 right-3 text-[#10b481] text-lg"></i>
          </div>
        </div>

        <!-- Archives -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-50">
            <h3 class="text-sm font-black text-[#112830]">{{ t('admin.recentArchives') }}</h3>
          </div>

          <div v-if="isLoading" class="py-10 flex justify-center">
            <div class="w-7 h-7 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
          </div>

          <div v-else-if="reportsHistory.length === 0" class="py-12 text-center">
            <i class="bx bx-file text-4xl text-gray-200 mb-2"></i>
            <p class="text-sm text-gray-400">{{ t('admin.noReports') }}</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="bg-gray-50/70 border-b border-gray-100">
                  <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('admin.colDocument') }}</th>
                  <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden sm:table-cell">{{ t('admin.colPeriod') }}</th>
                  <th class="px-5 py-3 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('dashboard.status') }}</th>
                  <th class="px-5 py-3"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="h in reportsHistory" :key="h.id" class="hover:bg-gray-50/50 transition-colors group">
                  <td class="px-5 py-4">
                    <div class="flex items-center gap-2">
                      <i class="bx bxs-file-pdf text-rose-500 text-lg flex-shrink-0"></i>
                      <span class="text-sm font-bold text-[#112830] group-hover:text-[#10b481] transition-colors truncate max-w-[180px]">
                        {{ h.name }}
                      </span>
                    </div>
                  </td>
                  <td class="px-5 py-4 hidden sm:table-cell">
                    <span class="text-xs text-gray-500 font-medium">{{ h.period }}</span>
                  </td>
                  <td class="px-5 py-4">
                    <span :class="['px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest', h.status === 'OK' ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600']">
                      {{ h.status === 'OK' ? t('admin.reportAvailable') : t('admin.reportPending') }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-right">
                    <a v-if="h.file" :href="h.file" target="_blank"
                      class="w-8 h-8 rounded-lg bg-gray-50 hover:bg-[#112830] hover:text-white transition-all flex items-center justify-center ml-auto text-gray-400">
                      <i class="bx bx-download text-sm"></i>
                    </a>
                    <div v-else class="w-8 h-8 rounded-lg bg-gray-50 text-gray-200 flex items-center justify-center ml-auto">
                      <i class="bx bx-time text-sm"></i>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="!isLoading && totalCount > 20" class="px-6 py-4 border-t border-gray-50">
            <PaginationBase :totalCount="totalCount" :perPage="20"
              v-model:currentPage="currentPage" @change-page="(p) => currentPage = p" />
          </div>
        </div>
      </div>
    </div>

    <!-- ===== TAB: MODÈLES ===== -->
    <div v-if="activeTab === 'templates'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="rt in reportTypes" :key="rrt.id"
        class="group bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:border-[#10b481]/20 transition-all cursor-pointer relative overflow-hidden">
        <div class="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
          <i :class="[rt.icon, 'text-5xl', rt.color]"></i>
        </div>
        <div :class="['w-12 h-12 rounded-xl flex items-center justify-center text-xl mb-4', rt.bg, rt.color]">
          <i :class="rt.icon"></i>
        </div>
        <h4 class="text-sm font-black text-[#112830] mb-1">{{ rt.name }}</h4>
        <p class="text-xs text-gray-400 leading-relaxed mb-4">{{ rt.desc }}</p>
        <button @click="selectedType = t.id; activeTab = 'reports'"
          class="flex items-center gap-1.5 text-[9px] font-black text-[#10b481] uppercase tracking-widest hover:gap-2.5 transition-all">
          Utiliser ce modèle <i class="bx bx-right-arrow-alt text-sm"></i>
        </button>
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
import { ref, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';
import PaginationBase from '~/components/ui/PaginationBase.vue';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const authStore    = useAuthStore();

const activeTab       = ref('reports');
const selectedType    = ref('PROGRESS');
const selectedScope   = ref('');
const dateStart       = ref('');
const dateEnd         = ref('');
const isGenerating    = ref(false);
const isLoading       = ref(true);
const totalCount      = ref(0);
const currentPage     = ref(1);
const reportsHistory  = ref<any[]>([]);
const organisations   = ref<any[]>([]);
const organisationId  = ref<number | null>(null);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

const reportTypes = computed(() => [
  { id: 'PROGRESS', name: t('admin.rType_progress_name'), desc: t('admin.rType_progress_desc'), icon: 'bx bx-line-chart',      bg: 'bg-emerald-50', color: 'text-emerald-600' },
  { id: 'IMPACT',   name: t('admin.rType_impact_name'), desc: t('admin.rType_impact_desc'), icon: 'bx bx-world',        bg: 'bg-blue-50',    color: 'text-blue-600'    },
  { id: 'FINANCIAL',name: t('admin.rType_financial_name'), desc: t('admin.rType_financial_desc'), icon: 'bx bx-money',          bg: 'bg-amber-50',   color: 'text-amber-600'   },
  { id: 'AUDIT',    name: t('admin.rType_audit_name'), desc: t('admin.rType_audit_desc'), icon: 'bx bx-shield-quarter',   bg: 'bg-rose-50',    color: 'text-rose-600'    },
]);

async function fetchOrganisations() {
  try {
    const data: any = await apiFetch('/api/organisations/');
    organisations.value = data.results || data || [];
  } catch { /* silent */ }
}

async function fetchUserData() {
  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    organisationId.value = data.organisation_id ?? null;
  } catch { /* silent */ }
}

async function fetchHistory() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch(`/api/suivi-evaluation/api/reporting/?page=${currentPage.value}`);
    const results = data.results || data || [];
    totalCount.value = data.count || results.length;
    reportsHistory.value = results.map((r: any) => ({
      id:     r.uuid,
      name:   r.name,
      period: `${r.period_start} – ${r.period_end}`,
      status: r.status === 'APPROVED' ? 'OK' : 'PENDING',
      file:   r.attachments?.[0]?.file_path || null,
    }));
  } catch (err) {
    console.error('Erreur fetchHistory:', err);
  } finally {
    isLoading.value = false;
  }
}

async function generateReport() {
  if (!dateStart.value || !dateEnd.value) {
    showToast(t('admin.selectPeriod'), 'error');
    return;
  }
  isGenerating.value = true;
  try {
    await apiFetch('/api/suivi-evaluation/api/reporting/', {
      method: 'POST',
      body: {
        name:           `Rapport ${selectedType.value} ${new Date().toLocaleDateString('fr-FR')}`,
        type:           selectedType.value,
        period_start:   dateStart.value,
        period_end:     dateEnd.value,
        organisation_id: selectedScope.value || organisationId.value,
      },
    });
    showToast(t('admin.reportCreated'));
    fetchHistory();
  } catch {
    showToast(t('admin.reportCreateError'), 'error');
  } finally {
    isGenerating.value = false;
  }
}

watch(currentPage, () => fetchHistory());

onMounted(async () => {
  await Promise.all([fetchHistory(), fetchUserData(), fetchOrganisations()]);
});
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>