<template>
  <div class="px-6 md:px-20 mt-12">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-xl sm:text-3xl font-bold mb-6 text-[#112830] flex items-center gap-2">
        {{ t("editProfile") }}
      </h1>

      <form
        @submit.prevent="updateProfile"
        class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-8 rounded-2xl shadow-sm border border-gray-100"
      >
        <div class="col-span-2">
          <label class="text-gray-700 text-xs font-bold uppercase tracking-wider mb-2 block">{{ t("username") }}</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-[#10b481]/5 focus:border-[#10b481] outline-none transition-all"
            required
          />
        </div>

        <div>
          <label class="text-gray-700 text-xs font-bold uppercase tracking-wider mb-2 block">{{ t("firstName") }}</label>
          <input
            v-model="form.first_name"
            type="text"
            class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-[#10b481]/5 focus:border-[#10b481] outline-none transition-all"
          />
        </div>

        <div>
          <label class="text-gray-700 text-xs font-bold uppercase tracking-wider mb-2 block">{{ t("lastName") }}</label>
          <input
            v-model="form.last_name"
            type="text"
            class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-[#10b481]/5 focus:border-[#10b481] outline-none transition-all"
          />
        </div>

        <div class="col-span-2">
          <label class="text-gray-700 text-xs font-bold uppercase tracking-wider mb-2 block">{{ t("email") }}</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-[#10b481]/5 focus:border-[#10b481] outline-none transition-all"
            required
          />
        </div>

        <div class="col-span-2 flex justify-between mt-6 pt-6 border-t border-gray-50">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-8 py-3 bg-[#112830] text-white font-bold rounded-xl hover:bg-black transition-all flex items-center gap-2"
          >
            <i v-if="isSubmitting" class="bx bx-loader-alt animate-spin"></i>
            {{ t("saveChanges") }}
          </button>

          <button
            type="button"
            @click="goBack"
            class="px-8 py-3 bg-gray-100 text-gray-700 font-bold rounded-xl hover:bg-gray-200 transition-all"
          >
            {{ t("back") }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const props = defineProps<{
  role: string;
}>();

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const isSubmitting = ref(false);
const form = ref({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  
  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    form.value.username = data.username;
    form.value.email = data.email;
    form.value.first_name = data.first_name;
    form.value.last_name = data.last_name;
  } catch (err) {
    console.error(err);
  }
});

const updateProfile = async () => {
  isSubmitting.value = true;
  try {
    await apiFetch(`/api/users/${authStore.uuid}/`, {
      method: "PATCH",
      body: form.value,
    });
    router.push(`/${props.role}/profil`);
  } catch (err) {
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
};

const goBack = () => {
  router.push(`/${props.role}/profil`);
};
</script>
