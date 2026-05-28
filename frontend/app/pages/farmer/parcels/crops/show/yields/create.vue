<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Enregistrer une récolte">
      <template #subtitle>
        <i class="bx bx-plus-circle"></i>
        Saisissez les données de rendement pour cette récolte
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink
          :to="preselectedCropId ? `/farmer/parcels/crops/show/yields?parcel_crop=${preselectedCropId}` : '/farmer/parcels/crops/show/yields'"
          class="hover:text-[#10b481] transition-colors"
        >Rendements</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Nouvelle récolte</span>
      </template>
    </PageHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- ===== FORM ===== -->
      <div class="lg:col-span-2">
        <form @submit.prevent="submitYield" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 md:p-8 space-y-6">

          <!-- Plantation -->
          <div class="space-y-2">
            <label class="block text-[12px] font-semibold text-gray-600 uppercase tracking-wider">Plantation <span class="text-rose-400">*</span></label>
            <div class="relative">
              <i class="bx bx-leaf absolute left-4 top-1/2 -translate-y-1/2 text-lg pointer-events-none z-10"
                 :class="preselectedCropId ? 'text-emerald-400' : 'text-gray-300'"></i>

              <!-- Plantation verrouillée (venue de la page rendements avec parcel_crop) -->
              <template v-if="preselectedCropId">
                <div class="w-full pl-11 pr-4 py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-[14px] text-[#013b28] font-semibold flex items-center justify-between">
                  <span>{{ selectedParcelName || `Plantation #${preselectedCropId}` }}</span>
                  <span class="flex items-center gap-1 text-[10px] font-black text-emerald-600 uppercase tracking-widest flex-shrink-0">
                    <i class="bx bx-lock-alt text-sm"></i> Fixé
                  </span>
                </div>
              </template>

              <!-- Select normal -->
              <template v-else>
                <select
                  v-model="form.parcelCrop"
                  required
                  @change="onParcelCropChange"
                  class="w-full pl-11 pr-10 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] text-gray-700 appearance-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all"
                >
                  <option value="" disabled>Sélectionner une plantation…</option>
                  <option v-for="pc in parcelCrops" :key="pc.id" :value="pc.id">{{ pc.fullName }}</option>
                </select>
                <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
              </template>
            </div>
            <!-- Info surface max -->
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

          <!-- Surface récoltée -->
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
            <!-- Calcul rendement live -->
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
              placeholder="Conditions météo, qualité de la récolte, remarques particulières…"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] resize-none focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
            ></textarea>
          </div>

          <!-- Actions -->
          <div class="flex items-center justify-end gap-3 pt-2 border-t border-gray-50">
            <NuxtLink
              :to="preselectedCropId ? `/farmer/parcels/crops/show/yields?parcel_crop=${preselectedCropId}` : '/farmer/parcels/crops/show/yields'"
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
              Enregistrer la récolte
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
              <i class="bx bx-bar-chart-alt-2 text-[#10b481] text-xl"></i>
            </div>
            <h3 class="text-[15px] font-semibold mb-2">Analyse des rendements</h3>
            <p class="text-[13px] text-white/60 leading-relaxed">
              Indiquez la surface exacte récoltée pour calculer votre productivité au m² et optimiser vos prochaines semences.
            </p>
          </div>
        </div>

        <!-- Live preview -->
        <div v-if="form.parcelCrop || form.yield_amount || form.date" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 space-y-3">
          <p class="text-[12px] font-semibold text-gray-500 uppercase tracking-wider">Aperçu de l'enregistrement</p>
          <div class="space-y-2 text-[13px]">
            <div v-if="selectedParcelName" class="flex items-center gap-2 text-gray-600">
              <i class="bx bx-leaf text-[#10b481]"></i>
              <span>{{ selectedParcelName }}</span>
            </div>
            <div v-if="form.date" class="flex items-center gap-2 text-gray-600">
              <i class="bx bx-calendar text-gray-400"></i>
              <span>{{ formatDate(form.date) }}</span>
            </div>
            <div v-if="form.yield_amount" class="flex items-center gap-2 text-gray-600">
              <i class="bx bx-package text-gray-400"></i>
              <span class="font-semibold text-gray-900">{{ form.yield_amount }} kg</span>
            </div>
            <div v-if="form.yield_amount && form.area" class="flex items-center gap-2 text-emerald-600">
              <i class="bx bx-trending-up"></i>
              <span class="font-semibold">{{ (form.yield_amount / form.area).toFixed(2) }} kg/m²</span>
            </div>
          </div>
        </div>

        <!-- Tip -->
        <div class="bg-emerald-50 rounded-2xl border border-emerald-100 p-5 flex gap-3">
          <i class="bx bx-bulb text-emerald-500 text-xl flex-shrink-0 mt-0.5"></i>
          <p class="text-[13px] text-emerald-700 leading-relaxed italic">
            "La qualité du sol après une récolte abondante nécessite souvent un apport en nutriments organiques."
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
const parcelCrops = ref<any[]>([])
const maxAreaM2   = ref<number | null>(null)
const toast = ref({ show: false, message: "", type: "success" as "success" | "error" })

const form = ref({
  parcelCrop:   null as number | null,
  date:         "",
  yield_amount: null as number | null,
  area:         null as number | null,
  notes:        "",
})

// ===== COMPUTED =====
// ID de la plantation pré-sélectionnée depuis ?parcel_crop=<id>
const preselectedCropId = computed(() =>
  route.query.parcel_crop ? Number(route.query.parcel_crop) : null
)

const selectedParcelName = computed(() => {
  const id = preselectedCropId.value ?? form.value.parcelCrop
  const pc = parcelCrops.value.find((p: any) => p.id === id)
  return pc?.fullName ?? ""
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

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login")

  try {
    const data: any = await apiFetch("/api/parcel-crops/")
    const crops = data?.results ?? data ?? []
    parcelCrops.value = crops.map((pc: any) => ({
      ...pc,
      fullName: `${pc.parcel?.parcel_name ?? `Parcelle #${pc.parcel}`} — ${pc.crop?.name ?? `Culture #${pc.crop}`}`,
    }))

    // Pré-sélectionner la plantation si ?parcel_crop= est présent
    if (preselectedCropId.value) {
      form.value.parcelCrop = preselectedCropId.value
      onParcelCropChange()
    }
  } catch {
    showToast("Erreur lors du chargement des plantations.", "error")
  }
})

// ===== ACTIONS =====
function onParcelCropChange() {
  const selected = parcelCrops.value.find((pc: any) => pc.id == form.value.parcelCrop)
  maxAreaM2.value = selected?.area ? Math.round(Number(selected.area)) : null
  if (maxAreaM2.value) form.value.area = maxAreaM2.value
}

function checkArea() {
  if (maxAreaM2.value && form.value.area !== null && form.value.area > maxAreaM2.value) {
    form.value.area = maxAreaM2.value
  }
}

async function submitYield() {
  const { parcelCrop, date, yield_amount, area } = form.value
  if (!parcelCrop || !date || !yield_amount || !area) {
    showToast("Veuillez remplir tous les champs obligatoires.", "error")
    return
  }

  isLoading.value = true
  try {
    await apiFetch("/api/yield-records/", {
      method: "POST",
      body: {
        parcelCrop: Number(form.value.parcelCrop),
        date:         form.value.date,
        yield_amount: form.value.yield_amount,
        area:         form.value.area,
        notes:        form.value.notes || null,
      },
    })
    showToast("Récolte enregistrée avec succès !")
    const redirectPath = preselectedCropId.value
      ? `/farmer/parcels/crops/show/yields?parcel_crop=${preselectedCropId.value}`
      : "/farmer/parcels/crops/show/yields"
    setTimeout(() => router.push(redirectPath), 1500)
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