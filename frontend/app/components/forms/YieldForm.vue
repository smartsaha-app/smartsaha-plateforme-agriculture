<template>
  <div class="max-w-3xl mx-auto mt-1 sm:mt-16 mb-10 sm:mb-1">
    <h2
      class="text-xl sm:text-3xl font-bold mb-6 text-[#212121] flex items-center gap-3"
    >
      {{ t("newyield") }}
    </h2>

    <form @submit.prevent="createYieldRecord" class="space-y-4">
      <div>
        <label class="text-gray-700 text-sm font-medium mb-1">{{
          t("parcelcrop")
        }}</label>
        <select
          v-model="form.parcelCrop"
          @change="onParcelCropChange"
          class="border rounded px-3 py-2 w-full focus:ring-2 focus:ring-[#10b481]"
          required
        >
          <option v-for="crop in parcelCrops" :key="crop.id" :value="crop.id">
            {{ crop.parcel.parcel_name }} - {{ crop.crop.name }}
          </option>
        </select>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="text-gray-700 text-sm font-medium mb-1">{{
            t("thdate")
          }}</label>
          <input
            v-model="form.date"
            type="date"
            class="border rounded px-3 py-2 w-full focus:ring-2 focus:ring-[#10b481]"
            required
          />
        </div>

        <div>
          <label class="text-gray-700 text-sm font-medium mb-1">{{
            t("thyield")
          }}</label>
          <input
            v-model.number="form.yield_amount"
            type="number"
            class="border rounded px-3 py-2 w-full focus:ring-2 focus:ring-[#10b481]"
            required
          />
        </div>

        <div>
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("area") }} (m²)</label
          >
          <input
            v-model.number="form.area"
            type="number"
            :max="areaInM2(maxArea)"
            step="1"
            @input="checkArea"
            class="border rounded px-3 py-2 w-full focus:ring-2 focus:ring-[#10b481]"
            required
          />
        </div>
      </div>

      <div>
        <label class="text-gray-700 text-sm font-medium mb-1">{{
          t("notes")
        }}</label>
        <textarea
          v-model="form.notes"
          class="border rounded px-3 py-2 w-full focus:ring-2 focus:ring-[#10b481]"
        ></textarea>
      </div>

      <div class="text-right">
        <button
          type="submit"
          class="w-full bg-[#10b481] text-white px-6 py-2 rounded font-bold transition transform"
        >
          {{ t("btnsaveyield") }}
        </button>
      </div>
    </form>
  </div>
  <div
    v-if="isLoading"
    class="absolute inset-0 bg-black/50 flex items-center justify-center"
  >
    <div
      class="w-12 h-12 border-4 border-t-[#10b481] border-white rounded-full animate-spin"
    ></div>
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

import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import * as turf from "@turf/turf";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

import { defineEmits } from "vue";
const emit = defineEmits(["next"]);

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const authStore = useAuthStore();
const { apiFetch } = useApi();

const router = useRouter();
const parcelCrops = ref([]);
const maxArea = ref(null);

const isLoading = ref(false);

const notification = ref({
  visible: false,
  message: "",
  type: "success",
});

const showNotification = (message, type = "success", duration = 3000) => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => {
    notification.value.visible = false;
  }, duration);
};

const form = ref({
  date: "",
  yield_amount: null,
  area: null,
  notes: "",
  parcelCrop: null,
});

let token = null;

onMounted(async () => {
  if (!process.client) return;

  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  await loadParcelCrops();
});

async function loadParcelCrops() {
  try {
    const data: any = await apiFetch('/api/parcel-crops/');

    for (const pc of data) {
      if (pc.parcel) {
        const pData: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
        pc.parcel = pData;
      }
    }

    parcelCrops.value = data;
  } catch (err) {
    console.error(err);
  }
}

function calculateParcelArea(points) {
  if (!points || points.length < 3) return 0;
  const coords = points.map((p) => [p.lng, p.lat]);
  coords.push([points[0].lng, points[0].lat]);
  const polygon = turf.polygon([coords]);
  const areaM2 = turf.area(polygon);
  return areaM2 / 10000; // hectares
}

function onParcelCropChange() {
  const selected = parcelCrops.value.find(
    (pc) => pc.id === form.value.parcelCrop
  );
  if (selected?.parcel?.points) {
    const area = calculateParcelArea(selected.parcel.points);
    maxArea.value = area.toFixed(2);
    form.value.area = areaInM2(maxArea.value);
  } else {
    maxArea.value = null;
    form.value.area = null;
  }
}

function checkArea() {
  if (areaInM2(maxArea.value) && form.value.area > areaInM2(maxArea.value)) {
    form.value.area = areaInM2(maxArea.value);
  }
}

async function createYieldRecord() {
  if (!authStore.isAuthenticated) return;
  isLoading.value = true;
  try {
    await apiFetch('/api/yield-records/', {
      method: "POST",
      body: form.value,
    });
    showNotification(t("success_save"), "success");
    emit("next");
  } catch (err) {
    console.error(err);
    showNotification(t("error_network"), "error");
  } finally {
    isLoading.value = false;
  }
}

const formatM2 = (areaInHa) => {
  if (!areaInHa) return "0 m²";
  return `${(areaInHa * 10000).toLocaleString()} m²`;
};

const areaInM2 = (areaInHa) => {
  if (!areaInHa) return 0;
  return areaInHa * 10000;
};
</script>
