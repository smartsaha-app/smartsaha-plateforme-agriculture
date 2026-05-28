<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Rendements & récoltes">
      <template #subtitle>
        <i class="bx bx-trending-up"></i>
        <template v-if="parcelCropId && parcelCropName">{{ parcelCropName }} · </template>
        {{ filteredYields.length }} enregistrement{{ filteredYields.length !== 1 ? 's' : '' }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <template v-if="parcelCropId">
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/crops/show/${parcelCropId}`" class="hover:text-[#10b481] transition-colors">
            {{ parcelCropName || 'Plantation' }}
          </NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Rendements</span>
      </template>
    </PageHeader>
    <div class="flex justify-end -mt-2 mb-6">
      <NuxtLink
        :to="parcelCropId ? `/farmer/parcels/crops/show/yields/create?parcel_crop=${parcelCropId}` : '/farmer/parcels/crops/show/yields/create'"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors shadow-sm whitespace-nowrap"
      >
        <i class="bx bx-plus text-base"></i> Enregistrer une récolte
      </NuxtLink>
    </div>

    <!-- ===== STATS ===== -->
    <div v-if="!isLoading && yields.length" class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <span :class="['w-9 h-9 rounded-xl flex items-center justify-center text-base', stat.iconBg]">
            <i :class="['bx', stat.icon]"></i>
          </span>
          <span class="text-[22px] font-bold text-gray-900 leading-none">{{ stat.value }}</span>
        </div>
        <p class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">{{ stat.label }}</p>
        <p v-if="stat.unit" class="text-[10px] text-gray-300 mt-0.5">{{ stat.unit }}</p>
      </div>
    </div>

    <!-- ===== SEARCH ===== -->
    <div v-if="!isLoading && yields.length" class="bg-white rounded-2xl border border-gray-100 shadow-sm mb-5 px-4 py-3">
      <div class="flex flex-col sm:flex-row sm:items-center gap-3">
        <div class="relative max-w-xs w-full sm:w-auto">
          <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher par plantation…"
            class="w-full pl-9 pr-4 py-2 bg-gray-50 border border-gray-100 rounded-xl text-[13px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 transition-all"
          >
        </div>
        <div class="flex items-center gap-2 flex-wrap text-[12px] text-gray-400 sm:ml-auto">
          <span>Trier par :</span>
          <button
            @click="sortBy = 'date'"
            :class="['px-3 py-1.5 rounded-xl font-semibold transition-all', sortBy === 'date' ? 'bg-[#013b28] text-white' : 'bg-gray-50 text-gray-500 hover:bg-gray-100']"
          >Date</button>
          <button
            @click="sortBy = 'yield'"
            :class="['px-3 py-1.5 rounded-xl font-semibold transition-all', sortBy === 'yield' ? 'bg-[#013b28] text-white' : 'bg-gray-50 text-gray-500 hover:bg-gray-100']"
          >Rendement</button>
        </div>
      </div>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <i class="bx bx-loader-alt animate-spin text-3xl"></i>
      <p class="text-[13px]">Chargement des rendements…</p>
    </div>

    <!-- ===== TABLE ===== -->
    <template v-else-if="paginatedYields.length">
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-gray-100 bg-gray-50/50">
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400">Date</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400">Plantation</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-right">Quantité (kg)</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-right">Surface (m²)</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-right">kg/m²</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr
                v-for="y in paginatedYields"
                :key="y.id"
                class="group hover:bg-gray-50/60 transition-colors"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center gap-1.5">
                    <i class="bx bx-calendar text-gray-300 text-sm"></i>
                    <span class="text-[13px] text-gray-600">{{ formatDate(y.date) }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div>
                    <p class="text-[14px] font-semibold text-gray-900">{{ y.parcelName || '—' }}</p>
                    <p v-if="y.cropName" class="text-[11px] text-[#10b481] font-medium mt-0.5">{{ y.cropName }}</p>
                  </div>
                </td>
                <td class="px-6 py-4 text-right">
                  <span class="text-[15px] font-bold text-gray-900">{{ formatNumber(y.yield_amount) }}</span>
                  <span class="text-[11px] text-gray-400 ml-1">kg</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span class="text-[14px] font-semibold text-gray-600">{{ formatNumber(y.area) }}</span>
                  <span class="text-[11px] text-gray-400 ml-1">m²</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span :class="['text-[13px] font-semibold', getYieldRatioColor(y)]">
                    {{ yieldRatio(y) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="goEdit(y.id)"
                      class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-amber-500 hover:border-amber-200 transition-all shadow-sm"
                      title="Modifier"
                    >
                      <i class="bx bx-edit-alt text-base"></i>
                    </button>
                    <button
                      @click="openDeleteModal(y)"
                      class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-rose-500 hover:border-rose-200 transition-all shadow-sm"
                      title="Supprimer"
                    >
                      <i class="bx bx-trash text-base"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="px-6 py-3.5 border-t border-gray-100 flex items-center justify-between bg-gray-50/30">
          <p class="text-[12px] text-gray-400">
            {{ (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, filteredYields.length) }} sur {{ filteredYields.length }}
          </p>
          <div class="flex items-center gap-1.5">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-left text-lg"></i>
            </button>
            <button
              v-for="p in totalPages"
              :key="p"
              @click="currentPage = p"
              :class="[
                'w-8 h-8 rounded-lg text-[12px] font-semibold transition-all',
                currentPage === p ? 'bg-[#013b28] text-white' : 'bg-white text-gray-500 hover:bg-gray-100 border border-gray-100'
              ]"
            >{{ p }}</button>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-right text-lg"></i>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- ===== EMPTY ===== -->
    <div v-else class="flex flex-col items-center justify-center py-24 text-center">
      <div class="w-16 h-16 bg-emerald-50 rounded-full flex items-center justify-center mb-5">
        <i class="bx bx-bar-chart-alt-2 text-3xl text-emerald-500"></i>
      </div>
      <h3 class="text-[16px] font-semibold text-gray-900 mb-2">Aucun rendement enregistré</h3>
      <p class="text-[13px] text-gray-400 mb-6 max-w-xs leading-relaxed">
        Enregistrez vos premières récoltes pour suivre l'évolution de vos rendements agricoles.
      </p>
      <NuxtLink
        :to="parcelCropId ? `/farmer/parcels/crops/show/yields/create?parcel_crop=${parcelCropId}` : '/farmer/parcels/crops/show/yields/create'"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors"
      >
        <i class="bx bx-plus"></i> Enregistrer une récolte
      </NuxtLink>
    </div>

    <!-- ===== MODAL SUPPRESSION ===== -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="deleteModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/25 backdrop-blur-sm" @click="deleteModal.show = false"></div>
          <div class="relative bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm border border-gray-100">
            <div class="flex items-start gap-4 mb-5">
              <div class="w-10 h-10 bg-rose-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <i class="bx bx-trash text-rose-500 text-lg"></i>
              </div>
              <div>
                <h3 class="text-[15px] font-semibold text-gray-900 mb-1">Supprimer l'enregistrement</h3>
                <p class="text-[13px] text-gray-500 leading-relaxed">
                  Récolte du <span class="font-semibold text-gray-700">{{ deleteModal.record ? formatDate(deleteModal.record.date) : '' }}</span> —
                  <span class="font-semibold text-gray-700">{{ deleteModal.record?.yield_amount }} kg</span>.
                  Cette action est irréversible.
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3 justify-end">
              <button @click="deleteModal.show = false" class="px-4 py-2 text-[13px] font-semibold text-gray-500 hover:text-gray-700 transition-colors">
                Annuler
              </button>
              <button
                @click="executeDelete"
                :disabled="deleteModal.loading"
                class="px-5 py-2 bg-rose-500 text-white rounded-xl text-[13px] font-semibold hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                <i v-if="deleteModal.loading" class="bx bx-loader-alt animate-spin"></i>
                <i v-else class="bx bx-trash"></i>
                Supprimer
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ===== TOAST ===== -->
    <Transition name="toast-slide">
      <div v-if="toast.show" class="fixed bottom-6 right-6 z-50">
        <div :class="[
          'flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg text-white text-[13px] font-semibold',
          toast.type === 'success' ? 'bg-[#013b28]' : 'bg-rose-500'
        ]">
          <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'"></i>
          {{ toast.message }}
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" })

import { ref, computed, onMounted, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"

const route  = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

// ===== STATE =====
const isLoading    = ref(true)
const yields       = ref<any[]>([])
const searchQuery  = ref("")
const sortBy       = ref<"date" | "yield">("date")
const currentPage  = ref(1)
const perPage      = 8
const parcelCropId = ref("")
const parcelCropName = ref("")

const deleteModal = ref({ show: false, record: null as any, loading: false })
const toast = ref({ show: false, message: "", type: "success" as "success" | "error" })

// ===== HELPERS =====
function formatDate(d: string) {
  if (!d) return "—"
  return new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}
function formatNumber(n: number | null | undefined) {
  if (n == null) return "—"
  return new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1 }).format(n)
}
function yieldRatio(y: any) {
  if (!y.area || !y.yield_amount) return "—"
  return (y.yield_amount / y.area).toFixed(2)
}
function getYieldRatioColor(y: any) {
  const ratio = y.area && y.yield_amount ? y.yield_amount / y.area : 0
  if (ratio >= 0.5) return "text-emerald-600"
  if (ratio >= 0.2) return "text-amber-600"
  return "text-rose-500"
}
function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3500)
}

// ===== COMPUTED =====
const filteredYields = computed(() => {
  let list = yields.value
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(y =>
      y.parcelName?.toLowerCase().includes(q) ||
      y.cropName?.toLowerCase().includes(q)
    )
  }
  return [...list].sort((a, b) => {
    if (sortBy.value === "yield") return (b.yield_amount ?? 0) - (a.yield_amount ?? 0)
    return new Date(b.date).getTime() - new Date(a.date).getTime()
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredYields.value.length / perPage)))

const paginatedYields = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredYields.value.slice(start, start + perPage)
})

const stats = computed(() => {
  const all = yields.value
  const totalQty   = all.reduce((s, y) => s + (y.yield_amount ?? 0), 0)
  const totalArea  = all.reduce((s, y) => s + (y.area ?? 0), 0)
  const avgPerM2   = totalArea > 0 ? totalQty / totalArea : 0
  const best       = all.reduce((max, y) => (y.yield_amount ?? 0) > (max?.yield_amount ?? 0) ? y : max, null as any)

  return [
    { label: "Récoltes",      value: all.length,                    unit: "",       icon: "bx-list-check",     iconBg: "bg-gray-100 text-gray-500"     },
    { label: "Total récolté", value: formatNumber(totalQty),        unit: "kg",     icon: "bx-package",        iconBg: "bg-emerald-50 text-emerald-600" },
    { label: "Rendement moy.", value: avgPerM2.toFixed(2),          unit: "kg/m²",  icon: "bx-trending-up",    iconBg: "bg-blue-50 text-blue-500"       },
    { label: "Meilleure récolte", value: formatNumber(best?.yield_amount), unit: "kg", icon: "bx-trophy", iconBg: "bg-amber-50 text-amber-500"    },
  ]
})

// ===== DATA =====
async function fetchYields() {
  const endpoint = parcelCropId.value
    ? `/api/yield-records/?parcel_crop=${parcelCropId.value}`
    : "/api/yield-records/"
  const raw: any = await apiFetch(endpoint)
  const results = raw?.results ?? raw ?? []

  // Si on est en contexte d'une plantation précise, parcelCropName est déjà chargé
  // dans onMounted — on évite N appels API individuels par enregistrement.
  if (parcelCropId.value && parcelCropName.value) {
    const [parcelPart, cropPart] = parcelCropName.value.split(" – ")
    yields.value = results.map((y: any) => ({
      ...y,
      parcelName: parcelPart ?? null,
      cropName:   cropPart   ?? null,
    }))
    return
  }

  // Sans contexte plantation : on résout les noms pour chaque enregistrement
  yields.value = await Promise.all(results.map(async (y: any) => {
    if (y.parcelCrop) {
      try {
        const pc: any = await apiFetch(`/api/parcel-crops/${y.parcelCrop}/`)
        const p: any  = await apiFetch(`/api/parcels/${pc.parcel}/`)
        return { ...y, parcelName: p.parcel_name, cropName: pc.crop?.name ?? null }
      } catch { /* ignore */ }
    }
    return { ...y, parcelName: null, cropName: null }
  }))
}

// ===== ACTIONS =====
function goEdit(id: number) {
  router.push(`/farmer/parcels/crops/show/yields/edit/${id}`)
}
function openDeleteModal(record: any) {
  deleteModal.value = { show: true, record, loading: false }
}
async function executeDelete() {
  if (!deleteModal.value.record) return
  deleteModal.value.loading = true
  try {
    await apiFetch(`/api/yield-records/${deleteModal.value.record.id}/`, { method: "DELETE" })
    yields.value = yields.value.filter(y => y.id !== deleteModal.value.record.id)
    deleteModal.value.show = false
    showToast("Enregistrement supprimé.")
  } catch {
    showToast("Erreur lors de la suppression.", "error")
  } finally {
    deleteModal.value.loading = false
  }
}

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  if (route.query.parcel_crop) parcelCropId.value = String(route.query.parcel_crop)

  if (parcelCropId.value) {
    try {
      const pc: any = await apiFetch(`/api/parcel-crops/${parcelCropId.value}/`)
      const p: any  = await apiFetch(`/api/parcels/${pc.parcel}/`)
      parcelCropName.value = `${p.parcel_name} – ${pc.crop?.name ?? "Plantation"}`
    } catch {
      parcelCropName.value = "Plantation"
    }
  }

  try {
    await fetchYields()
  } catch {
    showToast("Erreur lors du chargement des données.", "error")
  } finally {
    isLoading.value = false
  }
})

watch([searchQuery, sortBy], () => { currentPage.value = 1 })
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(12px); }
.toast-slide-leave-to   { opacity: 0; transform: translateY(12px); }
</style>