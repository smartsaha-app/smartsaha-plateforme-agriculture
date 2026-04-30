<template>
  <div class="max-w-2xl mx-auto p-4 sm:p-6 mt-16">
    <h2 class="text-xl sm:text-3xl font-bold mb-6 text-[#212121] flex items-center gap-3">
      {{ t("newcrop") }}
    </h2>

    <form @submit.prevent="submitCrop" class="space-y-5">
      <div class="flex flex-col">
        <label class="text-gray-700 text-sm font-medium mb-1">{{ t("cropname") }} *</label>
        <input
          v-model="form.name"
          type="text"
          placeholder="Enter crop name"
          required
          class="w-full border p-2 rounded focus:ring-[#212121]"
        />
      </div>

      <div class="flex flex-col">
        <label class="text-gray-700 text-sm font-medium mb-1">{{ t("variety") }} *</label>
        <select
          v-model="form.variety_id"
          required
          class="w-full border p-2 rounded focus:ring-[#212121]"
        >
          <option v-for="v in varieties" :key="v.id" :value="v.id">
            {{ v.name }}
          </option>
        </select>
      </div>

      <button
        type="submit"
        class="w-full bg-[#10b481] hover:bg-[#0da06a] transition-colors py-3 rounded text-white text-lg flex justify-center items-center gap-2"
      >
        {{ t("btnsavecrop") }}
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
              ? "Redirecting to your dashboard..."
              : "Please try again."
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
const router = useRouter();

const formState = useState("formData", () => ({ name: "", variety_id: null }));
const varietiesState = useState("varietiesData", () => [] as any[]);
const notificationState = useState("notificationData", () => ({
  visible: false,
  message: "",
  type: "success",
}));
const loadingState = useState("isLoading", () => false);

const form = ref(formState.value);
const varieties = ref(varietiesState.value);
const notification = ref(notificationState.value);
const isLoading = ref(loadingState.value);

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

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  try {
    if (!varietiesState.value.length) {
      const data: any = await apiFetch('/api/varieties/');
      varieties.value = data;
      varietiesState.value = varieties.value;
    } else {
      varieties.value = varietiesState.value;
    }
  } catch (err) {
    console.error("Failed to load varieties:", err);
  }
});

const submitCrop = async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  isLoading.value = true;
  loadingState.value = true;
  try {
    await apiFetch('/api/crops/', {
      method: "POST",
      body: form.value,
    });

    showNotification("Crop created successfully!", "success");
    showNotification("Crop created successfully!", "success");
    emit("next");
  } catch (err) {
    console.error(err);
    showNotification("Network error, please check your server", "error");
  } finally {
    isLoading.value = false;
    loadingState.value = false;
  }
};

watch(form, (val) => (formState.value = val), { deep: true });
watch(varieties, (val) => (varietiesState.value = val), { deep: true });
watch(notification, (val) => (notificationState.value = val), { deep: true });
watch(isLoading, (val) => (loadingState.value = val));
</script>

<style scoped>
input::placeholder,
select::placeholder {
  color: rgba(33, 33, 33, 0.5);
}
</style>
