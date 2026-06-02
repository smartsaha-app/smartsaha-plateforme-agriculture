<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('admin.auditsPageTitle')">
      <template #subtitle>
        <i class="bx bx-shield-quarter"></i>
        {{ t('admin.auditsPageDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Admin</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('admin.auditsLink') }}</span>
      </template>
    </PageHeader>

    <!-- Filter tabs -->
    <div class="flex items-center gap-2 justify-between flex-wrap">
      <div class="flex gap-1.5 bg-gray-100 p-1.5 rounded-2xl">
        <button v-for="s in statusFilters" :key="s" @click="selectedStatus = s"
          :class="['px-5 py-2 rounded-xl text-xs font-bold transition-all', selectedStatus === s ? 'bg-[#112830] text-white shadow-sm' : 'text-gray-400 hover:text-gray-600']">
          {{ s }}
        </button>
      </div>
      <span class="text-xs font-bold text-gray-400">
        {{ filteredAudits.length }} dossier{{ filteredAudits.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== CONTENT GRID ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- LEFT: Audit queue -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
        <div class="px-6 py-4 border-b border-gray-50 flex items-center justify-between">
          <h3 class="text-sm font-black text-[#112830]">{{ t('admin.auditQueue') }}</h3>
          <span class="px-2.5 py-1 bg-emerald-50 text-[#10b481] rounded-lg text-[9px] font-black uppercase tracking-widest border border-emerald-100">
            {{ filteredAudits.length }} {{ t('admin.auditFolders') }}
          </span>
        </div>

        <div v-if="isLoading" class="p-10 flex justify-center">
          <div class="w-8 h-8 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        </div>

        <div v-else-if="filteredAudits.length === 0" class="p-16 text-center space-y-3">
          <i class="bx bx-check-shield text-4xl text-gray-200"></i>
          <p class="text-sm text-gray-400 font-medium">{{ t('admin.noAuditStatus') }}</p>
        </div>

        <div v-else class="flex-1 overflow-y-auto divide-y divide-gray-50 custom-scrollbar">
          <div v-for="audit in filteredAudits" :key="audit.id"
            @click="selectedAudit = audit"
            :class="[
              'p-5 cursor-pointer group transition-all',
              selectedAudit?.id === audit.id ? 'bg-emerald-50/50 border-l-4 border-l-[#10b481]' : 'hover:bg-gray-50/50'
            ]">
            <div class="flex items-start justify-between gap-3 mb-2">
              <span class="px-2.5 py-1 bg-blue-50 text-blue-600 border border-blue-100 rounded-lg text-[8px] font-black uppercase tracking-widest">
                {{ audit.type }}
              </span>
              <span class="text-[9px] font-bold text-gray-400 flex-shrink-0">{{ audit.date }}</span>
            </div>
            <h4 class="text-sm font-black text-[#112830] group-hover:text-[#10b481] transition-colors mb-1">
              {{ audit.org }}
            </h4>
            <p class="text-xs text-gray-400 mb-3 line-clamp-2 border-l-2 border-gray-200 pl-2">{{ audit.summary }}</p>
            <div class="flex items-center justify-between">
              <span class="text-[9px] text-gray-400 font-medium flex items-center gap-1">
                <i class="bx bx-user-circle"></i>
                {{ audit.auditor }}
              </span>
              <span class="text-xs font-black" :class="audit.score >= 90 ? 'text-emerald-600' : 'text-amber-600'">
                {{ audit.score }}%
              </span>
            </div>
          </div>
        </div>

        <div v-if="!isLoading && totalCount > 20" class="p-4 border-t border-gray-50">
          <PaginationBase :totalCount="totalCount" :perPage="20"
            v-model:currentPage="currentPage" @change-page="(p) => currentPage = p" />
        </div>
      </div>

      <!-- RIGHT: Detail panel -->
      <div v-if="selectedAudit" class="bg-[#112830] rounded-2xl shadow-xl flex flex-col overflow-hidden relative">
        <i class="bx bx-badge-check absolute bottom-[-10%] right-[-10%] text-[15rem] text-white/5 pointer-events-none"></i>

        <div class="p-7 space-y-6 flex-1 relative z-10">
          <!-- Header -->
          <div class="flex items-start justify-between gap-3">
            <div>
              <p class="text-[#10b481] text-[9px] font-black uppercase tracking-widest mb-1">{{ t('admin.auditDetail') }}</p>
              <h2 class="text-xl font-black text-white">{{ selectedAudit.org }}</h2>
              <p class="text-white/50 text-xs mt-0.5">{{ selectedAudit.type }} · {{ selectedAudit.date }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-white/10 border border-white/10 flex items-center justify-center flex-shrink-0">
              <i class="bx bx-file-find text-[#10b481] text-xl"></i>
            </div>
          </div>

          <!-- Score -->
          <div class="p-4 bg-white/5 border border-white/10 rounded-xl flex items-center justify-between">
            <span class="text-white/60 text-xs font-bold">{{ t('admin.complianceScore') }}</span>
            <span class="text-xl font-black" :class="selectedAudit.score >= 90 ? 'text-[#10b481]' : 'text-amber-400'">
              {{ selectedAudit.score }}%
            </span>
          </div>

          <!-- Documents -->
          <div v-if="selectedAudit.docs?.length" class="space-y-3 bg-white/5 p-5 rounded-xl border border-white/5">
            <h4 class="text-[9px] font-black uppercase tracking-widest text-white/40 mb-2">{{ t('admin.docsToCheck') }}</h4>
            <div v-for="doc in selectedAudit.docs" :key="doc.name"
              class="flex items-center justify-between group/doc py-1">
              <div class="flex items-center gap-3">
                <i :class="['bx text-lg', doc.checked ? 'bx-check-circle text-[#10b481]' : 'bx-circle text-white/20']"></i>
                <span class="text-sm font-medium text-white/80">{{ doc.name }}</span>
              </div>
              <a v-if="doc.url" :href="doc.url" target="_blank"
                class="text-[9px] font-black uppercase text-white/40 hover:text-[#10b481] transition-colors underline">
                Voir
              </a>
            </div>
          </div>

          <!-- Remarques -->
          <div class="space-y-2">
            <h4 class="text-[9px] font-black uppercase tracking-widest text-white/40">{{ t('admin.auditorNotes') }}</h4>
            <p class="text-sm text-white/60 leading-relaxed italic bg-black/20 p-4 rounded-xl border-l-4 border-[#10b481]">
              "{{ selectedAudit.notes || t('admin.noNotes') }}"
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="p-5 border-t border-white/10 flex gap-3 relative z-10">
          <button @click="openActionModal('PASS')"
            class="flex-1 py-3 bg-[#10b481] hover:bg-emerald-400 text-white rounded-xl font-bold text-sm transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/20">
            <i class="bx bx-check-shield text-base"></i>
            Approuver
          </button>
          <button @click="openActionModal('FAIL')"
            class="px-6 py-3 bg-white/10 hover:bg-rose-500 text-white rounded-xl font-bold text-sm border border-white/10 transition-all flex items-center justify-center gap-2">
            <i class="bx bx-x-circle text-base"></i>
            Rejeter
          </button>
        </div>
      </div>

      <!-- Placeholder -->
      <div v-else class="bg-white rounded-2xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center py-20 text-center space-y-4 shadow-sm">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center">
          <i class="bx bx-mouse-alt text-3xl text-gray-200"></i>
        </div>
        <div>
          <h3 class="text-sm font-black text-gray-400">{{ t('admin.noFolderSelected') }}</h3>
          <p class="text-xs text-gray-300 mt-1">{{ t('admin.noFolderSelectedDesc') }}</p>
        </div>
      </div>
    </div>

    <!-- ===== CONFIRM MODAL ===== -->
    <div v-if="pendingAction" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mx-auto', pendingAction === 'PASS' ? 'bg-emerald-50' : 'bg-rose-50']">
            <i :class="['text-2xl', pendingAction === 'PASS' ? 'bx bx-check-shield text-emerald-500' : 'bx bx-x-circle text-rose-500']"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">
              {{ pendingAction === 'PASS' ? t('admin.approveConfirm') : t('admin.rejectConfirm') }}
            </h2>
            <p class="text-sm text-gray-400 mt-1">
              <span class="font-bold text-[#112830]">{{ selectedAudit?.org }}</span>
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="pendingAction = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="executeAction" :disabled="isActing"
            :class="['flex-1 py-3 rounded-xl text-white font-bold text-sm transition-all disabled:opacity-50 flex items-center justify-center gap-2', pendingAction === 'PASS' ? 'bg-[#10b481] hover:bg-emerald-400' : 'bg-rose-500 hover:bg-rose-600']">
            <div v-if="isActing" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else :class="pendingAction === 'PASS' ? 'bx bx-check' : 'bx bx-x'"></i>
            Confirmer
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
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import PaginationBase from '~/components/ui/PaginationBase.vue';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();

const isLoading      = ref(true);
const isActing       = ref(false);
const selectedStatus = ref<string>('');  // initialized in onMounted
const statusFilters = computed(() => [t('admin.auditFilter_pending'), t('admin.auditFilter_pass'), t('admin.auditFilter_fail')]);
const audits         = ref<any[]>([]);
const selectedAudit  = ref<any>(null);
const pendingAction  = ref<string | null>(null);
const totalCount     = ref(0);
const currentPage    = ref(1);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

const statusMap = computed((): Record<string, string> => ({ [t('admin.auditFilter_pending')]: 'PENDING', [t('admin.auditFilter_pass')]: 'PASS', [t('admin.auditFilter_fail')]: 'FAIL' }));
const reverseStatusMap = computed((): Record<string, string> => ({ PENDING: t('admin.auditFilter_pending'), PASS: t('admin.auditFilter_pass'), FAIL: t('admin.auditFilter_fail') }));

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

async function fetchAudits() {
  isLoading.value = true;
  try {
    const statusVal = statusMap.value[selectedStatus.value] || 'PENDING';
    const data: any = await apiFetch(
      `/api/suivi-evaluation/api/certification-audits/?page=${currentPage.value}&result=${statusVal}`
    );
    const results = data.results || data || [];
    totalCount.value = data.count || results.length;
    audits.value = results.map((a: any) => ({
      id:      a.uuid,
      org:     a.report?.name || 'Inconnu',
      auditor: a.auditor,
      score:   a.score ?? 100,
      date:    new Date(a.date_audit).toLocaleDateString('fr-FR'),
      type:    a.cert_type?.name || 'Audit',
      status:  reverseStatusMap.value[a.result] || t('admin.auditFilter_pending'),
      summary: a.remarks || 'Aucune remarque.',
      notes:   a.remarks || '',
      docs:    (a.attachments || []).map((d: any) => ({ name: d.name, checked: !!d.verified, url: d.file_path || null })),
    }));
  } catch (err) {
    console.error('Erreur fetchAudits:', err);
  } finally {
    isLoading.value = false;
  }
}

const filteredAudits = computed(() => audits.value);

function openActionModal(action: string) { pendingAction.value = action; }

async function executeAction() {
  if (!pendingAction.value || !selectedAudit.value) return;
  isActing.value = true;
  try {
    await apiFetch(`/api/suivi-evaluation/api/certification-audits/${selectedAudit.value.id}/`, {
      method: 'PATCH',
      body: { result: pendingAction.value },
    });
    showToast(pendingAction.value === 'PASS' ? t('admin.auditApproved') : t('admin.auditRejected'));
    selectedAudit.value = null;
    pendingAction.value = null;
    fetchAudits();
  } catch {
    showToast(t('admin.auditUpdateError'), 'error');
  } finally {
    isActing.value = false;
  }
}

watch(selectedStatus, () => { currentPage.value = 1; fetchAudits(); });
watch(currentPage, () => fetchAudits());
onMounted(() => { selectedStatus.value = t('admin.auditFilter_pending'); fetchAudits(); });
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 4px; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>