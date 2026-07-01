<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- HEADER -->
    <PageHeader :title="t('kyc.title')">
      <template #subtitle>
        <i class="bx bx-shield-quarter"></i>
        {{ t('kyc.subtitle') }}
      </template>
      <template #breadcrumb>
        <NuxtLink :to="`/${role}/dashboard`" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('kyc.sidebarLink') }}</span>
      </template>
    </PageHeader>

    <!-- STATUT ACTUEL -->
    <div class="rounded-2xl border shadow-sm p-6 flex items-start gap-5"
      :class="statusCardClass">
      <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0" :class="statusIconBg">
        <i class="text-2xl" :class="statusIcon"></i>
      </div>
      <div class="flex-1">
        <p class="text-sm font-black" :class="statusTextColor">{{ statusLabel }}</p>
        <p class="text-xs mt-1 leading-relaxed" :class="statusDescColor">{{ statusDesc }}</p>
        <div v-if="rejectedDocs.length > 0" class="mt-3 space-y-1">
          <p class="text-[10px] font-black text-rose-500 uppercase tracking-widest">{{ t('kyc.rejectionReason') }} :</p>
          <p v-for="doc in rejectedDocs" :key="doc.uuid" class="text-xs text-rose-600 flex items-center gap-1.5">
            <i class="bx bx-error-circle text-sm"></i>
            {{ doc.doc_type_display }} — {{ doc.rejection_reason }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- ── FORMULAIRE D'UPLOAD ── -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 flex flex-col">
        <div class="mb-6">
          <h2 class="text-base font-black text-[#112830]">{{ t('kyc.uploadTitle') }}</h2>
          <p class="text-xs text-gray-400 mt-0.5">{{ t('kyc.uploadDesc') }}</p>
        </div>

        <form @submit.prevent="handleSubmit" class="flex flex-col gap-5 flex-1">

          <!-- Type de document -->
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
              {{ t('kyc.docType') }} <span class="text-[#10b481]">*</span>
            </label>
            <div class="relative">
              <i class="bx bx-id-card absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
              <select
                v-model="form.docType"
                required
                class="w-full pl-11 pr-10 py-3.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 transition-all font-medium text-[#112830] appearance-none"
                :class="{ 'border-[#10b481]/30 bg-emerald-50/20': form.docType }"
              >
                <option disabled value="">{{ t('kyc.selectDocType') }}</option>
                <option value="ID_CARD">{{ t('kyc.idCard') }}</option>
                <option value="PASSPORT">{{ t('kyc.passport') }}</option>
                <option value="COMPANY_REG">{{ t('kyc.companyReg') }}</option>
                <option value="FARMER_CERT">{{ t('kyc.farmerCert') }}</option>
              </select>
              <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- Zone upload fichier -->
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
              {{ t('kyc.fileLabel') }} <span class="text-[#10b481]">*</span>
            </label>

            <div
              @click="fileInput?.click()"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              :class="[
                'relative flex flex-col items-center justify-center gap-3 p-8 rounded-xl border-2 border-dashed cursor-pointer transition-all',
                isDragging ? 'border-[#10b481] bg-emerald-50/50' : selectedFile ? 'border-[#10b481]/40 bg-emerald-50/20' : 'border-gray-200 hover:border-[#10b481]/40 hover:bg-gray-50'
              ]"
            >
              <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png,.pdf" class="hidden" @change="handleFileChange" />

              <!-- Aperçu fichier sélectionné -->
              <template v-if="selectedFile">
                <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center">
                  <i class="bx text-2xl text-[#10b481]" :class="fileIcon"></i>
                </div>
                <div class="text-center">
                  <p class="text-sm font-bold text-[#112830]">{{ selectedFile.name }}</p>
                  <p class="text-xs text-gray-400">{{ formatFileSize(selectedFile.size) }}</p>
                </div>
                <button type="button" @click.stop="clearFile"
                  class="text-xs font-bold text-rose-400 hover:text-rose-600 flex items-center gap-1">
                  <i class="bx bx-x"></i> Changer
                </button>
              </template>

              <!-- État vide -->
              <template v-else>
                <div class="w-12 h-12 rounded-xl bg-gray-50 flex items-center justify-center">
                  <i class="bx bx-cloud-upload text-2xl text-gray-300"></i>
                </div>
                <p class="text-sm font-medium text-gray-400 text-center">{{ t('kyc.dropzone') }}</p>
                <p class="text-[10px] text-gray-300">JPG, PNG, PDF — max 5 Mo</p>
              </template>
            </div>

            <!-- Erreur fichier -->
            <p v-if="fileError" class="text-[10px] text-rose-500 flex items-center gap-1 font-bold">
              <i class="bx bx-error-circle"></i> {{ fileError }}
            </p>
          </div>

          <!-- Bouton submit -->
          <button
            type="submit"
            :disabled="isSubmitting || !form.docType || !selectedFile"
            class="w-full py-3.5 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all shadow-sm disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-auto"
          >
            <div v-if="isSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <template v-else>
              <i class="bx bx-upload text-base"></i>
              {{ t('kyc.submit') }}
            </template>
          </button>
        </form>
      </div>

      <!-- ── HISTORIQUE DES DOCUMENTS ── -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 flex flex-col">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-base font-black text-[#112830]">{{ t('kyc.historyTitle') }}</h2>
          <span class="text-xs font-bold text-gray-400 bg-gray-50 px-2.5 py-1 rounded-lg">
            {{ documents.length }} doc{{ documents.length !== 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="flex-1 flex items-center justify-center">
          <div class="w-8 h-8 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        </div>

        <!-- Empty -->
        <div v-else-if="documents.length === 0" class="flex-1 flex flex-col items-center justify-center gap-4 text-center py-8">
          <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center">
            <i class="bx bx-file text-3xl text-gray-200"></i>
          </div>
          <div>
            <p class="text-sm font-black text-[#112830]">{{ t('kyc.noDocuments') }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ t('kyc.noDocumentsDesc') }}</p>
          </div>
        </div>

        <!-- Liste des documents -->
        <div v-else class="space-y-3 flex-1 overflow-y-auto">
          <div v-for="doc in documents" :key="doc.uuid"
            class="flex items-start gap-3 p-4 rounded-xl border border-gray-100 hover:border-gray-200 transition-colors">

            <!-- Icône type -->
            <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
              :class="docStatusBg(doc.status)">
              <i class="bx bx-file-blank text-base" :class="docStatusColor(doc.status)"></i>
            </div>

            <!-- Détails -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <p class="text-sm font-bold text-[#112830] truncate">{{ doc.doc_type_display }}</p>
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide"
                  :class="statusBadgeClass(doc.status)">
                  <i class="bx text-[9px]" :class="statusBadgeIcon(doc.status)"></i>
                  {{ doc.status_display }}
                </span>
              </div>
              <p class="text-[10px] text-gray-400 mt-0.5">
                {{ t('kyc.date') }} {{ formatDate(doc.created_at) }}
              </p>
              <p v-if="doc.rejection_reason" class="text-[10px] text-rose-500 mt-1 font-medium">
                <i class="bx bx-error-circle"></i> {{ doc.rejection_reason }}
              </p>
            </div>

            <!-- Actions -->
            <div class="flex flex-col gap-1.5 flex-shrink-0">
              <a v-if="doc.file_url" :href="doc.file_url" target="_blank"
                class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-500 hover:bg-[#112830] hover:text-white transition-all text-[10px] font-bold">
                <i class="bx bx-show text-sm"></i>
              </a>
              <button v-if="doc.status === 'PENDING'"
                @click="confirmDelete(doc)"
                class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-400 hover:bg-rose-50 hover:text-rose-500 hover:border-rose-100 transition-all text-[10px] font-bold">
                <i class="bx bx-trash text-sm"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL SUPPRESSION -->
    <div v-if="docToDelete" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-trash text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('kyc.deleteConfirm') }}</h2>
            <p class="text-xs text-gray-400 mt-1">{{ t('kyc.deleteDesc') }}</p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="docToDelete = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="handleDelete" :disabled="isDeleting"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
            <div v-if="isDeleting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <template v-else><i class="bx bx-trash"></i> {{ t('dashboard.delete') }}</template>
          </button>
        </div>
      </div>
    </div>

    <!-- NOTIFICATION TOAST -->
    <transition name="pop-notification">
      <div v-if="notif.visible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[100] w-full max-w-sm px-4">
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useKyc } from '~/composables/useKyc'

const props = defineProps<{ role: 'farmer' | 'organization' | 'seller' }>()
const { t } = useI18n()
const authStore = useAuthStore()
const { documents, isLoading, isSubmitting, fetchMyDocuments, submitDocument, deleteDocument } = useKyc()

// ── État local ───────────────────────────────────────────────────────────────
const form       = ref({ docType: '' })
const selectedFile = ref<File | null>(null)
const fileInput  = ref<HTMLInputElement | null>(null)
const fileError  = ref('')
const isDragging = ref(false)
const docToDelete = ref<any>(null)
const isDeleting  = ref(false)
const kycStatus   = ref<string>('PENDING')
const notif = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' })

// ── Statut global ────────────────────────────────────────────────────────────
const rejectedDocs = computed(() => documents.value.filter(d => d.status === 'REJECTED'))
const hasApproved  = computed(() => documents.value.some(d => d.status === 'APPROVED'))
const hasPending   = computed(() => documents.value.some(d => d.status === 'PENDING'))

const computedStatus = computed(() => {
  if (kycStatus.value === 'APPROVED') return 'APPROVED'
  if (rejectedDocs.value.length > 0 && !hasPending.value) return 'REJECTED'
  return 'PENDING'
})

const statusCardClass = computed(() => ({
  'bg-emerald-50 border-emerald-100': computedStatus.value === 'APPROVED',
  'bg-rose-50 border-rose-100':      computedStatus.value === 'REJECTED',
  'bg-amber-50 border-amber-100':    computedStatus.value === 'PENDING',
}))
const statusIconBg = computed(() => ({
  'bg-emerald-100': computedStatus.value === 'APPROVED',
  'bg-rose-100':    computedStatus.value === 'REJECTED',
  'bg-amber-100':   computedStatus.value === 'PENDING',
}))
const statusIcon = computed(() => ({
  'bx bx-check-shield text-emerald-600': computedStatus.value === 'APPROVED',
  'bx bx-shield-x text-rose-500':        computedStatus.value === 'REJECTED',
  'bx bx-time-five text-amber-500':       computedStatus.value === 'PENDING',
}))
const statusLabel = computed(() => ({
  APPROVED: t('kyc.approved'),
  REJECTED: t('kyc.rejected'),
  PENDING:  t('kyc.pending'),
}[computedStatus.value]))
const statusDesc = computed(() => ({
  APPROVED: t('kyc.approvedDesc'),
  REJECTED: t('kyc.rejectedDesc'),
  PENDING:  t('kyc.pendingDesc'),
}[computedStatus.value]))
const statusTextColor = computed(() => ({
  'text-emerald-700': computedStatus.value === 'APPROVED',
  'text-rose-600':    computedStatus.value === 'REJECTED',
  'text-amber-700':   computedStatus.value === 'PENDING',
}))
const statusDescColor = computed(() => ({
  'text-emerald-600': computedStatus.value === 'APPROVED',
  'text-rose-500':    computedStatus.value === 'REJECTED',
  'text-amber-600':   computedStatus.value === 'PENDING',
}))

// ── Fichier ──────────────────────────────────────────────────────────────────
const MAX_SIZE = 5 * 1024 * 1024
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf']

const fileIcon = computed(() => {
  if (!selectedFile.value) return 'bx-file'
  if (selectedFile.value.type === 'application/pdf') return 'bx-file-pdf'
  return 'bx-image'
})

function validateFile(file: File): boolean {
  fileError.value = ''
  if (file.size > MAX_SIZE) { fileError.value = t('kyc.errorFileSize'); return false }
  if (!ALLOWED_TYPES.includes(file.type)) { fileError.value = t('kyc.errorFileType'); return false }
  return true
}

function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file && validateFile(file)) selectedFile.value = file
}

function handleDrop(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file && validateFile(file)) selectedFile.value = file
}

function clearFile() {
  selectedFile.value = null
  fileError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' o'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' Ko'
  return (bytes / (1024 * 1024)).toFixed(1) + ' Mo'
}

// ── Soumission ───────────────────────────────────────────────────────────────
async function handleSubmit() {
  if (!selectedFile.value || !form.value.docType) return
  try {
    await submitDocument(form.value.docType, selectedFile.value)
    form.value.docType = ''
    clearFile()
    await fetchMyDocuments()
    showNotif(t('kyc.successSubmit'), 'success')
  } catch {
    showNotif(t('kyc.errorSubmit'), 'error')
  }
}

// ── Suppression ──────────────────────────────────────────────────────────────
function confirmDelete(doc: any) { docToDelete.value = doc }

async function handleDelete() {
  if (!docToDelete.value) return
  isDeleting.value = true
  try {
    await deleteDocument(docToDelete.value.uuid)
    docToDelete.value = null
    showNotif(t('kyc.successDelete'), 'success')
  } catch {
    showNotif(t('kyc.errorDelete'), 'error')
  } finally {
    isDeleting.value = false
  }
}

// ── Helpers affichage ────────────────────────────────────────────────────────
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

function docStatusBg(status: string): string {
  if (status === 'APPROVED') return 'bg-emerald-50'
  if (status === 'REJECTED') return 'bg-rose-50'
  return 'bg-amber-50'
}

function docStatusColor(status: string): string {
  if (status === 'APPROVED') return 'text-emerald-500'
  if (status === 'REJECTED') return 'text-rose-400'
  return 'text-amber-500'
}

function showNotif(message: string, type: 'success' | 'error') {
  notif.value = { visible: true, message, type }
  setTimeout(() => (notif.value.visible = false), 4000)
}

// ── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(async () => {
  await fetchMyDocuments()
  // Récupère le kyc_status depuis l'API user
  try {
    const { apiFetch } = useApi()
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`)
    kycStatus.value = data.kyc_status || 'PENDING'
  } catch { /* silencieux */ }
})
</script>

<style scoped>
.pop-notification-enter-active, .pop-notification-leave-active { transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop-notification-enter-from, .pop-notification-leave-to { opacity: 0; transform: translate(-50%, -16px) scale(0.92); }
</style>
