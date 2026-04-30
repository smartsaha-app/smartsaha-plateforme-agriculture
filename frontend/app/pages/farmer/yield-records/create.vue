<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="space-y-2">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1 font-bold">
          <i class="bx bx-home text-xs font-bold"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/yield-records" class="hover:text-[#10b481] transition-colors font-bold">Récoltes</NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481] font-bold">Nouvel Enregistrement</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Enregistrer une Récolte</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-2">
        <form @submit.prevent="createYieldRecord" class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12 space-y-10">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-bold">
            <!-- Parcel Crop Selection -->
            <div class="md:col-span-2 space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("parcelcrop") }} *</label>
              <div class="relative group">
                <i class="bx bx-link-alt absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <select 
                  v-model="form.parcelCrop" 
                  required
                  @change="onParcelCropChange"
                  class="w-full pl-14 pr-10 py-4 bg-gray-50 border border-gray-50 rounded-2xl appearance-none focus:bg-white focus:border-[#10b481]/30 outline-none transition-all font-bold"
                >
                  <option value="" disabled>-- Sélectionner une parcelle --</option>
                  <option v-for="pc in parcelCrops" :key="pc.id" :value="pc.id">
                    {{ pc.parcel_name ?? pc.parcel?.parcel_name ?? `ParcelCrop #${pc.id}` }} - {{ pc.crop?.name ?? `Crop #${pc.crop}` }}
                  </option>
                </select>
                <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none font-bold font-bold"></i>
              </div>
            </div>

            <!-- Date -->
            <div class="space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("thdate") }} *</label>
              <div class="relative group">
                <i class="bx bx-calendar absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <input 
                  v-model="form.date"
                  type="date" 
                  required
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all"
                >
              </div>
            </div>

            <!-- Yield Amount -->
            <div class="space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("thyield") }} *</label>
              <div class="relative group">
                <i class="bx bx-layer absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <input 
                  v-model.number="form.yield_amount"
                  type="number" 
                  step="0.01"
                  required
                  placeholder="Quantité récoltée"
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all placeholder:text-gray-300 font-bold"
                >
              </div>
            </div>

            <!-- Area -->
            <div class="space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("area") }} (m²) *</label>
              <div class="relative group">
                <i class="bx bx-area absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <input 
                  v-model.number="form.area"
                  type="number" 
                  :max="maxAreaM2 ?? undefined"
                  required
                  @input="checkArea"
                  placeholder="Surface récoltée"
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all placeholder:text-gray-300 font-bold"
                >
                <div v-if="maxAreaM2" class="absolute right-4 top-1/2 -translate-y-1/2 text-[8px] font-bold text-gray-300 uppercase tracking-widest pointer-events-none font-bold">
                  Max: {{ maxAreaM2 }} m²
                </div>
              </div>
            </div>

            <!-- Notes -->
            <div class="md:col-span-2 space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("notes") }}</label>
              <div class="relative group">
                <i class="bx bx-note absolute left-5 top-6 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <textarea 
                  v-model="form.notes"
                  placeholder="Observations sur la récolte..."
                  class="w-full pl-14 pr-6 py-5 bg-gray-50 border border-gray-50 rounded-[2rem] focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all min-h-[120px] resize-none placeholder:text-gray-300 font-bold"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col md:flex-row items-center justify-end gap-4 pt-6">
            <NuxtLink to="/farmer/yield-records" class="w-full md:w-auto px-8 py-4 text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-[#112830] transition-colors text-center font-bold">
              {{ t("cancel") }}
            </NuxtLink>
            <button 
              type="submit" 
              :disabled="isLoading"
              class="w-full md:w-auto px-10 py-4 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] hover:bg-[#10b481] transition-all shadow-xl shadow-[#112830]/10 disabled:opacity-50 flex items-center justify-center gap-3 font-bold"
            >
              <div v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              <span>{{ t("btnsaveyield") }}</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Helper Sidebar -->
      <div class="space-y-6">
        <div class="bg-[#112830] rounded-[3rem] p-10 text-white relative overflow-hidden group shadow-2xl font-bold">
          <div class="absolute -right-10 -top-10 w-40 h-40 bg-[#10b481] opacity-10 rounded-full filter blur-3xl group-hover:opacity-20 transition-opacity font-bold"></div>
          <div class="relative space-y-6 font-bold">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-3xl text-[#10b481]">
              <i class="bx bx-info-circle font-bold"></i>
            </div>
            <div class="space-y-2">
              <h3 class="text-xl font-black tracking-tight">Analyse des Rendements</h3>
              <p class="text-xs text-gray-400 leading-relaxed font-bold">
                Assurez-vous d'indiquer la surface exacte récoltée. Ces données sont cruciales pour calculer votre productivité par m² et optimiser vos prochaines semences.
              </p>
            </div>
          </div>
        </div>

        <div class="bg-emerald-50 rounded-[2rem] p-8 border border-emerald-100/50 flex flex-col items-center text-center gap-4">
          <div class="w-14 h-14 rounded-full bg-white flex items-center justify-center text-2xl text-[#10b481] shadow-sm font-bold">
            <i class="bx bx-bulb animate-pulse"></i>
          </div>
          <p class="text-xs font-bold text-[#10b481] tracking-tight uppercase tracking-[0.1em]">Astuce Agricole</p>
          <p class="text-xs text-gray-500 italic font-bold leading-relaxed px-4">
             "La qualité du sol après une récolte abondante nécessite souvent un apport en nutriments organiques."
          </p>
        </div>
      </div>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100 font-bold', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500 font-bold']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight font-bold">{{ notification.message }}</p>
            <span class="text-[10px] font-medium text-gray-400 uppercase tracking-widest">Confirmation</span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import * as turf from "@turf/turf";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

// ===== STATE =====
const parcelCrops = ref<any[]>([]);
const isLoading = ref(false);
const maxAreaM2 = ref<number | null>(null);
const notification = ref({ visible: false, message: "", type: "success" as "success" | "error" });

const form = ref({
  date: "",
  yield_amount: null as number | null,
  area: null as number | null,
  notes: "",
  parcelCrop: "" as number | string,
});

// ===== HELPERS =====
const showNotification = (message: string, type: "success" | "error" = "success") => {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
};

const calculateParcelAreaM2 = (points: { lng: number; lat: number }[]): number => {
  if (!points || points.length < 3) return 0;
  const coords = points.map((p) => [p.lng, p.lat]);
  coords.push([points[0].lng, points[0].lat]);
  const polygon = turf.polygon([coords]);
  return turf.area(polygon);
};

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  try {
    const data: any = await apiFetch("/api/parcel-crops/");
    parcelCrops.value = data;
  } catch (err) {
    showNotification("Erreur de chargement des données", "error");
  }
});

// ===== ACTIONS =====
const onParcelCropChange = () => {
  const selected = parcelCrops.value.find((pc) => pc.id === form.value.parcelCrop);
  if (selected?.parcel?.points) {
    maxAreaM2.value = Math.round(calculateParcelAreaM2(selected.parcel.points));
  } else if (selected?.area) {
    maxAreaM2.value = selected.area;
  } else {
    maxAreaM2.value = null;
  }
  form.value.area = maxAreaM2.value;
};

const checkArea = () => {
  if (maxAreaM2.value && form.value.area !== null && form.value.area > maxAreaM2.value) {
    form.value.area = maxAreaM2.value;
  }
};

const createYieldRecord = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  isLoading.value = true;
  try {
    const payload = {
      parcelCrop: Number(form.value.parcelCrop),
      date: form.value.date,
      yield_amount: form.value.yield_amount,
      area: form.value.area,
      notes: form.value.notes || null,
    };

    await apiFetch("/api/yield-records/", { method: "POST", body: payload });
    showNotification("Récolte enregistrée avec succès !", "success");
    setTimeout(() => router.push({ path: "/farmer/yield-records", query: { refresh: "1" } }), 2000);
  } catch (err) {
    showNotification("Erreur lors de l'enregistrement", "error");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.pop-notification-enter-active, .pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from, .pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>