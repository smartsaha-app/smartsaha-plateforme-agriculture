<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="space-y-2">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1 font-bold">
          <i class="bx bx-home text-xs font-bold"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/yield-records" class="hover:text-[#10b481] transition-colors font-bold">Récoltes</NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481] font-bold">Modifier l'Enregistrement</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Édition Journalière</h1>
    </div>

    <div v-if="initialLoading" class="min-h-[400px] flex flex-col items-center justify-center gap-4 text-gray-400">
      <div class="w-12 h-12 border-4 border-t-[#10b481] border-gray-100 rounded-full animate-spin"></div>
      <p class="text-[10px] font-black uppercase tracking-widest font-bold">Chargement des données...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-2">
        <form @submit.prevent="update" class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12 space-y-10">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-bold text-bold">
            <!-- Date -->
            <div class="space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("thdate") }} *</label>
              <div class="relative group font-bold">
                <i class="bx bx-calendar absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <input 
                  v-model="form.date"
                  type="date" 
                  required
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all font-bold"
                >
              </div>
            </div>

            <!-- Yield Amount -->
            <div class="space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("thyield") }} *</label>
              <div class="relative group font-bold">
                <i class="bx bx-layer absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <input 
                  v-model.number="form.yield_amount"
                  type="number" 
                  step="0.01"
                  required
                  placeholder="Quantité récoltée"
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all font-bold placeholder:text-gray-300"
                >
              </div>
            </div>

            <!-- Area -->
            <div class="space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("area") }} (m²) *</label>
              <div class="relative group font-bold">
                <i class="bx bx-area absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <input 
                  v-model.number="form.area"
                  type="number" 
                  step="0.01"
                  required
                  placeholder="Surface récoltée"
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all font-bold placeholder:text-gray-300"
                >
              </div>
            </div>

            <!-- Notes -->
            <div class="md:col-span-2 space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("notes") }}</label>
              <div class="relative group font-bold">
                <i class="bx bx-note absolute left-5 top-6 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors font-bold"></i>
                <textarea 
                  v-model="form.notes"
                  placeholder="Observations sur la récolte..."
                  class="w-full pl-14 pr-6 py-5 bg-gray-50 border border-gray-50 rounded-[2rem] focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all min-h-[120px] resize-none font-bold placeholder:text-gray-300"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col md:flex-row items-center justify-end gap-4 pt-6 font-bold">
            <NuxtLink to="/farmer/yield-records" class="w-full md:w-auto px-8 py-4 text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-[#112830] transition-colors text-center font-bold">
              {{ t("cancel") }}
            </NuxtLink>
            <button 
              type="submit" 
              :disabled="isLoading"
              class="w-full md:w-auto px-10 py-4 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] hover:bg-[#10b481] transition-all shadow-xl shadow-[#112830]/10 disabled:opacity-50 flex items-center justify-center gap-3 font-bold font-bold"
            >
              <div v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin font-bold"></div>
              <span>Mettre à jour la récolte</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Preview / History Sidebar -->
      <div class="space-y-6 font-bold">
        <div class="bg-gray-50 rounded-[3rem] p-10 border border-gray-100 space-y-8 font-bold text-bold">
           <div class="w-16 h-16 rounded-2xl bg-white flex items-center justify-center text-3xl text-[#10b481] shadow-sm font-bold">
            <i class="bx bx-history font-bold"></i>
          </div>
          <div class="space-y-4 font-bold">
             <h3 class="text-xl font-black tracking-tight tracking-tighter font-bold">Historique Récolte</h3>
             <div class="space-y-4 font-bold text-bold">
               <div class="flex items-center gap-3 text-xs font-bold">
                 <span class="w-2 h-2 rounded-full bg-emerald-400 font-bold"></span>
                 <span class="text-gray-400 font-bold">Date initiale :</span>
                 <span class="text-[#112830] font-bold">{{ formatDate(initialDate) }}</span>
               </div>
               <div class="flex items-center gap-3 text-xs font-bold">
                 <span class="w-2 h-2 rounded-full bg-amber-400 font-bold"></span>
                 <span class="text-gray-400 font-bold font-bold">MàJ Système :</span>
                 <span class="text-[#112830] font-bold">{{ formatDate(new Date().toISOString()) }}</span>
               </div>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100 font-bold', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 font-bold', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500 font-bold']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error font-bold font-bold'"></i>
          </div>
          <div class="flex-1 font-bold">
            <p class="text-sm font-black text-[#112830] tracking-tight font-bold">{{ notification.message }}</p>
            <span class="text-[10px] font-medium text-gray-400 uppercase tracking-widest font-bold">Confirmation</span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const id = route.params.id as string;

// ===== STATE =====
const isLoading = ref(false);
const initialLoading = ref(true);
const initialDate = ref("");
const notification = ref({ visible: false, message: "", type: "success" });

const form = ref({
  date: "",
  yield_amount: 0,
  area: 0,
  notes: "",
});

// ===== HELPERS =====
const showNotification = (message: string, type = "success") => {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
};

const formatDate = (date: string | null) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "long", day: "numeric" });
};

// ===== LIFECYCLE =====
onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  try {
    const data: any = await apiFetch(`/api/yield-records/${id}/`);
    form.value = {
      date: data.date || "",
      yield_amount: data.yield_amount || 0,
      area: data.area || 0,
      notes: data.notes || "",
    };
    initialDate.value = data.created_at || data.date;
  } catch (err) {
    showNotification("Erreur de chargement", "error");
  } finally {
    initialLoading.value = false;
  }
});

// ===== ACTIONS =====
const update = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  isLoading.value = true;
  try {
    await apiFetch(`/api/yield-records/${id}/`, { method: "PUT", body: form.value });
    showNotification("Récolte mise à jour avec succès !", "success");
    setTimeout(() => router.push({ path: "/farmer/yield-records" }), 2000);
  } catch (err) {
    showNotification("Erreur lors de la sauvegarde", "error");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.pop-notification-enter-active, .pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from, .pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>
