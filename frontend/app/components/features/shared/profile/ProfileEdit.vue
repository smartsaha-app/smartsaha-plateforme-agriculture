<template>
  <div class="px-4 sm:px-6 md:px-12 py-8">
    <div class="max-w-2xl mx-auto">
      <!-- En-tête -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-[#112830] flex items-center gap-2">
            <i class="bx bx-user-circle text-[#10b481]"></i>
            {{ t("editProfile") }}
          </h1>
          <p class="text-sm text-gray-500 mt-1">Mettez à jour vos informations personnelles</p>
        </div>

        <button
          type="button"
          @click="goBack"
          class="p-2.5 text-gray-500 hover:text-[#112830] hover:bg-gray-100 rounded-xl transition-all"
          :title="t('back')"
        >
          <i class="bx bx-x text-2xl"></i>
        </button>
      </div>

      <!-- Formulaire -->
      <form
        @submit.prevent="updateProfile"
        class="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-gray-100 space-y-6"
      >
        <!-- Badge Avatar / Aperçu -->
        <div class="flex items-center gap-4 pb-6 border-b border-gray-100">
          <div class="w-16 h-16 rounded-2xl bg-[#edf8f3] text-[#10b481] flex items-center justify-center font-black text-xl shadow-inner border border-[#10b481]/20">
            {{ userInitials }}
          </div>
          <div>
            <h2 class="font-bold text-[#112830] text-base">
              {{ form.first_name || form.last_name ? `${form.first_name} ${form.last_name}` : form.username }}
            </h2>
            <p class="text-xs text-gray-400 font-medium">{{ form.username }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Nom d'utilisateur -->
          <div class="col-span-2">
            <label class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
              {{ t("username") }}
            </label>
            <div class="relative">
              <i class="bx bx-[#10b481] bx-at absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
              <input
                v-model="form.username"
                type="text"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:bg-white focus:ring-4 focus:ring-[#10b481]/10 focus:border-[#10b481] outline-none transition-all text-sm font-medium text-[#112830]"
                required
              />
            </div>
          </div>

          <!-- Prénom -->
          <div>
            <label class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
              {{ t("firstName") }}
            </label>
            <div class="relative">
              <i class="bx bx-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
              <input
                v-model="form.first_name"
                type="text"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:bg-white focus:ring-4 focus:ring-[#10b481]/10 focus:border-[#10b481] outline-none transition-all text-sm font-medium text-[#112830]"
              />
            </div>
          </div>

          <!-- Nom -->
          <div>
            <label class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
              {{ t("lastName") }}
            </label>
            <div class="relative">
              <i class="bx bx-user-pin absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
              <input
                v-model="form.last_name"
                type="text"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:bg-white focus:ring-4 focus:ring-[#10b481]/10 focus:border-[#10b481] outline-none transition-all text-sm font-medium text-[#112830]"
              />
            </div>
          </div>

          <!-- Email -->
          <div class="col-span-2">
            <label class="text-gray-700 text-xs font-black uppercase tracking-wider mb-2 block">
              {{ t("email") }}
            </label>
            <div class="relative">
              <i class="bx bx-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
              <input
                v-model="form.email"
                type="email"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl focus:bg-white focus:ring-4 focus:ring-[#10b481]/10 focus:border-[#10b481] outline-none transition-all text-sm font-medium text-[#112830]"
                required
              />
            </div>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="flex flex-col-reverse sm:flex-row items-center justify-between gap-3 pt-6 border-t border-gray-100">
          <button
            type="button"
            @click="goBack"
            class="w-full sm:w-auto px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-2xl transition-all text-sm"
          >
            {{ t("back") }}
          </button>

          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full sm:w-auto px-8 py-3 bg-[#112830] hover:bg-[#10b481] text-white font-bold rounded-2xl transition-all duration-200 shadow-md shadow-[#112830]/10 flex items-center justify-center gap-2 text-sm disabled:opacity-50"
          >
            <i v-if="isSubmitting" class="bx bx-loader-alt animate-spin text-lg"></i>
            <i v-else class="bx bx-check text-lg"></i>
            <span>{{ t("saveChanges") }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
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

// Calcul automatique des initiales pour la vignette avatar
const userInitials = computed(() => {
  return form.value.first_name?.slice(0, 2).toUpperCase();
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  
  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    form.value.username = data.username || "";
    form.value.email = data.email || "";
    form.value.first_name = data.first_name || "";
    form.value.last_name = data.last_name || "";
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