<template>
  <div class="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-center p-6">
    <div class="w-full max-w-2xl bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100">
      <div class="flex items-center gap-4 mb-8">
        <div class="w-12 h-12 rounded-2xl bg-[#10b481]/10 flex items-center justify-center text-[#10b481]">
          <i class="bx bx-buildings text-3xl"></i>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-[#112830]">{{ $t("onboarding.title") }}</h1>
          <p class="text-gray-500">{{ $t("onboarding.subtitle") }}</p>
        </div>
      </div>

      <form @submit.prevent="handleOnboarding" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="text-sm font-bold text-gray-700">{{ $t("onboarding.orgName") }}</label>
            <input 
              v-model="form.name" 
              type="text" 
              :placeholder="$t('onboarding.orgName').replace(' *', '')"
              class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition"
              required
            />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-gray-700">{{ $t("onboarding.orgType") }}</label>
            <select 
              v-model="form.org_type" 
              class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition appearance-none bg-white"
              required
            >
              <option value="COOP">{{ $t("onboarding.coop") }}</option>
              <option value="NGO">{{ $t("onboarding.ngo") }}</option>
              <option value="PRIVATE">{{ $t("onboarding.private") }}</option>
              <option value="GOVERNMENT">{{ $t("onboarding.government") }}</option>
              <option value="OTHER">{{ $t("onboarding.other") }}</option>
            </select>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-bold text-gray-700">{{ $t("onboarding.contactEmail") }}</label>
          <input 
            v-model="form.contact_email" 
            type="email" 
            placeholder="contact@organisation.com"
            class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition"
            required
          />
        </div>

        <div class="space-y-2">
          <label class="text-sm font-bold text-gray-700">{{ $t("onboarding.description") }}</label>
          <textarea 
            v-model="form.description" 
            rows="3"
            :placeholder="$t('onboarding.missionPlaceholder')"
            class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition"
          ></textarea>
        </div>

        <div class="flex items-center justify-end gap-4 pt-4">
          <!-- <button 
            type="button"
            @click="skipOnboarding"
            class="px-6 py-3 text-gray-400 font-medium hover:text-gray-600 transition"
          >
            Plus tard
          </button> -->
          <button 
            type="submit"
            :disabled="isLoading"
            class="px-10 py-3 bg-[#10b481] text-white rounded-xl font-bold hover:bg-[#0da06a] transition shadow-lg shadow-[#10b481]/20 disabled:opacity-50"
          >
            <span v-if="!isLoading">{{ $t("onboarding.activateBtn") }}</span>
            <span v-else class="flex items-center gap-2">
              <i class="bx bx-loader-alt animate-spin"></i> {{ $t("dashboard.processing") }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';

const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();
const router = useRouter();
const isLoading = ref(false);

const form = ref({
  name: '',
  org_type: 'COOP',
  contact_email: '',
  description: '',
});

async function handleOnboarding() {
  isLoading.value = true;
  try {
    // Création de l'organisation
    const org = await apiFetch('/api/organisations/', {
      method: 'POST',
      body: form.value
    });
    
    // On pourrait aussi créer un groupe par défaut ici si nécessaire
    
    alert(nuxtT("onboarding.successMsg"));
    
    // Rafraîchir les infos utilisateur pour mettre à jour les "spaces"
    try {
      const authStore = useAuthStore();
      const userData: any = await apiFetch(`/api/users/${authStore.uuid}/`);
      authStore.setUserData({ spaces: userData.spaces });
    } catch (e) {
      console.error("Erreur refresh user data:", e);
    }

    router.push('/organization/dashboard');
  } catch (err: any) {
    console.error(err);
    alert(nuxtT("onboarding.errorMsg") + (err.data?.name || nuxtT("onboarding.checkInfo")));
  } finally {
    isLoading.value = false;
  }
}

function skipOnboarding() {
  router.push('/farmer/dashboard');
}
</script>
