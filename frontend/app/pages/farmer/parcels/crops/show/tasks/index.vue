<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="`${cropName || 'Plantation'} — Tâches`">
      <template #subtitle>
        <i class="bx bx-task"></i>
        {{ filteredTasks.length }} tâche{{ filteredTasks.length !== 1 ? 's' : '' }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <template v-if="parcelId">
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/show/${parcelId}`" class="hover:text-[#10b481] transition-colors">
            {{ parcelName || 'Parcelle' }}
          </NuxtLink>
        </template>
        <template v-if="parcelCropId">
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/crops/show/${parcelCropId}`" class="hover:text-[#10b481] transition-colors">
            {{ cropName || 'Plantation' }}
          </NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Tâches</span>
      </template>
    </PageHeader>
    <div class="flex justify-end mb-8">
      <NuxtLink
        :to="createTaskPath"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors shadow-sm whitespace-nowrap"
      >
        <i class="bx bx-plus text-base"></i> Nouvelle tâche
      </NuxtLink>
    </div>

    <!-- ===== STATS ===== -->
    <div v-if="!isLoading && tasks.length" class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <div v-for="stat in stats" :key="stat.label" class="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <span :class="['w-9 h-9 rounded-xl flex items-center justify-center text-base', stat.iconBg]">
            <i :class="['bx', stat.icon]"></i>
          </span>
          <span class="text-[26px] font-bold text-gray-900">{{ stat.count }}</span>
        </div>
        <p class="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">{{ stat.label }}</p>
      </div>
    </div>

    <!-- ===== FILTERS ===== -->
    <div v-if="!isLoading" class="bg-white rounded-2xl border border-gray-100 shadow-sm mb-5 px-4 py-3">
      <div class="flex flex-col sm:flex-row sm:items-center gap-3">
        <div class="relative max-w-xs w-full sm:w-auto flex-shrink-0">
          <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher une tâche…"
            class="w-full pl-9 pr-4 py-2 bg-gray-50 border border-gray-100 rounded-xl text-[13px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 transition-all"
          >
        </div>
        <div class="flex items-center gap-2 flex-wrap">
          <button
            v-for="f in statusFilters"
            :key="f.value"
            @click="activeStatus = f.value; currentPage = 1"
            :class="[
              'px-3 py-1.5 rounded-xl text-[12px] font-semibold transition-all',
              activeStatus === f.value
                ? 'bg-[#013b28] text-white'
                : 'bg-gray-50 text-gray-500 hover:bg-gray-100'
            ]"
          >
            {{ f.label }}
            <span v-if="f.value !== 'ALL'" class="ml-1 opacity-60 text-[11px]">{{ countByStatus(f.value) }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <i class="bx bx-loader-alt animate-spin text-3xl"></i>
      <p class="text-[13px]">Chargement des tâches…</p>
    </div>

    <!-- ===== TABLE ===== -->
    <template v-else-if="paginatedTasks.length">
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-gray-100 bg-gray-50/50">
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400">Tâche</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400">Échéance</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-center">Priorité</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-center">Statut</th>
                <th class="px-6 py-3.5 text-[11px] font-semibold uppercase tracking-widest text-gray-400 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr
                v-for="task in paginatedTasks"
                :key="task.id"
                class="group hover:bg-gray-50/60 transition-colors"
              >
                <td class="px-6 py-4">
                  <p class="text-[14px] font-semibold text-gray-900">{{ task.name }}</p>
                  <p v-if="task.description" class="text-[12px] text-gray-400 mt-0.5 line-clamp-1">{{ task.description }}</p>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-1.5">
                    <i :class="['bx bx-calendar text-sm', isOverdue(task) ? 'text-rose-400' : 'text-gray-300']"></i>
                    <span :class="['text-[13px]', isOverdue(task) ? 'text-rose-500 font-semibold' : 'text-gray-500']">
                      {{ formatDate(task.due_date) }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <span :class="['inline-flex items-center px-2.5 py-1 rounded-lg text-[11px] font-semibold', priorityClass(task.priorityName)]">
                    {{ priorityLabel(task.priorityName) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-semibold', statusClass(task.statusName)]">
                    <span :class="['w-1.5 h-1.5 rounded-full flex-shrink-0', statusDot(task.statusName)]"></span>
                    {{ statusLabel(task.statusName) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="goEdit(task.id)"
                      class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-amber-500 hover:border-amber-200 transition-all shadow-sm"
                      title="Modifier"
                    >
                      <i class="bx bx-edit-alt text-base"></i>
                    </button>
                    <button
                      @click="openDeleteModal(task)"
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
            {{ (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, filteredTasks.length) }} sur {{ filteredTasks.length }}
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
        <i class="bx bx-task text-3xl text-emerald-500"></i>
      </div>
      <h3 class="text-[16px] font-semibold text-gray-900 mb-2">Aucune tâche trouvée</h3>
      <p class="text-[13px] text-gray-400 mb-6 max-w-xs leading-relaxed">
        {{ activeStatus !== 'ALL' ? 'Aucune tâche pour ce statut.' : 'Créez votre première tâche agricole pour démarrer.' }}
      </p>
      <NuxtLink
        :to="createTaskPath"
        class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors"
      >
        <i class="bx bx-plus"></i> Créer une tâche
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
                <h3 class="text-[15px] font-semibold text-gray-900 mb-1">Supprimer la tâche</h3>
                <p class="text-[13px] text-gray-500 leading-relaxed">
                  Voulez-vous supprimer <span class="font-semibold text-gray-700">« {{ deleteModal.task?.name }} »</span> ?
                  Cette action est irréversible.
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3 justify-end">
              <button
                @click="deleteModal.show = false"
                class="px-4 py-2 text-[13px] font-semibold text-gray-500 hover:text-gray-700 transition-colors"
              >
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
const isLoading      = ref(true)
const tasks          = ref<any[]>([])
const searchQuery    = ref("")
const activeStatus   = ref("ALL")
const currentPage    = ref(1)
const perPage        = 8
const parcelCropId   = ref("")
const parcelCropName = ref("") // "[parcelName] – [cropName]" utilisé pour les filtres
const parcelId       = ref("")
const parcelName     = ref("")
const cropName       = ref("")

const priorities = ref<Record<number, string>>({})
const statuses   = ref<Record<number, string>>({})

const deleteModal = ref({ show: false, task: null as any, loading: false })
const toast = ref({ show: false, message: "", type: "success" as "success" | "error" })

const statusFilters = [
  { label: "Toutes",     value: "ALL"         },
  { label: "Planifiée",  value: "Planned"     },
  { label: "En cours",   value: "In Progress" },
  { label: "Terminée",   value: "Done"        },
  { label: "Annulée",    value: "Cancelled"   },
]

// ===== HELPERS VISUELS =====
function priorityLabel(name: string) {
  if (name === "High")   return "Haute"
  if (name === "Medium") return "Moyenne"
  if (name === "Low")    return "Faible"
  return name || "—"
}
function priorityClass(name: string) {
  if (name === "High")   return "bg-rose-50 text-rose-600"
  if (name === "Medium") return "bg-amber-50 text-amber-600"
  return "bg-emerald-50 text-emerald-600"
}
function statusLabel(name: string) {
  const map: Record<string, string> = {
    "Planned":     "Planifiée",
    "In Progress": "En cours",
    "Done":        "Terminée",
    "Cancelled":   "Annulée",
    "Pending":     "En attente",
  }
  return map[name] ?? name ?? "—"
}
function statusClass(name: string) {
  if (name === "Done")        return "bg-emerald-50 text-emerald-600"
  if (name === "In Progress") return "bg-sky-50 text-sky-600"
  if (name === "Cancelled")   return "bg-gray-50 text-gray-500"
  if (name === "Planned")     return "bg-blue-50 text-blue-600"
  return "bg-amber-50 text-amber-600"
}
function statusDot(name: string) {
  if (name === "Done")        return "bg-emerald-500"
  if (name === "In Progress") return "bg-sky-500"
  if (name === "Cancelled")   return "bg-gray-400"
  if (name === "Planned")     return "bg-blue-500"
  return "bg-amber-500"
}
function isOverdue(task: any) {
  if (!task.due_date) return false
  const statusName = task.statusName
  if (statusName === "Done" || statusName === "Cancelled") return false
  return new Date(task.due_date) < new Date()
}
function formatDate(d: string) {
  if (!d) return "—"
  return new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}

// ===== COMPUTED =====
const filteredTasks = computed(() => {
  let list = tasks.value
  if (activeStatus.value !== "ALL") {
    list = list.filter(t => t.statusName === activeStatus.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(t =>
      t.name?.toLowerCase().includes(q) ||
      t.description?.toLowerCase().includes(q)
    )
  }
  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredTasks.value.length / perPage)))

const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredTasks.value.slice(start, start + perPage)
})

const createTaskPath = computed(() =>
  parcelCropId.value
    ? `/farmer/parcels/crops/show/tasks/create?parcel_crop=${parcelCropId.value}`
    : '/farmer/parcels/crops/show/tasks/create'
)

const stats = computed(() => {
  const all = tasks.value
  return [
    { label: "Total",     count: all.length,                                                              icon: "bx-list-ul",        iconBg: "bg-gray-100 text-gray-500"    },
    { label: "Planifiées",  count: all.filter(t => t.statusName === "Planned").length,                   icon: "bx-calendar-check", iconBg: "bg-blue-50 text-blue-500"     },
    { label: "En cours",  count: all.filter(t => t.statusName === "In Progress").length,                 icon: "bx-time-five",      iconBg: "bg-amber-50 text-amber-500"   },
    { label: "Terminées", count: all.filter(t => t.statusName === "Done").length,                        icon: "bx-check-circle",   iconBg: "bg-emerald-50 text-emerald-500"},
  ]
})

function countByStatus(val: string) {
  return tasks.value.filter(t => t.statusName === val).length
}

// ===== DATA =====
async function loadLookups() {
  const [pData, sData]: [any, any] = await Promise.all([
    apiFetch("/api/task-priority/"),
    apiFetch("/api/task-status/"),
  ])
  priorities.value = Object.fromEntries((pData?.results ?? pData ?? []).map((p: any) => [p.id, p.name]))
  statuses.value   = Object.fromEntries((sData?.results  ?? sData  ?? []).map((s: any) => [s.id, s.name]))
}

async function fetchTasks() {
  // parcelCropId est toujours présent (redirect enforced dans onMounted)
  const raw: any = await apiFetch(`/api/tasks/?parcel_crop=${parcelCropId.value}`)
  const results = raw?.results ?? raw ?? []
  tasks.value = results.map((t: any) => ({
    ...t,
    // Le serializer retourne priority_detail.name et status_detail.name directement
    // On garde le fallback sur la table de lookup pour robustesse
    priorityName:   t.priority_detail?.name ?? priorities.value[t.priority] ?? "",
    statusName:     t.status_detail?.name   ?? statuses.value[t.status]     ?? "",
    parcelCropFull: parcelCropName.value,
  }))
}

// ===== ACTIONS =====
function goEdit(id: number) {
  const query = parcelCropId.value ? `?parcel_crop=${parcelCropId.value}` : ''
  router.push(`/farmer/parcels/crops/show/tasks/edit/${id}${query}`)
}

function openDeleteModal(task: any) {
  deleteModal.value = { show: true, task, loading: false }
}

async function executeDelete() {
  if (!deleteModal.value.task) return
  deleteModal.value.loading = true
  try {
    await apiFetch(`/api/tasks/${deleteModal.value.task.id}/`, { method: "DELETE" })
    tasks.value = tasks.value.filter(t => t.id !== deleteModal.value.task.id)
    deleteModal.value.show = false
    showToast("Tâche supprimée avec succès.")
  } catch {
    showToast("Erreur lors de la suppression.", "error")
  } finally {
    deleteModal.value.loading = false
  }
}

function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3500)
}

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  if (route.query.parcel_crop) parcelCropId.value = String(route.query.parcel_crop)
  if (route.query.status)      activeStatus.value = String(route.query.status)

  // Cette page exige toujours un contexte de plantation
  if (!parcelCropId.value) {
    return router.push("/farmer/parcels")
  }

  try {
    const pc: any = await apiFetch(`/api/parcel-crops/${parcelCropId.value}/`)
    const p: any  = await apiFetch(`/api/parcels/${pc.parcel}/`)
    parcelId.value   = String(pc.parcel)
    parcelName.value = p.parcel_name || p.name || "Parcelle"
    cropName.value   = pc.crop?.name ?? "Plantation"
    parcelCropName.value = `${parcelName.value} – ${cropName.value}`
  } catch {
    parcelCropName.value = "Plantation"
    cropName.value = "Plantation"
  }

  try {
    await loadLookups()
    await fetchTasks()
  } catch {
    showToast("Erreur lors du chargement des données.", "error")
  } finally {
    isLoading.value = false
  }
})

watch([searchQuery, activeStatus], () => { currentPage.value = 1 })
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(12px); }
.toast-slide-leave-to   { opacity: 0; transform: translateY(12px); }
</style>
