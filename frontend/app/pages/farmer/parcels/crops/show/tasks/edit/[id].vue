<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Modifier la tâche">
      <template #subtitle>
        <i class="bx bx-edit"></i>
        Mettez à jour les informations de la tâche
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
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/crops/show/tasks?parcel_crop=${parcelCropId}`" class="hover:text-[#10b481] transition-colors">
            Tâches
          </NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Modifier</span>
      </template>
    </PageHeader>

    <!-- Loading state -->
    <div v-if="initialLoading" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <i class="bx bx-loader-alt animate-spin text-3xl"></i>
      <p class="text-[13px]">Chargement de la tâche…</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- ===== FORM ===== -->
      <div class="lg:col-span-2">
        <form @submit.prevent="submitTask" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 md:p-8 space-y-6">

          <!-- Nom -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Nom de la tâche <span class="text-rose-400">*</span></label>
            <div class="relative">
              <i class="bx bx-task absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
              <input
                v-model="form.name"
                type="text"
                required
                placeholder="Ex : Traitement fongicide parcelle Nord"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
              >
            </div>
          </div>

          <!-- Date + Priorité -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Date d'échéance <span class="text-rose-400">*</span></label>
              <div class="relative">
                <i class="bx bx-calendar-event absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
                <input
                  v-model="form.due_date"
                  type="date"
                  required
                  class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all"
                >
              </div>
            </div>

            <div class="space-y-2">
              <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Priorité <span class="text-rose-400">*</span></label>
              <div class="flex items-center gap-2">
                <button
                  v-for="p in priorities"
                  :key="p.id"
                  type="button"
                  @click="form.priority = p.id"
                  :class="[
                    'flex-1 py-3 rounded-xl text-[12px] font-semibold border transition-all',
                    form.priority === p.id
                      ? getPriorityActive(p.name)
                      : 'bg-gray-50 border-gray-100 text-gray-400 hover:bg-gray-100'
                  ]"
                >
                  {{ getPriorityLabel(p.name) }}
                </button>
              </div>
            </div>
          </div>

          <!-- Plantation (verrouillée) -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Plantation</label>
            <div class="relative">
              <i class="bx bx-leaf absolute left-4 top-1/2 -translate-y-1/2 text-emerald-400 text-lg pointer-events-none z-10"></i>
              <div class="w-full pl-11 pr-4 py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-[14px] text-[#013b28] font-semibold flex items-center justify-between">
                <span>{{ parcelCropName || `Plantation #${form.parcelCrop}` }}</span>
                <span class="flex items-center gap-1 text-[10px] font-black text-emerald-600 uppercase tracking-widest flex-shrink-0">
                  <i class="bx bx-lock-alt text-sm"></i> Fixé
                </span>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="Détails de la mission, matériel nécessaire…"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] resize-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
            ></textarea>
          </div>

          <!-- Statut -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Statut</label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button
                v-for="s in statuses"
                :key="s.id"
                type="button"
                @click="form.status = s.id"
                :class="[
                  'py-2.5 rounded-xl text-[12px] font-semibold border transition-all',
                  form.status === s.id
                    ? getStatusActive(s.name)
                    : 'bg-gray-50 border-gray-100 text-gray-400 hover:bg-gray-100'
                ]"
              >
                {{ getStatusLabel(s.name) }}
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-3 pt-2 border-t border-gray-50">
            <NuxtLink
              :to="parcelCropId ? `/farmer/parcels/crops/show/tasks?parcel_crop=${parcelCropId}` : '/farmer/parcels/crops/show/tasks'"
              class="px-5 py-2.5 text-[13px] font-semibold text-gray-500 hover:text-gray-700 transition-colors"
            >
              Annuler
            </NuxtLink>
            <button
              type="submit"
              :disabled="isLoading"
              class="px-6 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-colors shadow-sm disabled:opacity-50 flex items-center gap-2"
            >
              <i v-if="isLoading" class="bx bx-loader-alt animate-spin"></i>
              <i v-else class="bx bx-save"></i>
              Sauvegarder les modifications
            </button>
          </div>
        </form>
      </div>

      <!-- ===== SIDEBAR ===== -->
      <div class="space-y-4">
        <!-- Current state recap -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 space-y-3">
          <p class="text-[12px] font-semibold text-gray-500 uppercase tracking-wider">État actuel</p>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Tâche</span>
              <span class="font-semibold text-gray-700 text-right max-w-[60%] truncate">{{ form.name || '—' }}</span>
            </div>
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Échéance</span>
              <span class="font-semibold text-gray-700">{{ form.due_date ? formatDate(form.due_date) : '—' }}</span>
            </div>
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Priorité</span>
              <span :class="['px-2 py-0.5 rounded-lg text-[11px] font-semibold', getPriorityBadge()]">
                {{ getPriorityLabel(currentPriorityName) }}
              </span>
            </div>
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Statut</span>
              <span :class="['px-2 py-0.5 rounded-lg text-[11px] font-semibold', getStatusBadge()]">
                {{ getStatusLabel(currentStatusName) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Danger zone -->
        <div class="bg-rose-50 rounded-2xl border border-rose-100 p-5">
          <p class="text-[12px] font-semibold text-rose-500 uppercase tracking-wider mb-3">Zone dangereuse</p>
          <p class="text-[13px] text-rose-700/70 leading-relaxed mb-4">
            La suppression de cette tâche est définitive et ne peut pas être annulée.
          </p>
          <button
            type="button"
            @click="openDeleteModal"
            class="w-full py-2.5 bg-white border border-rose-200 text-rose-500 rounded-xl text-[13px] font-semibold hover:bg-rose-500 hover:text-white transition-all"
          >
            <i class="bx bx-trash mr-1.5"></i> Supprimer cette tâche
          </button>
        </div>
      </div>

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
                  Voulez-vous supprimer <span class="font-semibold text-gray-700">« {{ form.name }} »</span> ? Cette action est irréversible.
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

import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"

const route  = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

// ===== STATE =====
const initialLoading = ref(true)
const isLoading      = ref(false)
const priorities     = ref<any[]>([])
const statuses       = ref<any[]>([])
const parcelCrops    = ref<any[]>([])
const deleteModal    = ref({ show: false, loading: false })
const toast          = ref({ show: false, message: "", type: "success" as "success" | "error" })

const form = ref({
  name:        "",
  description: "",
  due_date:    "",
  parcelCrop:  "" as number | string,
  priority:    "" as number | string,
  status:      "" as number | string,
})

// ===== COMPUTED =====
// Plantation fixée depuis ?parcel_crop= (navigation depuis la page show)
const parcelCropId = computed(() =>
  route.query.parcel_crop ? Number(route.query.parcel_crop) : null
)
const parcelCropName = computed(() => {
  const id = parcelCropId.value ?? form.value.parcelCrop
  const pc = parcelCrops.value.find((p: any) => p.id === id)
  return pc?.fullName ?? ""
})

const currentPriorityName = computed(() => {
  const p = priorities.value.find((p: any) => p.id === form.value.priority)
  return p?.name ?? ""
})
const currentStatusName = computed(() => {
  const s = statuses.value.find((s: any) => s.id === form.value.status)
  return s?.name ?? ""
})

// ===== HELPERS =====
function getPriorityLabel(name: string) {
  const map: Record<string, string> = { High: "Haute", Medium: "Moyenne", Low: "Faible" }
  return map[name] ?? name ?? "—"
}
function getPriorityActive(name: string) {
  if (name === "High")   return "bg-rose-500 border-rose-500 text-white"
  if (name === "Medium") return "bg-amber-500 border-amber-500 text-white"
  return "bg-emerald-600 border-emerald-600 text-white"
}
function getPriorityBadge() {
  const name = currentPriorityName.value
  if (name === "High")   return "bg-rose-50 text-rose-600"
  if (name === "Medium") return "bg-amber-50 text-amber-600"
  return "bg-emerald-50 text-emerald-600"
}
function getStatusLabel(name: string) {
  const map: Record<string, string> = {
    Planned: "Planifiée", "In Progress": "En cours", Done: "Terminée", Cancelled: "Annulée", Pending: "En attente",
  }
  return map[name] ?? name ?? "—"
}
function getStatusActive(name: string) {
  if (name === "Done")        return "bg-emerald-600 border-emerald-600 text-white"
  if (name === "In Progress") return "bg-sky-500 border-sky-500 text-white"
  if (name === "Cancelled")   return "bg-gray-500 border-gray-500 text-white"
  if (name === "Planned")     return "bg-blue-500 border-blue-500 text-white"
  return "bg-amber-500 border-amber-500 text-white"
}
function getStatusBadge() {
  const name = currentStatusName.value
  if (name === "Done")        return "bg-emerald-50 text-emerald-600"
  if (name === "In Progress") return "bg-sky-50 text-sky-600"
  if (name === "Cancelled")   return "bg-gray-100 text-gray-500"
  if (name === "Planned")     return "bg-blue-50 text-blue-600"
  return "bg-amber-50 text-amber-600"
}
function formatDate(d: string) {
  if (!d) return "—"
  return new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}
function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3500)
}

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  try {
    const [task, priData, staData, cropData]: [any, any, any, any] = await Promise.all([
      apiFetch(`/api/tasks/${route.params.id}/`),
      apiFetch("/api/task-priority/"),
      apiFetch("/api/task-status/"),
      apiFetch("/api/parcel-crops/"),
    ])

    priorities.value = priData?.results ?? priData ?? []
    statuses.value   = staData?.results  ?? staData  ?? []

    const crops = cropData?.results ?? cropData ?? []
    parcelCrops.value = crops.map((pc: any) => ({
      ...pc,
      fullName: `${pc.parcel?.parcel_name ?? `Parcelle #${pc.parcel}`} — ${pc.crop?.name ?? `Culture #${pc.crop}`}`,
    }))

    // Remplir le formulaire
    form.value = {
      name:        task.name        ?? "",
      description: task.description ?? "",
      due_date:    task.due_date    ?? "",
      parcelCrop:  task.parcelCrop  ?? "",
      priority:    task.priority    ?? "",
      status:      task.status      ?? "",
    }
  } catch {
    showToast("Erreur lors du chargement de la tâche.", "error")
  } finally {
    initialLoading.value = false
  }
})

// ===== SUBMIT =====
async function submitTask() {
  const { name, due_date, parcelCrop, priority, status } = form.value
  if (!name || !due_date || !parcelCrop || !priority || !status) {
    showToast("Veuillez remplir tous les champs obligatoires.", "error")
    return
  }

  isLoading.value = true
  try {
    await apiFetch(`/api/tasks/${route.params.id}/`, {
      method: "PATCH",
      body: {
        name:        form.value.name,
        description: form.value.description || null,
        due_date:    form.value.due_date,
        parcelCrop:  Number(form.value.parcelCrop),
        priority:    Number(form.value.priority),
        status:      Number(form.value.status),
      },
    })
    showToast("Tâche mise à jour avec succès !")
    const backPath = parcelCropId.value
      ? `/farmer/parcels/crops/show/tasks?parcel_crop=${parcelCropId.value}`
      : "/farmer/parcels/crops/show/tasks"
    setTimeout(() => router.push(backPath), 1500)
  } catch {
    showToast("Erreur lors de la mise à jour.", "error")
  } finally {
    isLoading.value = false
  }
}

// ===== DELETE =====
function openDeleteModal() {
  deleteModal.value = { show: true, loading: false }
}
async function executeDelete() {
  deleteModal.value.loading = true
  try {
    await apiFetch(`/api/tasks/${route.params.id}/`, { method: "DELETE" })
    showToast("Tâche supprimée.")
    const backPath = parcelCropId.value
      ? `/farmer/parcels/crops/show/tasks?parcel_crop=${parcelCropId.value}`
      : "/farmer/parcels/crops/show/tasks"
    setTimeout(() => router.push(backPath), 1200)
  } catch {
    showToast("Erreur lors de la suppression.", "error")
    deleteModal.value.loading = false
  }
}
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(12px); }
.toast-slide-leave-to   { opacity: 0; transform: translateY(12px); }
</style>