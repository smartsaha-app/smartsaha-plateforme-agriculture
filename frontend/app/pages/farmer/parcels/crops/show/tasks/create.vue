<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Planifier une tâche">
      <template #subtitle>
        <i class="bx bx-plus-circle"></i>
        Renseignez les détails de la tâche agricole
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <template v-if="preselectedCrop">
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/crops/show/${preselectedCrop.id}`" class="hover:text-[#10b481] transition-colors">
            {{ preselectedCrop.fullName }}
          </NuxtLink>
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink :to="`/farmer/parcels/crops/show/tasks?parcel_crop=${preselectedCrop.id}`" class="hover:text-[#10b481] transition-colors">
            Tâches
          </NuxtLink>
        </template>
        <template v-else>
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink to="/farmer/parcels/crops/show/tasks" class="hover:text-[#10b481] transition-colors">Tâches</NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Nouvelle tâche</span>
      </template>
    </PageHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

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

          <!-- Plantation -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Plantation <span class="text-rose-400">*</span></label>
            <div class="relative">
              <i class="bx bx-leaf absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none z-10"></i>

              <!-- Plantation verrouillée (contexte spécifique) -->
              <template v-if="preselectedCrop">
                <div class="w-full pl-11 pr-4 py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-[14px] text-[#013b28] font-semibold flex items-center justify-between">
                  <span>{{ preselectedCrop.fullName }}</span>
                  <span class="flex items-center gap-1 text-[10px] font-black text-emerald-600 uppercase tracking-widest ml-3 flex-shrink-0">
                    <i class="bx bx-lock-alt text-sm"></i> Fixée
                  </span>
                </div>
              </template>

              <!-- Select normal si pas de contexte -->
              <template v-else>
                <select
                  v-model="form.parcelCrop"
                  required
                  class="w-full pl-11 pr-10 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] text-gray-700 appearance-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all"
                >
                  <option value="" disabled>Sélectionner une plantation…</option>
                  <option v-for="pc in parcelCrops" :key="pc.id" :value="pc.id">{{ pc.fullName }}</option>
                </select>
                <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
              </template>
            </div>
          </div>

          <!-- Description -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Description</label>
            <textarea
              v-model="form.description"
              rows="3"
              placeholder="Détails de la mission, matériel nécessaire, instructions particulières…"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] resize-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
            ></textarea>
          </div>

          <!-- Statut -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Statut initial</label>
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
              :to="preselectedCrop
                ? `/farmer/parcels/crops/show/tasks?parcel_crop=${preselectedCrop.id}`
                : '/farmer/parcels/crops/show/tasks'"
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
              <i v-else class="bx bx-check"></i>
              Enregistrer la tâche
            </button>
          </div>
        </form>
      </div>

      <!-- ===== SIDEBAR ===== -->
      <div class="space-y-4">
        <!-- Info card -->
        <div class="bg-[#013b28] rounded-2xl p-6 text-white relative overflow-hidden">
          <div class="absolute -right-8 -top-8 w-32 h-32 bg-[#10b481]/10 rounded-full blur-2xl"></div>
          <div class="relative">
            <div class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center mb-4">
              <i class="bx bx-info-circle text-[#10b481] text-xl"></i>
            </div>
            <h3 class="text-[15px] font-semibold mb-2">Planification efficace</h3>
            <p class="text-[13px] text-white/60 leading-relaxed">
              Une bonne organisation des tâches agricoles permet d'optimiser les rendements et d'anticiper les problèmes.
            </p>
          </div>
        </div>

        <!-- Priorités -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 space-y-3">
          <p class="text-[12px] font-semibold text-gray-500 uppercase tracking-wider">Guide des priorités</p>
          <div class="space-y-2">
            <div class="flex items-center gap-3">
              <span class="w-2 h-2 rounded-full bg-rose-500 flex-shrink-0"></span>
              <div>
                <p class="text-[13px] font-semibold text-gray-700">Haute</p>
                <p class="text-[11px] text-gray-400">Action immédiate requise</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="w-2 h-2 rounded-full bg-amber-500 flex-shrink-0"></span>
              <div>
                <p class="text-[13px] font-semibold text-gray-700">Moyenne</p>
                <p class="text-[11px] text-gray-400">Dans la semaine</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0"></span>
              <div>
                <p class="text-[13px] font-semibold text-gray-700">Faible</p>
                <p class="text-[11px] text-gray-400">Peut attendre</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tip -->
        <div class="bg-emerald-50 rounded-2xl border border-emerald-100 p-5 flex gap-3">
          <i class="bx bx-bulb text-emerald-500 text-xl flex-shrink-0 mt-0.5"></i>
          <p class="text-[13px] text-emerald-700 leading-relaxed italic">
            "Vérifier régulièrement l'état des cultures permet de détecter les maladies précocement et de limiter les pertes."
          </p>
        </div>
      </div>

    </div>

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
const isLoading   = ref(false)
const priorities  = ref<any[]>([])
const statuses    = ref<any[]>([])
const parcelCrops = ref<any[]>([])
const toast = ref({ show: false, message: "", type: "success" as "success" | "error" })

// Plantation pré-sélectionnée via ?parcel_crop=<id> (navigation depuis tasks/index)
const preselectedCrop = computed(() => {
  const id = route.query.parcel_crop ? String(route.query.parcel_crop) : ""
  if (!id) return null
  return parcelCrops.value.find((pc: any) => String(pc.id) === id) ?? null
})

const form = ref({
  name:        "",
  description: "",
  due_date:    "",
  parcelCrop:  "" as number | string,
  priority:    "" as number | string,
  status:      "" as number | string,
})

// ===== HELPERS =====
function getPriorityLabel(name: string) {
  const map: Record<string, string> = { High: "Haute", Medium: "Moyenne", Low: "Faible" }
  return map[name] ?? name
}
function getPriorityActive(name: string) {
  if (name === "High")   return "bg-rose-500 border-rose-500 text-white"
  if (name === "Medium") return "bg-amber-500 border-amber-500 text-white"
  return "bg-emerald-600 border-emerald-600 text-white"
}
function getStatusLabel(name: string) {
  const map: Record<string, string> = {
    Planned: "Planifiée", "In Progress": "En cours", Done: "Terminée", Cancelled: "Annulée", Pending: "En attente",
  }
  return map[name] ?? name
}
function getStatusActive(name: string) {
  if (name === "Done")        return "bg-emerald-600 border-emerald-600 text-white"
  if (name === "In Progress") return "bg-sky-500 border-sky-500 text-white"
  if (name === "Cancelled")   return "bg-gray-500 border-gray-500 text-white"
  if (name === "Planned")     return "bg-blue-500 border-blue-500 text-white"
  return "bg-amber-500 border-amber-500 text-white"
}

function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3500)
}

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  // Pré-remplir plantation si ?parcel_crop= dans l'URL
  if (route.query.parcel_crop) {
    form.value.parcelCrop = String(route.query.parcel_crop)
  }

  try {
    const [priData, staData, cropData]: [any, any, any] = await Promise.all([
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

    // Statut par défaut : Planifiée
    const planned = statuses.value.find((s: any) => s.name === "Planned")
    if (planned) form.value.status = planned.id
  } catch {
    showToast("Erreur lors du chargement des données.", "error")
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
    await apiFetch("/api/tasks/", {
      method: "POST",
      body: {
        name:        form.value.name,
        description: form.value.description || null,
        due_date:    form.value.due_date,
        parcelCrop:  Number(form.value.parcelCrop),
        priority:    Number(form.value.priority),
        status:      Number(form.value.status),
      },
    })
    showToast("Tâche créée avec succès !")
    const parcelCropId = route.query.parcel_crop ? String(route.query.parcel_crop) : ""
    const redirect = parcelCropId
      ? `/farmer/parcels/crops/show/tasks?parcel_crop=${parcelCropId}`
      : "/farmer/parcels/crops/show/tasks"
    setTimeout(() => router.push(redirect), 1500)
  } catch {
    showToast("Erreur lors de l'enregistrement.", "error")
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from { opacity: 0; transform: translateY(12px); }
.toast-slide-leave-to   { opacity: 0; transform: translateY(12px); }
</style>