<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="space-y-2">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
          <i class="bx bx-home text-xs"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/parcel-crops" class="hover:text-[#10b481] transition-colors">Parcel crops</NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481]">Modifier parcel crops</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">{{ t("editparcelcrop") }}</h1>
    </div>

    <!-- ===== FORM CARD ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden p-8 md:p-12 relative">
      <div v-if="isLoadingData" class="absolute inset-0 bg-white/80 backdrop-blur-sm z-10 flex items-center justify-center">
        <div class="w-12 h-12 border-4 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
      </div>

      <form @submit.prevent="submitParcelCrop" class="space-y-8 max-w-4xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- PARCEL -->
          <div class="space-y-2 group">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("parcel") }} *</label>
            <div class="relative">
              <i class="bx bx-map absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <select
                v-model="form.parcel"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold appearance-none"
              >
                <option v-for="p in parcels" :key="p.uuid" :value="p.uuid">{{ p.parcel_name }}</option>
              </select>
            </div>
          </div>

          <!-- CROP -->
          <div class="space-y-2 group">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("crop") }} *</label>
            <div class="relative">
              <i class="bx bx-leaf absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <select
                v-model="form.crop_id"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold appearance-none"
              >
                <option v-for="c in crops" :key="c.id" :value="c.id">{{ c.name }} ({{ c.variety?.name }})</option>
              </select>
            </div>
          </div>

          <!-- PLANTING DATE -->
          <div class="space-y-2 group">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("plantingdate") }} *</label>
            <div class="relative">
              <i class="bx bx-calendar-plus absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model="form.planting_date"
                type="date"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold"
              />
            </div>
          </div>

          <!-- HARVEST DATE -->
          <div class="space-y-2 group">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("harvestdate") }}</label>
            <div class="relative">
              <i class="bx bx-calendar-check absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model="form.harvest_date"
                type="date"
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold"
              />
            </div>
          </div>

          <!-- AREA -->
          <div class="space-y-2 group">
            <div class="flex items-center justify-between px-1">
              <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">{{ t("area") }} (m²) *</label>
              <span v-if="calculatedArea" class="text-[10px] font-black text-[#10b481]">MAX: {{ formatM2(calculatedArea) }}</span>
            </div>
            <div class="relative">
              <i class="bx bx-area absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model.number="form.area"
                type="number"
                step="1"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold"
              />
            </div>
          </div>

          <!-- STATUS -->
          <div class="space-y-2 group">
            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400 px-1">{{ t("status") }} *</label>
            <div class="relative">
              <i class="bx bx-stats absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <select
                v-model="form.status_id"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-bold appearance-none"
              >
                <option v-for="s in statuses" :key="s.id" :value="s.id">{{ t(cropStatusKeyMap[s.name]) }}</option>
              </select>
            </div>
          </div>
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-6 bg-[#112830] text-white rounded-[2rem] font-black uppercase tracking-widest text-xs hover:bg-[#10b481] disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-xl shadow-[#112830]/10 hover:shadow-[#10b481]/20 flex items-center justify-center gap-3"
        >
          <i v-if="isLoading" class="bx bx-loader-alt animate-spin text-xl"></i>
          <span v-else>{{ t("btnsaveparcelcrop") }}</span>
        </button>
      </form>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">Confirmation du système</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import * as turf from "@turf/turf";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const cropStatusKeyMap: Record<string, string> = {
  Planned: "cropStatusPlanned",
  Planted: "cropStatusPlanted",
  Germinated: "cropStatusGerminated",
  Growing: "cropStatusGrowing",
  Flowering: "cropStatusFlowering",
  Fruiting: "cropStatusFruiting",
  Mature: "cropStatusMature",
  Harvested: "cropStatusHarvested",
  "Post-Harvest": "cropStatusPostHarvest",
  Failed: "cropStatusFailed",
};

const isLoading = ref(false);
const isLoadingData = ref(true);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const notification = ref({ visible: false, message: "", type: "success" });

const form = ref({
  parcel: "",
  crop_id: null,
  planting_date: "",
  harvest_date: "",
  area: null,
  status_id: null,
});

const parcels = ref<any[]>([]);
const crops = ref<any[]>([]);
const statuses = ref<any[]>([]);
const calculatedArea = ref<number>(0);

function showNotification(message: string, type: "success" | "error" = "success") {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
}

function calculateParcelArea(points: { lat: number; lng: number }[]) {
  if (!points || points.length < 3) return 0;
  const coords = points.map((p) => [p.lng, p.lat]);
  coords.push([points[0].lng, points[0].lat]);
  const polygon = turf.polygon([coords]);
  const areaM2 = turf.area(polygon);
  return areaM2 / 10000;
}

watch(
  () => form.value.parcel,
  (parcelId) => {
    const selectedParcel = parcels.value.find((p) => p.uuid === parcelId);
    if (selectedParcel?.points?.length) {
      calculatedArea.value = Number(calculateParcelArea(selectedParcel.points).toFixed(2));
    } else {
      calculatedArea.value = 0;
    }
  }
);

onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  try {
    const [pData, cData, sData, pcData] = await Promise.all([
      apiFetch('/api/parcels/'),
      apiFetch('/api/crops/'),
      apiFetch('/api/status-crops/'),
      apiFetch(`/api/parcel-crops/${route.params.id}/`),
    ]);

    parcels.value = pData as any[];
    crops.value = cData as any[];
    statuses.value = sData as any[];
    const data = pcData as any;
    form.value = {
      parcel: data.parcel,
      crop_id: data.crop_id,
      planting_date: data.planting_date,
      harvest_date: data.harvest_date || "",
      area: data.area,
      status_id: data.status_id,
    };
  } catch (err) {
    showNotification("Erreur de chargement", "error");
  } finally {
    isLoadingData.value = false;
  }
});

const submitParcelCrop = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  isLoading.value = true;
  try {
    await apiFetch(`/api/parcel-crops/${route.params.id}/`, { method: "PUT", body: form.value });
    showNotification("Mise à jour réussie !", "success");
    setTimeout(() => router.push("/farmer/parcel-crops"), 2000);
  } catch (err) {
    showNotification("Échec de la mise à jour", "error");
  } finally {
    isLoading.value = false;
  }
};

const formatM2 = (areaInHa: number) => `${(areaInHa * 10000).toLocaleString()} m²`;
</script>

<style scoped>
.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from,
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23D1D5DB'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-position: right 1.25rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
}
</style>
