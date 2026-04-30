<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1 font-bold">
            <i class="bx bx-home text-xs font-bold"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <NuxtLink to="/farmer/yield-records" class="hover:text-[#10b481] transition-colors font-bold">Récoltes</NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481] font-bold italic">Détails de la Récolte</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">Analyse de Récolte</h1>
      </div>

      <div class="flex items-center gap-3 font-bold">
        <button @click="goBack" class="p-3 bg-white border border-gray-100 rounded-2xl text-gray-400 hover:text-[#10b481] transition-all shadow-sm font-bold">
          <i class="bx bx-arrow-back text-xl font-bold"></i>
        </button>
        <button
          @click="goToEdit"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg font-bold"
        >
          <i class="bx bx-edit-alt text-lg font-bold"></i> {{ t("edit") }}
        </button>
      </div>
    </div>

    <div v-if="initialLoading" class="min-h-[400px] flex flex-col items-center justify-center gap-4 text-gray-400 font-bold">
      <div class="w-12 h-12 border-4 border-t-[#10b481] border-gray-100 rounded-full animate-spin font-bold"></div>
      <p class="text-[10px] font-black uppercase tracking-widest font-bold">Chargement des détails...</p>
    </div>

    <div v-else-if="yieldRecord" class="grid grid-cols-1 lg:grid-cols-3 gap-8 font-bold">
      <!-- MAIN CONTENT -->
      <div class="lg:col-span-2 space-y-8 font-bold">
        <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12 space-y-10 font-bold">
          <!-- Yield Metric Hero -->
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-8 font-bold">
            <div class="space-y-4 font-bold">
              <div class="flex items-center gap-3 font-bold">
                <div class="w-12 h-12 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center text-2xl shadow-sm font-bold">
                  <i class="bx bx-layer font-bold"></i>
                </div>
                <h2 class="text-2xl font-black uppercase tracking-widest text-gray-400 font-bold">{{ t("thyield") }}</h2>
              </div>
              <div class="flex items-baseline gap-2 font-bold">
                <span class="text-6xl font-black tracking-tighter text-[#112830]">{{ yieldRecord.yield_amount }}</span>
                <span class="text-xl font-bold text-gray-300 uppercase italic font-bold">unités</span>
              </div>
            </div>

            <div class="p-8 bg-[#112830] rounded-[2rem] text-white space-y-2 font-bold min-w-[200px] text-center md:text-left">
              <p class="text-[10px] font-black uppercase tracking-widest text-[#10b481]">Productivité</p>
              <p class="text-4xl font-black tracking-tighter">{{ (yieldRecord.yield_amount / yieldRecord.area).toFixed(2) }}</p>
              <p class="text-[10px] text-gray-400 font-bold font-bold font-bold">unités / m²</p>
            </div>
          </div>

          <!-- Notes / Observations -->
          <div class="space-y-4 pt-10 border-t border-gray-50 font-bold">
            <h3 class="text-[10px] font-black uppercase tracking-widest text-gray-400 tracking-[0.2em] font-bold">Observations de terrain</h3>
            <p class="text-gray-500 leading-relaxed font-bold italic">
               {{ yieldRecord.notes || "Aucune note particulière n'a été enregistrée pour cette récolte." }}
            </p>
          </div>

          <!-- Linked Data -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-10 font-bold">
            <div class="p-6 bg-gray-50 rounded-[2rem] border border-gray-50 font-bold">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Parcelle de Récolte</p>
              <div class="flex items-center gap-3 text-[#112830] font-bold">
                <i class="bx bx-map-pin text-xl text-[#10b481] font-bold"></i>
                <span class="font-bold text-lg tracking-tight font-bold">{{ parcelData?.parcel_name || "Non spécifié" }}</span>
              </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-[2rem] border border-gray-50 font-bold">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 font-bold">Culture Associée</p>
              <div class="flex items-center gap-3 text-[#112830] font-bold">
                <i class="bx bx-spa text-xl text-[#10b481] font-bold font-bold"></i>
                <span class="font-bold text-lg tracking-tight font-bold">{{ parcelCropData?.crop?.name || "Non spécifié" }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SIDEBAR METRICS -->
      <div class="space-y-8 font-bold">
        <div class="bg-white rounded-[3rem] p-8 border border-gray-100 shadow-sm space-y-8 font-bold text-bold">
           <div class="space-y-1 font-bold">
             <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 font-bold">Date de l'enregistrement</p>
             <p class="text-3xl font-black tracking-tighter text-[#112830] font-bold font-bold">{{ formatDate(yieldRecord.date) }}</p>
           </div>

           <div class="space-y-1 font-bold">
             <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 font-bold">Surface Récoltée</p>
             <div class="flex items-baseline gap-2 font-bold">
               <p class="text-3xl font-black tracking-tighter text-[#112830] font-bold">{{ yieldRecord.area }}</p>
               <span class="text-sm font-bold text-gray-300 italic font-bold">m²</span>
             </div>
           </div>

           <div class="pt-6 border-t border-gray-50 space-y-4 font-bold text-bold">
              <div class="flex items-center justify-between text-[10px] font-bold font-bold">
                <span class="text-gray-400 uppercase tracking-widest font-bold">Créé le</span>
                <span class="text-[#112830] font-bold">{{ formatDate(yieldRecord.created_at) }}</span>
              </div>
              <div class="flex items-center justify-between text-[10px] font-bold font-bold">
                <span class="text-gray-400 uppercase tracking-widest font-bold font-bold">ID Référence</span>
                <span class="text-gray-300 font-bold font-bold">#{{ yieldRecord.id }}</span>
              </div>
           </div>
        </div>

        <!-- Quick Actions Sidebar -->
        <div class="bg-emerald-50 rounded-[2rem] p-8 border border-emerald-100/50 flex flex-col gap-4 font-bold">
           <h4 class="text-[10px] font-black uppercase tracking-widest text-[#10b481] font-bold">Actions de gestion</h4>
           <div class="flex flex-col gap-2 font-bold text-bold">
             <button @click="goToEdit" class="w-full py-3 bg-white border border-emerald-100 rounded-xl text-[10px] font-black uppercase tracking-widest text-[#112830] hover:bg-emerald-100 transition-all font-bold font-bold">
               Modifier les données
             </button>
             <button @click="goBack" class="w-full py-3 text-[10px] font-black uppercase tracking-widest text-emerald-600 hover:text-emerald-800 transition-colors font-bold font-bold">
               Retour au journal
             </button>
           </div>
        </div>
      </div>
    </div>
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

const authStore = useAuthStore();
const { apiFetch } = useApi();
const route = useRoute();
const router = useRouter();

const id = route.params.id as string;
const yieldRecord = ref<any>(null);
const parcelCropData = ref<any>(null);
const parcelData = ref<any>(null);
const initialLoading = ref(true);

const fetchYield = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  try {
    const data: any = await apiFetch(`/api/yield-records/${id}/`);
    yieldRecord.value = data;

    if (yieldRecord.value.parcelCrop) {
      const pc: any = await apiFetch(`/api/parcel-crops/${yieldRecord.value.parcelCrop}/`);
      parcelCropData.value = pc;
      if (pc.parcel) {
        const p: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
        parcelData.value = p;
      }
    }
  } catch (err) {
    console.error(err);
  } finally {
    initialLoading.value = false;
  }
};

const formatDate = (date: string | null) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "long", day: "numeric" });
};

const goToEdit = () => router.push(`/farmer/yield-records/edit/${id}`);
const goBack = () => router.push("/farmer/yield-records");

onMounted(fetchYield);
</script>
