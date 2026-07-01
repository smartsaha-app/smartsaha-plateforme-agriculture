<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- HEADER -->
    <PageHeader :title="t('kyc.adminTitle')">
      <template #subtitle>
        <i class="bx bx-shield-quarter"></i>
        {{ t('kyc.adminSubtitle') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Tableau de bord</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('kyc.sidebarLink') }}</span>
      </template>
    </PageHeader>

    <!-- KPIs -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="kpi in kpis" :key="kpi.label"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex items-center gap-4">
        <div :class="['w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0', kpi.bg]">
          <i :class="['text-xl', kpi.icon, kpi.color]"></i>
        </div>
        <div>
          <p class="text-2xl font-black text-[#112830]">{{ kpi.value }}</p>
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{{ kpi.label }}</p>
        </div>
      </div>
    </div>

    <!-- FILTRES -->
    <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
      <div class="flex items-center gap-2 flex-wrap">
        <button v-for="f in filters" :key="f.value"
          @click="activeFilter = f.value"
          :class="[
            'px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all border',
            activeFilter === f.value
              ? 'bg-[#112830] text-white border-[#112830]'
              : 'bg-white text-gray-500 border-gray-100 hover:border-gray-200'
          ]"
        >
          {{ f.label }}
          <span v-if="f.count > 0" class="ml-1.5 px-1.5 py-0.5 rounded-full text-[9px] font-black"
            :class="activeFilter === f.value ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-500'">
            {{ f.count }}
          </span>
        </button>
      </div>

      <!-- Recherche -->
      <div class="relative">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="search" type="text" placeholder="Rechercher un utilisateur..."
          class="pl-10 pr-4 py-2.5 bg-white border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830] shadow-sm w-64" />
      </div>
    </div>

    <!-- TABLE -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">

      <div v-if="isLoading" class="py-24 flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-3 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">Chargement...</p>
      </div>

      <div v-else-if="filteredDocs.length > 0" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50/70 border-b border-gray-100">
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('kyc.user') }}</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Type de document</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest hidden sm:table-cell">{{ t('kyc.date') }}</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="doc in paginatedDocs" :key="doc.uuid"
              class="hover:bg-gray-50/50 transition-colors group">

              <!-- Utilisateur -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-[#10b481] flex items-center justify-center flex-shrink-0">
                    <span class="text-white text-xs font-bold">{{ userInitials(doc) }}</span>
                  </div>
                  <div>
                    <p class="font-bold text-sm text-[#112830]">
                      {{ [doc.user_first_name, doc.user_last_name].filter(Boolean).join(' ') || '—' }}
                    </p>
                    <p class="text-[10px] text-gray-400">{{ doc.user_email || '' }}</p>
                  </div>
                </div>
              </td>

              <!-- Type doc -->
              <td class="px-6 py-4">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[10px] font-bold text-gray-600 uppercase tracking-wide">
                  <i class="bx bx-file-blank text-xs"></i>
                  {{ doc.doc_type_display }}
                </span>
              </td>

              <!-- Date -->
              <td class="px-6 py-4 hidden sm:table-cell">
                <span class="text-xs font-medium text-gray-400">{{ formatDate(doc.created_at) }}</span>
              </td>

              <!-- Statut -->
              <td class="px-6 py-4">
                <span :class="['inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wide', statusBadgeClass(doc.status)]">
                  <i class="bx text-xs" :class="statusBadgeIcon(doc.status)"></i>
                  {{ doc.status_display }}
                </span>
              </td>

              <!-- Actions -->
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <!-- Voir le document -->
                  <a v-if="doc.file_url" :href="doc.file_url" target="_blank"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-500 hover:bg-[#112830] hover:text-white hover:border-[#112830] transition-all text-xs font-bold"
                    :title="t('kyc.viewDocument')">
                    <i class="bx bx-show text-sm"></i>
                  </a>
                  <!-- Approuver (si PENDING) -->
                  <button v-if="doc.status === 'PENDING'"
                    @click="openReview(doc, 'APPROVED')"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-600 hover:bg-emerald-500 hover:text-white hover:border-emerald-500 transition-all text-xs font-bold"
                    :title="t('kyc.approve')">
                    <i class="bx bx-check text-sm"></i>
                    {{ t('kyc.approve') }}
                  </button>
                  <!-- Rejeter (si PENDING) -->
                  <button v-if="doc.status === 'PENDING'"
                    @click="openReview(doc, 'REJECTED')"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-rose-50 border border-rose-100 text-rose-500 hover:bg-rose-500 hover:text-white hover:border-rose-500 transition-all text-xs font-bold"
                    :title="t('kyc.reject')">
                    <i class="bx bx-x text-sm"></i>
                    {{ t('kyc.reject') }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-50 flex items-center justify-between">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
            Page {{ currentPage }} / {{ totalPages }}
          </p>
          <div class="flex gap-1.5">
            <button @click="currentPage--" :disabled="currentPage === 1"
              class="w-9 h-9 rounded-lg bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-[#112830] hover:text-white disabled:opacity-30 transition-all">
              <i class="bx bx-chevron-left text-lg"></i>
            </button>
            <button v-for="p in totalPages" :key="p" @click="currentPage = p"
              :class="['w-9 h-9 rounded-lg text-xs font-black transition-all', currentPage === p ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100']">
              {{ p }}
            </button>
            <button @click="currentPage++" :disabled="currentPage === totalPages"
              class="w-9 h-9 rounded-lg bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-[#112830] hover:text-white disabled:opacity-30 transition-all">
              <i class="bx bx-chevron-right text-lg"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="py-24 flex flex-col items-center gap-5 text-center">
        <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center">
          <i class="bx bx-shield-quarter text-4xl text-gray-200"></i>
        </div>
        <div>
          <h3 class="text-base font-black text-[#112830]">{{ t('kyc.noDocsToReview') }}</h3>
          <p class="text-sm text-gray-400 mt-1">Tous les documents ont été traités.</p>
        </div>
      </div>
    </div>

    <!-- ── MODALE DE REVIEW ── -->
    <div v-if="reviewModal.open" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/30">
      <div class="bg-white w-full max-w-md rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">

        <!-- Header modale -->
        <div class="px-6 py-5 border-b border-gray-100 flex items-center gap-3">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0', reviewModal.action === 'APPROVED' ? 'bg-emerald-50' : 'bg-rose-50']">
            <i class="text-xl" :class="reviewModal.action === 'APPROVED' ? 'bx bx-check text-emerald-500' : 'bx bx-x text-rose-500'"></i>
          </div>
          <div>
            <h3 class="text-sm font-black text-[#112830]">
              {{ reviewModal.action === 'APPROVED' ? t('kyc.confirmApprove') : t('kyc.confirmReject') }}
            </h3>
            <p class="text-xs text-gray-400">
              {{ reviewModal.doc?.doc_type_display }} —
              {{ [reviewModal.doc?.user_first_name, reviewModal.doc?.user_last_name].filter(Boolean).join(' ') || reviewModal.doc?.user_email }}
            </p>
          </div>
        </div>

        <!-- Aperçu document -->
        <div v-if="reviewModal.doc?.file_url" class="px-6 pt-4">
          <a :href="reviewModal.doc.file_url" target="_blank"
            class="flex items-center gap-2 px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm font-bold text-[#10b481] hover:bg-emerald-50 transition-colors">
            <i class="bx bx-show text-base"></i>
            {{ t('kyc.viewDocument') }}
            <i class="bx bx-link-external text-xs ml-auto text-gray-300"></i>
          </a>
        </div>

        <!-- Motif de rejet -->
        <div class="px-6 py-4">
          <div v-if="reviewModal.action === 'REJECTED'" class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
              {{ t('kyc.rejectionReasonLabel') }}
            </label>
            <textarea
              v-model="reviewModal.reason"
              :placeholder="t('kyc.rejectionReasonPlaceholder')"
              rows="3"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-rose-200 focus:border-rose-300 transition-all font-medium text-[#112830] resize-none"
            ></textarea>
            <p v-if="reviewModal.reasonError" class="text-[10px] text-rose-500 font-bold flex items-center gap-1">
              <i class="bx bx-error-circle"></i> {{ reviewModal.reasonError }}
            </p>
          </div>
          <div v-else class="p-4 bg-emerald-50 rounded-xl text-sm text-emerald-700 font-medium">
            <i class="bx bx-info-circle mr-1"></i>
            Le statut KYC de l'utilisateur sera mis à jour en "Approuvé".
          </div>
        </div>

        <!-- Actions modale -->
        <div class="px-6 pb-6 flex gap-3">
          <button @click="reviewModal.open = false"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            Annuler
          </button>
          <button @click="handleReview" :disabled="isReviewing"
            :class="[
              'flex-[2] py-3 rounded-xl font-bold text-sm text-white transition-all flex items-center justify-center gap-2',
              reviewModal.action === 'APPROVED' ? 'bg-emerald-500 hover:bg-emerald-600' : 'bg-rose-500 hover:bg-rose-600',
              isReviewing ? 'opacity-50 cursor-not-allowed' : ''
            ]">
            <div v-if="isReviewing" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <template v-else>
              <i :class="reviewModal.action === 'APPROVED' ? 'bx bx-check' : 'bx bx-x'"></i>
              {{ reviewModal.action === 'APPROVED' ? t('kyc.approve') : t('kyc.reject') }}
            </template>
          </button>
        </div>
      </div>
    </div>

    <!-- TOAST -->
    <transition name="pop-notification">
      <div v-if="notif.visible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-2xl shadow-xl p-5 flex items-center gap-4 border',
          notif.type === 'success' ? 'border-l-4 border-l-[#10b481] border-gray-100' : 'border-l-4 border-l-rose-500 border-gray-100']">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0',
            notif.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notif.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <p class="text-sm font-bold text-[#112830]">{{ notif.message }}</p>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useKyc } from '~/composables/useKyc'

const { t } = useI18n()
const { documents, totalCount, adminStats, isLoading, fetchAllDocuments, fetchAdminStats, reviewDocument } = useKyc()

const search       = ref('')
const activeFilter = ref('')
const currentPage  = ref(1)
const itemsPerPage = 10
const isReviewing  = ref(false)
const notif = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' })

const reviewModal = reactive({
  open:        false,
  doc:         null as any,
  action:      'APPROVED' as 'APPROVED' | 'REJECTED',
  reason:      '',
  reasonError: '',
})

// ── KPIs : totaux globaux depuis l'endpoint stats (pas dépendants de la page courante)
const kpis = computed(() => [
  { label: 'Total',                   value: adminStats.value.total,    icon: 'bx bx-file-blank', bg: 'bg-blue-50',    color: 'text-blue-500' },
  { label: t('kyc.filterPending'),  value: adminStats.value.pending,  icon: 'bx bx-time-five',    bg: 'bg-amber-50',   color: 'text-amber-500' },
  { label: t('kyc.filterApproved'), value: adminStats.value.approved, icon: 'bx bx-check-circle', bg: 'bg-emerald-50', color: 'text-emerald-500' },
  { label: t('kyc.filterRejected'), value: adminStats.value.rejected, icon: 'bx bx-x-circle',     bg: 'bg-rose-50',    color: 'text-rose-500' },
])

// ── Filtres ──────────────────────────────────────────────────────────────────
const filters = computed(() => [
  { value: '',         label: t('kyc.allDocs'),        count: 0 },
  { value: 'PENDING',  label: t('kyc.filterPending'),  count: 0 },
  { value: 'APPROVED', label: t('kyc.filterApproved'), count: 0 },
  { value: 'REJECTED', label: t('kyc.filterRejected'), count: 0 },
])

// ── Documents : viennent directement du serveur (déjà filtrés et paginés)
const filteredDocs  = computed(() => documents.value)
const paginatedDocs = computed(() => documents.value)
const totalPages    = computed(() => Math.max(1, Math.ceil(totalCount.value / itemsPerPage)))

// Recharge depuis le serveur à chaque changement de filtre/recherche/page
let debounceTimer: ReturnType<typeof setTimeout>
function reload() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => fetchAllDocuments(activeFilter.value || undefined, search.value || undefined, currentPage.value), 300)
}

watch([activeFilter, search], () => {
  currentPage.value = 1
  reload()
})
watch(currentPage, () => reload())

// ── Helpers ──────────────────────────────────────────────────────────────────
function userInitials(doc: any): string {
  const first = doc.user_first_name?.charAt(0) ?? ''
  const last  = doc.user_last_name?.charAt(0) ?? ''
  if (first || last) return (first + last).toUpperCase()
  return (doc.user_email ?? '?').slice(0, 2).toUpperCase()
}

function formatDate(d: string): string {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

function statusBadgeClass(status: string): string {
  if (status === 'APPROVED') return 'bg-emerald-50 border border-emerald-100 text-emerald-600'
  if (status === 'REJECTED') return 'bg-rose-50 border border-rose-100 text-rose-500'
  return 'bg-amber-50 border border-amber-100 text-amber-600'
}

function statusBadgeIcon(status: string): string {
  if (status === 'APPROVED') return 'bx-check-circle'
  if (status === 'REJECTED') return 'bx-x-circle'
  return 'bx-time-five'
}

// ── Review ───────────────────────────────────────────────────────────────────
function openReview(doc: any, action: 'APPROVED' | 'REJECTED') {
  reviewModal.doc    = doc
  reviewModal.action = action
  reviewModal.reason = ''
  reviewModal.reasonError = ''
  reviewModal.open   = true
}

async function handleReview() {
  if (reviewModal.action === 'REJECTED' && !reviewModal.reason.trim()) {
    reviewModal.reasonError = 'Le motif de rejet est obligatoire.'
    return
  }
  isReviewing.value = true
  try {
    await reviewDocument(reviewModal.doc.uuid, reviewModal.action, reviewModal.reason || undefined)
    reviewModal.open = false
    showNotif(t('kyc.actionSuccess'), 'success')
    // Recharger les compteurs globaux après chaque décision
    await fetchAdminStats()
    reload()
  } catch {
    showNotif(t('kyc.actionError'), 'error')
  } finally {
    isReviewing.value = false
  }
}

function showNotif(message: string, type: 'success' | 'error') {
  notif.value = { visible: true, message, type }
  setTimeout(() => (notif.value.visible = false), 4000)
}

onMounted(() => {
  fetchAdminStats()
  fetchAllDocuments(undefined, undefined, 1)
})
</script>

<style scoped>
.pop-notification-enter-active, .pop-notification-leave-active { transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop-notification-enter-from, .pop-notification-leave-to { opacity: 0; transform: translate(-50%, -16px) scale(0.92); }
</style>
