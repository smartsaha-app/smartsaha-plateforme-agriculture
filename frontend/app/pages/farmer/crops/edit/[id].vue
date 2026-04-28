<template>
  <div class="p-6 min-h-[calc(100vh-5rem)] flex flex-col items-center justify-center space-y-8 text-[#112830]">
    
    <!-- ===== BREADCRUMB & TITLE ===== -->
    <div class="w-full max-w-xl space-y-2 text-center mb-4">
      <nav class="flex items-center justify-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
          <i class="bx bx-home text-xs"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/crops" class="hover:text-[#10b481] transition-colors">
          Crops
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481]">Modifier</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Modifier la Culture</h1>
      <p class="text-gray-500 font-medium max-w-md mx-auto">Mettez à jour les informations de votre culture pour maintenir vos registres précis.</p>
    </div>

    <!-- ===== FORM CARD ===== -->
    <div class="w-full max-w-xl bg-white p-10 rounded-[3rem] border border-gray-100 shadow-[0_20px_50px_rgba(0,0,0,0.04)] relative overflow-hidden">
      <!-- Decorative element -->
      <div class="absolute -top-10 -right-10 w-32 h-32 bg-[#10b481]/5 rounded-full blur-3xl"></div>
      
      <form @submit.prevent="submitCrop" class="relative z-10 space-y-8">
        <!-- Crop Name -->
        <div class="space-y-3">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Nom de la culture *</label>
          <div class="relative group">
            <i class="bx bx-leaf absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-400 group-focus-within:text-[#10b481] transition-colors"></i>
            <input
              v-model="form.name"
              type="text"
              placeholder="Ex: Riz Malagasy"
              required
              class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300"
            />
          </div>
        </div>

        <!-- Variety Selection -->
        <div class="space-y-3">
          <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">Variété *</label>
          <div class="relative group">
            <i class="bx bx-category absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-400 group-focus-within:text-[#10b481] transition-colors"></i>
            <select
              v-model="form.variety_id"
              required
              class="w-full pl-14 pr-10 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none appearance-none transition-all font-medium text-[#112830] placeholder:text-gray-300"
            >
              <option disabled value="">Sélectionnez une variété</option>
              <option v-for="v in varieties" :key="v.id" :value="v.id">
                {{ v.name }}
              </option>
            </select>
            <i class="bx bx-chevron-down absolute right-5 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full group bg-[#112830] hover:bg-[#10b481] py-5 rounded-2xl text-white font-black uppercase tracking-widest text-xs flex justify-center items-center gap-3 transition-all duration-500 shadow-xl shadow-[#112830]/10 hover:shadow-[#10b481]/20 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <template v-if="isLoading">
            <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            Mise à jour...
          </template>
          <template v-else>
            Enregistrer les modifications
            <i class="bx bx-save text-xl group-hover:scale-110 transition-transform"></i>
          </template>
        </button>

        <!-- Cancel/Back -->
        <div class="pt-4 text-center">
          <NuxtLink to="/farmer/crops" class="text-xs font-black text-gray-400 uppercase tracking-widest hover:text-[#10b481] transition-colors">
            Annuler et retourner
          </NuxtLink>
        </div>
      </form>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div
        v-if="notification.visible"
        class="fixed top-10 left-1/2 -translate-x-1/2 z-[100] w-full max-w-sm px-4"
      >
        <div
          :class="[
            'bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100',
            notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500'
          ]"
        >
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">
              {{ notification.type === 'success' ? 'Mise à jour réussie.' : 'Veuillez réessayer plus tard.' }}
            </p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const cropId = route.params.id;

// ===== STATE =====
const form = ref({ name: "", variety_id: null });
const varieties = ref<any[]>([]);
const isLoading = ref(false);
const notification = ref({
  visible: false,
  message: "",
  type: "success" as "success" | "error",
});

// ===== HELPERS =====
const showNotification = (message: string, type: "success" | "error" = "success") => {
  notification.value = { visible: true, message, type };
  setTimeout(() => (notification.value.visible = false), 3000);
};

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  isLoading.value = true;
  try {
    // Load both varieties and the specific crop data
    const [varietiesData, cropData]: any = await Promise.all([
      apiFetch('/api/varieties/'),
      apiFetch(`/api/crops/${cropId}/`)
    ]);
    
    varieties.value = varietiesData;
    form.value.name = cropData.name;
    form.value.variety_id = cropData.variety_id;
  } catch (err) {
    console.error("Failed to load data:", err);
    showNotification("Erreur lors du chargement des données", "error");
  } finally {
    isLoading.value = false;
  }
});

// ===== SUBMIT =====
const submitCrop = async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  isLoading.value = true;
  try {
    await apiFetch(`/api/crops/${cropId}/`, {
      method: "PUT",
      body: form.value,
    });

    showNotification("Culture mise à jour avec succès !", "success");
    setTimeout(() => {
      router.push("/farmer/crops");
    }, 2000);
  } catch (err) {
    console.error(err);
    showNotification("Échec de la mise à jour", "error");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}

input::placeholder,
select::placeholder {
  color: rgba(33, 33, 33, 0.3);
}
</style>
