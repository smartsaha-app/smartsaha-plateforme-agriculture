<template>
  <div class="max-w-3xl mx-auto p-4 sm:p-6 mb-10 sm:mb-1">
    <h2
      class="text-xl sm:text-3xl font-bold mb-6 text-[#212121] flex items-center gap-2"
    >
      {{ t("titlenewtask") }}
    </h2>

    <form @submit.prevent="submitTask" class="space-y-4">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("taskname") }} *</label
          >
          <input
            v-model="form.name"
            type="text"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          />
        </div>

        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1"
            >{{ t("due") }} *</label
          >
          <input
            v-model="form.due_date"
            type="date"
            required
            class="w-full border p-2 rounded focus:ring-[#212121]"
          />
        </div>
      </div>

      <div class="flex flex-col">
        <label class="text-gray-700 text-sm font-medium mb-1"
          >{{ t("desc") }} *</label
        >
        <textarea
          v-model="form.description"
          required
          class="w-full border p-2 rounded focus:ring-[#212121]"
        ></textarea>
      </div>

      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1">{{
            t("parcelcrop")
          }}</label>
          <select
            v-model="form.parcelCrop"
            class="w-full border p-2 rounded focus:ring-[#212121]"
          >
            <option v-for="crop in parcelCrops" :key="crop.id" :value="crop.id">
              {{ crop.fullName }}
            </option>
          </select>
        </div>

        <div class="flex-1 flex flex-col">
          <label class="text-gray-700 text-sm font-medium mb-1">{{
            t("priority")
          }}</label>
          <select
            v-model="form.priority"
            class="w-full border p-2 rounded focus:ring-[#212121]"
          >
            <option v-for="p in priorities" :key="p.id" :value="p.id">
              {{ t(priorityKeyMap[p.name]) }}
            </option>
          </select>
        </div>
      </div>

      <div class="flex flex-col">
        <label class="text-gray-700 text-sm font-medium mb-1">{{
          t("status")
        }}</label>
        <select
          v-model="form.status"
          class="w-full border p-2 rounded focus:ring-[#212121]"
        >
          <option v-for="s in statuses" :key="s.id" :value="s.id">
            {{ t(statusKeyMap[s.name]) }}
          </option>
        </select>
      </div>

      <button
        type="submit"
        class="w-full bg-[#10b481] text-white py-2 rounded hover:opacity-90 transition"
      >
        {{ t("btnaddtask") }}
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
definePageMeta({
  layout: "dashboard",
});

import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
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

const priorityKeyMap = {
  Low: "priorityLow",
  Medium: "priorityMedium",
  High: "priorityHigh",
};

const statusKeyMap = {
  Pending: "statusPending",
  "In Progress": "statusInProgress",
  Done: "statusDone",
  Cancelled: "statusCancelled",
};

const router = useRouter();

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

const form = ref({
  name: "",
  description: "",
  due_date: "",
  parcelCrop: null,
  priority: null,
  status: null,
});

const priorities = ref<any[]>([]);
const statuses = ref<any[]>([]);
const parcelCrops = ref<any[]>([]);

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  try {
    const priData: any = await apiFetch('/api/task-priority/');
    priorities.value = priData;

    const staData: any = await apiFetch('/api/task-status/');
    statuses.value = staData;

    const cropsData: any = await apiFetch('/api/parcel-crops/');

    const enrichedCrops = await Promise.all(
      cropsData.map(async (pc: any) => {
        try {
          const parcelData: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
          return {
            ...pc,
            fullName: `${parcelData.parcel_name} - ${pc.crop.name}`,
          };
        } catch (err) {
          console.error("Erreur fetch parcel:", err);
          return { ...pc, fullName: `${pc.crop.name}` };
        }
      })
    );

    parcelCrops.value = enrichedCrops;
  } catch (err) {
    console.error("Erreur lors du chargement des options:", err);
  }
});

const submitTask = async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  isLoading.value = true;
  try {
    await apiFetch('/api/tasks/', {
      method: "POST",
      body: form.value,
    });

    showNotification(t("success_save"), "success");
    router.push(`/dashboard/s/${authStore.user?.uuid}`);
  } catch (err) {
    console.error("Erreur création tâche:", err);
    showNotification(t("error_network"), "error");
  } finally {
    isLoading.value = false;
  }
};
</script>
