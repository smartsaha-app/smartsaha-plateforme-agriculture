<template>
  <div class="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-center p-6">
    <div class="w-full max-w-2xl bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100">
      <div class="flex items-center gap-4 mb-8">
        <div class="w-12 h-12 rounded-2xl bg-[#10b481]/10 flex items-center justify-center text-[#10b481]">
          <i class="bx bx-buildings text-3xl"></i>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-[#112830]">Configurez votre Organisation</h1>
          <p class="text-gray-500">Activez votre espace professionnel pour commencer le monitoring.</p>
        </div>
      </div>

      <form @submit.prevent="handleOnboarding" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="text-sm font-bold text-gray-700">Nom de l'Organisation *</label>
            <input 
              v-model="form.name" 
              type="text" 
              placeholder="Ex: Coopérative de Vakinankaratra"
              class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition"
              required
            />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-gray-700">Type d'entité *</label>
            <select 
              v-model="form.org_type" 
              class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition appearance-none bg-white"
              required
            >
              <option value="COOP">Coopérative</option>
              <option value="NGO">ONG</option>
              <option value="PRIVATE">Entreprise Privée</option>
              <option value="GOVERNMENT">Gouvernementale</option>
              <option value="OTHER">Autre</option>
            </select>
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-bold text-gray-700">Email de contact *</label>
          <input 
            v-model="form.contact_email" 
            type="email" 
            placeholder="contact@organisation.mg"
            class="w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10b481] outline-none transition"
            required
          />
        </div>

        <div class="space-y-2">
          <label class="text-sm font-bold text-gray-700">Description</label>
          <textarea 
            v-model="form.description" 
            rows="3"
            placeholder="Décrivez brièvement votre mission..."
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
            <span v-if="!isLoading">Activer mon espace</span>
            <span v-else class="flex items-center gap-2">
              <i class="bx bx-loader-alt animate-spin"></i> Traitement...
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
    
    alert("Organisation créée avec succès ! Votre espace Entreprise est maintenant actif.");
    
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
    alert("Erreur lors de la création : " + (err.data?.name || "Veuillez vérifier les informations."));
  } finally {
    isLoading.value = false;
  }
}

function skipOnboarding() {
  router.push('/farmer/dashboard');
}
</script>
