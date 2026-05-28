<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Nouvelle Culture">
      <template #subtitle>
        <i class="bx bx-plus-circle"></i>
        Enregistrez une nouvelle culture pour commencer le suivi de vos parcelles.
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/crops" class="hover:text-[#10b481] transition-colors">Cultures</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Nouvelle</span>
      </template>
    </PageHeader>

    <!-- ===== CONTENT — two side-by-side cards, full width ===== -->
    <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- ── CARD GAUCHE : Formulaire ── -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 flex flex-col">
        <div class="mb-6">
          <h2 class="text-base font-black text-[#112830]">Informations de la culture</h2>
          <p class="text-xs text-gray-400 mt-0.5">Renseignez le nom et la variété de la culture.</p>
        </div>

        <form @submit.prevent="submitCrop" class="flex flex-col gap-5 flex-1">

          <!-- Nom -->
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
              {{ t('cropname') }} <span class="text-[#10b481]">*</span>
            </label>
            <div class="relative">
              <i class="bx bx-leaf absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
              <input
                v-model="form.name"
                type="text"
                :placeholder="t('cropname_placeholder')"
                required
                class="w-full pl-11 pr-10 py-3.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 transition-all font-medium text-[#112830]"
                :class="{ 'border-[#10b481]/30 bg-emerald-50/20': form.name }"
              />
              <i v-if="form.name" class="bx bx-check-circle absolute right-4 top-1/2 -translate-y-1/2 text-[#10b481] text-lg"></i>
            </div>
          </div>

          <!-- Variété -->
          <div class="space-y-2">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest block">
              {{ t('variety') }} <span class="text-[#10b481]">*</span>
            </label>
            <div class="relative">
              <i class="bx bx-category absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
              <select
                v-model="form.variety_id"
                required
                class="w-full pl-11 pr-10 py-3.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 transition-all font-medium text-[#112830] appearance-none cursor-pointer"
                :class="{ 'border-[#10b481]/30 bg-emerald-50/20': form.variety_id }"
              >
                <option disabled value="">{{ t('select_variety') }}</option>
                <option v-for="v in varieties" :key="v.id" :value="v.id">{{ v.name }}</option>
              </select>
              <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- Aperçu animé -->
          <transition name="slide-down">
            <div v-if="form.name && form.variety_id"
              class="flex items-center gap-3 p-4 bg-emerald-50 border border-emerald-100 rounded-xl">
              <div class="w-10 h-10 rounded-xl bg-[#10b481] flex items-center justify-center flex-shrink-0">
                <i class="bx bx-leaf text-white text-lg"></i>
              </div>
              <div>
                <p class="text-[9px] font-black text-[#10b481] uppercase tracking-widest leading-none mb-0.5">Prêt à enregistrer</p>
                <p class="text-sm font-bold text-[#112830] leading-tight">
                  {{ form.name }}
                  <span class="text-gray-400 font-medium"> — {{ selectedVarietyName }}</span>
                </p>
              </div>
            </div>
          </transition>

          <!-- Actions — poussées en bas -->
          <div class="flex gap-3 mt-auto pt-4">
            <NuxtLink
              to="/farmer/crops"
              class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors text-center"
            >
              Annuler
            </NuxtLink>
            <button
              type="submit"
              :disabled="isLoading || !form.name || !form.variety_id"
              class="flex-[2] py-3 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all shadow-sm disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <div v-if="isLoading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <template v-else>
                <i class="bx bx-save text-base"></i>
                {{ t('btnsavecrop') }}
              </template>
            </button>
          </div>
        </form>
      </div>

      <!-- ── CARD DROITE : Informations ── -->
      <div class="bg-[#112830] rounded-2xl overflow-hidden shadow-sm flex flex-col relative">
        <!-- Pattern décoratif -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none opacity-[0.04]">
          <div class="absolute -top-12 -right-12 w-56 h-56 border-[3px] border-white rounded-full"></div>
          <div class="absolute top-1/3 -left-16 w-48 h-48 border-2 border-white rounded-full"></div>
          <div class="absolute bottom-0 right-1/4 w-32 h-32 border border-white rounded-full"></div>
        </div>

        <div class="relative z-10 p-8 flex flex-col h-full gap-8">

          <!-- En-tête -->
          <div>
            <div class="w-14 h-14 rounded-2xl bg-[#10b481] flex items-center justify-center mb-5 shadow-lg shadow-emerald-900/30">
              <i class="bx bx-leaf text-white text-2xl"></i>
            </div>
            <h2 class="text-white font-black text-xl leading-tight mb-2">Pourquoi enregistrer vos cultures ?</h2>
            <p class="text-slate-400 text-sm leading-relaxed">
              Un catalogue de cultures bien structuré est la base d'une gestion agricole efficace et traçable.
            </p>
          </div>

          <!-- Bénéfices -->
          <div class="space-y-4">
            <div v-for="benefit in benefits" :key="benefit.title" class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center flex-shrink-0">
                <i :class="benefit.icon" class="text-[#10b481] text-lg"></i>
              </div>
              <div>
                <p class="text-white text-sm font-bold leading-none mb-1">{{ benefit.title }}</p>
                <p class="text-slate-400 text-xs leading-relaxed">{{ benefit.desc }}</p>
              </div>
            </div>
          </div>

          <!-- Statistique décorative en bas -->
          <div class="mt-auto grid grid-cols-3 gap-3">
            <div class="p-3 bg-white/5 border border-white/10 rounded-xl text-center">
              <p class="text-[#10b481] text-lg font-black">100%</p>
              <p class="text-slate-400 text-[9px] uppercase tracking-wide font-bold">Traçable</p>
            </div>
            <div class="p-3 bg-white/5 border border-white/10 rounded-xl text-center">
              <p class="text-[#10b481] text-lg font-black">∞</p>
              <p class="text-slate-400 text-[9px] uppercase tracking-wide font-bold">Cultures</p>
            </div>
            <div class="p-3 bg-white/5 border border-white/10 rounded-xl text-center">
              <p class="text-[#10b481] text-lg font-black">IA</p>
              <p class="text-slate-400 text-[9px] uppercase tracking-wide font-bold">Conseils</p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ===== NOTIFICATION ===== -->
    <transition name="pop-notification">
      <div
        v-if="notification.visible"
        class="fixed top-6 left-1/2 -translate-x-1/2 z-[100] w-full max-w-sm px-4"
      >
        <div
          :class="[
            'bg-white rounded-2xl shadow-xl p-5 flex items-center gap-4 border',
            notification.type === 'success' ? 'border-l-4 border-l-[#10b481] border-gray-100' : 'border-l-4 border-l-rose-500 border-gray-100'
          ]"
        >
          <div :class="[
            'w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0',
            notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500'
          ]">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div>
            <p class="text-sm font-black text-[#112830]">{{ notification.message }}</p>
            <p class="text-[10px] text-gray-400">
              {{ notification.type === 'success' ? 'Redirection en cours...' : 'Veuillez corriger les informations.' }}
            </p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard' });

import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useApi } from '~/composables/useApi';

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const router    = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const form      = ref({ name: '', variety_id: '' });
const varieties = ref<any[]>([]);
const isLoading = ref(false);
const notification = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

const benefits = [
  { icon: 'bx bx-map-alt',     title: 'Association aux parcelles',  desc: 'Liez chaque culture à une ou plusieurs parcelles pour un suivi géolocalisé.' },
  { icon: 'bx bx-trending-up', title: 'Suivi des rendements',       desc: 'Analysez vos rendements saison par saison et optimisez vos prochaines récoltes.' },
  { icon: 'bx bx-bug',         title: 'Historique des incidents',   desc: 'Enregistrez les maladies, ravageurs et interventions pour chaque culture.' },
  { icon: 'bx bx-robot',       title: 'Conseils personnalisés IA',  desc: 'Sesily vous donnera des recommandations adaptées à vos cultures enregistrées.' },
];

const selectedVarietyName = computed(() =>
  varieties.value.find(v => v.id == form.value.variety_id)?.name || ''
);

function showNotification(message: string, type: 'success' | 'error' = 'success', duration = 3000) {
  notification.value = { visible: true, message, type };
  setTimeout(() => (notification.value.visible = false), duration);
}

onMounted(async () => {
  if (!authStore.isAuthenticated) { router.push('/login'); return; }
  try {
    const data: any = await apiFetch('/api/varieties/');
    varieties.value = data;
  } catch (err) {
    showNotification(t('error_load_data'), 'error');
  }
});

async function submitCrop() {
  if (!authStore.isAuthenticated) { router.push('/login'); return; }
  isLoading.value = true;
  try {
    await apiFetch('/api/crops/', { method: 'POST', body: form.value });
    showNotification(t('success_save'), 'success');
    form.value = { name: '', variety_id: '' };
    setTimeout(() => router.push('/farmer/crops'), 2000);
  } catch (err) {
    showNotification(t('error_save'), 'error');
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-notification-enter-from,
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -16px) scale(0.92);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>