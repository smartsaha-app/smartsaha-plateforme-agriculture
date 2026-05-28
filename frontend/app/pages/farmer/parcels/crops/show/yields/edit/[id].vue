<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Modifier l'enregistrement">
      <template #subtitle>
        <i class="bx bx-edit"></i>
        Mettez à jour les données de cette récolte
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
          <NuxtLink :to="`/farmer/parcels/crops/show/yields?parcel_crop=${parcelCropId}`" class="hover:text-[#10b481] transition-colors">Rendements</NuxtLink>
        </template>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Modifier</span>
      </template>
    </PageHeader>

    <!-- Loading -->
    <div v-if="initialLoading" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <i class="bx bx-loader-alt animate-spin text-3xl"></i>
      <p class="text-[13px]">Chargement de l'enregistrement…</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- ===== FORM ===== -->
      <div class="lg:col-span-2">
        <form @submit.prevent="submitYield" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 md:p-8 space-y-6">

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
            <p v-if="maxAreaM2" class="text-[12px] text-[#10b481] flex items-center gap-1.5 px-1">
              <i class="bx bx-info-circle"></i>
              Surface de la parcelle : {{ maxAreaM2.toLocaleString("fr-FR") }} m²
            </p>
          </div>

          <!-- Date + Quantité -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Date de récolte <span class="text-rose-400">*</span></label>
              <div class="relative">
                <i class="bx bx-calendar absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
                <input
                  v-model="form.date"
                  type="date"
                  required
                  class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all"
                >
              </div>
            </div>

            <div class="space-y-2">
              <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Quantité récoltée (kg) <span class="text-rose-400">*</span></label>
              <div class="relative">
                <i class="bx bx-package absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
                <input
                  v-model.number="form.yield_amount"
                  type="number"
                  step="0.01"
                  min="0.01"
                  required
                  placeholder="Ex : 250.5"
                  class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
                >
              </div>
            </div>
          </div>

          <!-- Surface -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">
              Surface récoltée (m²) <span class="text-rose-400">*</span>
              <span v-if="maxAreaM2" class="ml-2 text-[10px] text-gray-400 normal-case font-normal">max : {{ maxAreaM2.toLocaleString("fr-FR") }} m²</span>
            </label>
            <div class="relative">
              <i class="bx bx-area absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
              <input
                v-model.number="form.area"
                type="number"
                step="1"
                min="1"
                :max="maxAreaM2 ?? undefined"
                required
                @input="checkArea"
                placeholder="Ex : 500"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
              >
            </div>
            <div v-if="form.yield_amount && form.area" class="flex items-center gap-2 px-1">
              <i class="bx bx-trending-up text-[#10b481] text-sm"></i>
              <p class="text-[12px] text-[#10b481] font-semibold">
                Rendement calculé : {{ (form.yield_amount / form.area).toFixed(2) }} kg/m²
              </p>
            </div>
          </div>

          <!-- Notes -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Notes / Observations</label>
            <textarea
              v-model="form.notes"
              rows="3"
              placeholder="Conditions météo, qualité de la récolte, remarques…"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] resize-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
            ></textarea>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-3 pt-2 border-t border-gray-50">
            <NuxtLink
              :to="parcelCropId ? `/farmer/parcels/crops/show/yields?parcel_crop=${parcelCropId}` : '/farmer/parcels/crops/show/yields'"
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
        <!-- Récap actuel -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 space-y-3">
          <p class="text-[12px] font-semibold text-gray-500 uppercase tracking-wider">Données actuelles</p>
          <div class="space-y-2.5">
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Date</span>
              <span class="font-semibold text-gray-700">{{ form.date ? formatDate(form.date) : '—' }}</span>
            </div>
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Quantité</span>
              <span class="font-bold text-gray-900">{{ form.yield_amount ? `${form.yield_amount} kg` : '—' }}</span>
            </div>
            <div class="flex items-center justify-between text-[13px]">
              <span class="text-gray-400">Surface</span>
              <span class="font-semibold text-gray-700">{{ form.area ? `${form.area} m²` : '—' }}</span>
            </div>
            <div v-if="form.yield_amount && form.area" class="flex items-center justify-between text-[13px] pt-1 border-t border-gray-50">
              <span class="text-gray-400">Rendement</span>
              <span class="font-bold text-[#10b481]">{{ (form.yield_amount / form.area).toFixed(2) }} kg/m²</span>
            </div>
          </div>
        </div>

        <!-- Danger zone -->
        <div class="bg-rose-50 rounded-2xl border border-rose-100 p-5">
          <p class="text-[12px] font-semibold text-rose-500 uppercase tracking-wider mb-3">Zone dangereuse</p>
          <p class="text-[13px] text-rose-700/70 leading-relaxed mb-4">
            La suppression de cet enregistrement est définitive et irréversible.
          </p>
          <button
            type="button"
            @click="openDeleteModal"
            class="w-full py-2.5 bg-white border border-rose-200 text-rose-500 rounded-xl text-[13px] font-semibold hover:bg-rose-500 hover:text-white transition-all"
          >
            <i class="bx bx-trash mr-1.5"></i> Supprimer cette récolte
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
                <h3 class="text-[15px] font-semibold text-gray-900 mb-1">Supprimer l'enregistrement</h3>
                <p class="text-[13px] text-gray-500 leading-relaxed">
                  Récolte du <span class="font-semibold text-gray-700">{{ formatDate(form.date) }}</span> —
                  <span class="font-semibold text-gray-700">{{ form.yield_amount }} kg</span>. Cette action est irréversible.
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

import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"

const route  = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

// ===== COMPUTED =====
const parcelCropId = computed(() =>
  route.query.parcel_crop ? Number(route.query.parcel_crop) : null
)
const parcelCropName = computed(() => {
  const id = parcelCropId.value ?? form.value.parcelCrop
  const pc = parcelCrops.value.find((p: any) => p.id === id)
  return pc?.fullName ?? ""
})

// ===== STATE =====
const initialLoading = ref(true)
const isLoading      = ref(false)
const parcelCrops    = ref<any[]>([])
const maxAreaM2      = ref<number | null>(null)
const deleteModal    = ref({ show: false, loading: false })
const toast          = ref({ show: false, message: "", type: "success" as "success" | "error" })

const form = ref({
  parcelCrop:   "" as number | string,
  date:         "",
  yield_amount: null as number | null,
  area:         null as number | null,
  notes:        "",
})

// ===== HELPERS =====
function formatDate(d: string) {
  if (!d) return "—"
  return new Date(d).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}
function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3500)
}
function onParcelCropChange() {
  const selected = parcelCrops.value.find((pc: any) => pc.id == form.value.parcelCrop)
  maxAreaM2.value = selected?.area ? Math.round(Number(selected.area)) : null
}
function checkArea() {
  if (maxAreaM2.value && form.value.area !== null && form.value.area > maxAreaM2.value) {
    form.value.area = maxAreaM2.value
  }
}

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  try {
    const [record, cropData]: [any, any] = await Promise.all([
      apiFetch(`/api/yield-records/${route.params.id}/`),
      apiFetch("/api/parcel-crops/"),
    ])

    const crops = cropData?.results ?? cropData ?? []
    parcelCrops.value = crops.map((pc: any) => ({
      ...pc,
      fullName: `${pc.parcel?.parcel_name ?? `Parcelle #${pc.parcel}`} — ${pc.crop?.name ?? `Culture #${pc.crop}`}`,
    }))

    // Pré-remplir le formulaire
    form.value = {
      parcelCrop:   record.parcelCrop ?? "",
      date:         record.date       ?? "",
      yield_amount: record.yield_amount ?? null,
      area:         record.area         ?? null,
      notes:        record.notes        ?? "",
    }

    // Calculer la surface max pour la plantation sélectionnée
    onParcelCropChange()
  } catch {
    showToast("Erreur lors du chargement de l'enregistrement.", "error")
  } finally {
    initialLoading.value = false
  }
})

// ===== SUBMIT =====
async function submitYield() {
  const { parcelCrop, date, yield_amount, area } = form.value
  if (!parcelCrop || !date || !yield_amount || !area) {
    showToast("Veuillez remplir tous les champs obligatoires.", "error")
    return
  }

  isLoading.value = true
  try {
    await apiFetch(`/api/yield-records/${route.params.id}/`, {
      method: "PATCH",
      body: {
        parcelCrop:   Number(form.value.parcelCrop),
        date:         form.value.date,
        yield_amount: form.value.yield_amount,
        area:         form.value.area,
        notes:        form.value.notes || null,
      },
    })
    showToast("Récolte mise à jour avec succès !")
    const backPath = parcelCropId.value
      ? `/farmer/parcels/crops/show/yields?parcel_crop=${parcelCropId.value}`
      : "/farmer/parcels/crops/show/yields"
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
    await apiFetch(`/api/yield-records/${route.params.id}/`, { method: "DELETE" })
    showToast("Enregistrement supprimé.")
    const backPath = parcelCropId.value
      ? `/farmer/parcels/crops/show/yields?parcel_crop=${parcelCropId.value}`
      : "/farmer/parcels/crops/show/yields"
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