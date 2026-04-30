<template>
  <div class="max-w-3xl mx-auto mt-1 sm:mt-16 mb-10 sm:mb-1">
    <div
      class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4"
    >
      <h2
        class="text-xl sm:text-3xl font-bold text-[#212121] flex items-center gap-2"
      >
        {{ t("newparcelcrop") }}
      </h2>
    </div>

    <form @submit.prevent="submitParcelCrop" class="space-y-5">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("parcel") }} *</label
          >
          <select
            v-model="form.parcel"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          >
            <option v-for="p in parcels" :key="p.uuid" :value="p.uuid">
              {{ p.parcel_name }}
            </option>
          </select>
        </div>

        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("crop") }} *</label
          >
          <select
            v-model="form.crop_id"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          >
            <option v-for="c in crops" :key="c.id" :value="c.id">
              {{ c.name }} ({{ c.variety?.name }})
            </option>
          </select>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("plantingdate") }} *</label
          >
          <input
            v-model="form.planting_date"
            type="date"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          />
        </div>

        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1">{{
            t("harvestdate")
          }}</label>
          <input
            v-model="form.harvest_date"
            type="date"
            class="w-full border p-2 rounded focus:ring-[#212121]"
          />
        </div>
      </div>

      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("area") }} (m²) *</label
          >
          <input
            v-model.number="form.area"
            type="number"
            step="1"
            :max="areaInM2(calculatedArea)"
            required
            placeholder="Enter area in m²"
            class="w-full border p-2 rounded focus:ring-[#212121]"
            @input="onAreaInput"
          />
          <!-- <small class="text-gray-500 text-sm">
            Max: {{ formatM2(calculatedArea) }}
          </small> -->
        </div>

        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("status") }} *</label
          >
          <select
            v-model="form.status_id"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          >
            <option v-for="s in statuses" :key="s.id" :value="s.id">
              {{ t(cropStatusKeyMap[s.name]) }}
            </option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        class="w-full bg-[#10b481] hover:bg-[#0da06a] transition-colors py-3 rounded text-white text-lg flex justify-center items-center gap-2"
      >
        {{ t("btnsaveparcelcrop") }}
      </button>
    </form>
  </div>

  <transition name="fade">
    <div
      v-if="notification.visible"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black/20 backdrop-blur-sm"
    >
      <div
        :class="[
          'bg-white rounded-2xl shadow-2xl px-8 py-6 flex flex-col items-center gap-4 w-[340px] text-center transition-all duration-300',
          notification.type === 'success'
            ? 'border-t-4 border-[#10b481]'
            : 'border-t-4 border-red-500',
        ]"
      >
        <div
          v-if="notification.type === 'success'"
          class="w-16 h-16 rounded-full bg-[#10b481] flex items-center justify-center"
        >
          <i class="bx bx-check text-4xl font-extrabold text-white"></i>
        </div>
        <div
          v-else
          class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center"
        >
          <i class="bx bx-x text-4xl font-extrabold text-white"></i>
        </div>

        <p
          :class="[
            'text-lg font-semibold',
            notification.type === 'success' ? 'text-[#10b481]' : 'text-red-500',
          ]"
        >
          {{ notification.message }}
        </p>

        <p class="text-gray-500 text-sm">
          {{
            notification.type === "success"
              ? t("redirecting")
              : t("try_again")
          }}
        </p>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import * as turf from "@turf/turf";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

import { defineEmits } from "vue";
const emit = defineEmits<{
  (e: "next"): void;
}>();

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const authStore = useAuthStore();
const { apiFetch } = useApi();

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

const notification = ref({
  visible: false,
  message: "",
  type: "success",
});

const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => (notification.value.visible = false), duration);
};

const router = useRouter();
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

function calculateParcelArea(points: { lat: number; lng: number }[]) {
  if (points.length < 3) return 0;
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
      const area = calculateParcelArea(selectedParcel.points);
      calculatedArea.value = Number(area.toFixed(2));
      form.value.area = areaInM2(calculatedArea.value);
    } else {
      calculatedArea.value = 0;
      form.value.area = null;
    }
  }
);

const onAreaInput = () => {
  if (form.value.area > areaInM2(calculatedArea.value)) {
    form.value.area = areaInM2(calculatedArea.value);
  } else if (form.value.area < 0) {
    form.value.area = 0;
  }
};

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  try {
    const dataParcels: any = await apiFetch('/api/parcels/');
    parcels.value = dataParcels;

    const dataCrops: any = await apiFetch('/api/crops/');
    crops.value = dataCrops;

    const dataStatus: any = await apiFetch('/api/status-crops/');
    statuses.value = dataStatus;
  } catch (err) {
    console.error(err);
    showNotification(t("error_load_data"), "error");
  }
});

const submitParcelCrop = async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  isLoading.value = true;
  try {
    await apiFetch('/api/parcel-crops/', {
      method: "POST",
      body: form.value,
    });
    showNotification(t("success_save"), "success");
    emit("next");
  } catch (err) {
    console.error(err);
    showNotification(t("error_save"), "error");
  } finally {
    isLoading.value = false;
  }
};

const formatM2 = (areaInHa) => {
  if (!areaInHa) return "0 m²";
  return `${(areaInHa * 10000).toLocaleString()} m²`;
};

const areaInM2 = (areaInHa: number) => {
  if (!areaInHa) return 0;
  return areaInHa * 10000;
};
</script>

<style scoped>
input::placeholder,
select::placeholder {
  color: rgba(255, 255, 255, 0.6);
}
</style>
