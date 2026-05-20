<template>
  <div class="p-6 md:p-8 space-y-8 bg-[#F8FAFC] min-h-screen">
    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-start justify-between gap-6">
      <div class="space-y-3 max-w-2xl">
        <h1 class="text-4xl font-bold text-[#112830] tracking-tight">Plantations</h1>
        <p class="text-gray-500 text-sm leading-relaxed">
          Gérez vos cultures plantées, suivez leur évolution et optimisez vos rendements en temps réel avec nos outils d'analyse avancés.
        </p>
      </div>

      <div class="flex items-center gap-3 shrink-0">
        <button @click="loadParcelCrops" class="p-3 bg-white border border-gray-200 rounded-xl text-gray-400 hover:text-[#10b481] hover:border-[#10b481]/20 transition-all shadow-sm">
          <i class="bx bx-refresh text-xl" :class="{ 'animate-spin': isLoading }"></i>
        </button>
        <NuxtLink
          to="/farmer/parcel-crops/create"
          class="flex items-center gap-2 px-5 py-3 bg-[#0d2a23] text-white rounded-xl font-medium text-sm hover:bg-[#10b481] transition-all shadow-sm"
        >
          <i class="bx bx-plus text-lg"></i> Nouvelle Plantation
        </NuxtLink>
      </div>
    </div>

    <!-- CARDS SECTION -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Card 1 -->
      <div class="bg-white rounded-[2rem] p-8 border border-gray-100 shadow-sm relative overflow-hidden flex flex-col justify-between">
        <div class="absolute top-0 right-0 w-40 h-40 bg-emerald-50/50 rounded-bl-full"></div>
        <div class="relative z-10 space-y-4 mb-8">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-emerald-50 text-[#10b481] rounded-xl flex items-center justify-center text-2xl">
              <i class="bx bx-receipt"></i>
            </div>
            <h2 class="text-xl font-bold text-[#112830]">Gestion des tâches et suivi des rendements</h2>
          </div>
          <p class="text-gray-500 text-sm leading-relaxed">
            Optimisez votre calendrier agricole. Planifiez l'irrigation, la fertilisation et surveillez la croissance grâce à nos indicateurs de performance automatisés.
          </p>
        </div>
        <div class="relative z-10 flex flex-wrap items-center gap-3">
          <button class="px-5 py-2.5 bg-white border border-gray-200 text-[#112830] rounded-xl text-sm font-medium hover:border-[#112830] transition-colors flex items-center gap-2">
            Gérer les tâches <i class="bx bx-right-arrow-alt"></i>
          </button>
          <button class="px-5 py-2.5 bg-white border border-gray-200 text-[#112830] rounded-xl text-sm font-medium hover:border-[#112830] transition-colors flex items-center gap-2">
            Gérer le rendement <i class="bx bx-right-arrow-alt"></i>
          </button>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="bg-[#1e3f32] rounded-[2rem] p-8 relative overflow-hidden text-white shadow-sm flex flex-col justify-between">
        <!-- Decoration -->
        <div class="absolute -bottom-10 -right-10 w-48 h-48 bg-white/5 rounded-full blur-2xl"></div>
        <div class="absolute top-10 right-10 w-24 h-24 bg-white/5 rounded-full blur-xl"></div>
        
        <div class="relative z-10 space-y-5 mb-6">
          <div class="flex items-center gap-3">
            <i class="bx bx-sparkles text-[#a3e6cd] text-2xl"></i>
            <h2 class="text-xl font-bold">Recommandations IA</h2>
          </div>
          
          <div class="space-y-3">
            <div class="bg-white/10 rounded-2xl p-4 flex items-center gap-4 border border-white/5 backdrop-blur-sm">
              <div class="w-8 h-8 rounded-full bg-[#a3e6cd]/20 text-[#a3e6cd] flex items-center justify-center shrink-0">
                <i class="bx bx-droplet"></i>
              </div>
              <p class="text-sm font-medium text-emerald-50">Ajouter irrigation cette semaine sur Zone Alpha-7</p>
            </div>
            
            <div class="bg-white/10 rounded-2xl p-4 flex items-center gap-4 border border-white/5 backdrop-blur-sm">
              <div class="w-8 h-8 rounded-full bg-[#a3e6cd]/20 text-[#a3e6cd] flex items-center justify-center shrink-0">
                <i class="bx bx-leaf"></i>
              </div>
              <p class="text-sm font-medium text-emerald-50">Appliquer fertilisant azoté (Rendement +12%)</p>
            </div>
          </div>
        </div>
        
        <button class="relative z-10 w-full py-3.5 bg-[#a3e6cd] text-[#1e3f32] rounded-xl text-sm font-bold hover:bg-[#8bd1b6] transition-colors">
          Voir recommandations
        </button>
      </div>
    </div>

    <!-- TABLE SECTION -->
    <div class="space-y-4">
      <h2 class="text-2xl font-bold text-[#112830]">Liste des plantations actives</h2>
      
      <div class="bg-white rounded-[2rem] border border-gray-100 shadow-sm overflow-hidden flex flex-col">
        <div class="overflow-x-auto scrollbar-hidden">
          <table class="w-full text-left border-collapse min-w-[900px]">
            <thead>
              <tr class="bg-gray-50/50">
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Culture</th>
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Parcelle</th>
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Surface</th>
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Date Plantation</th>
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Date Récolte</th>
                <th class="px-6 py-4 text-sm font-bold text-[#112830] border-b border-gray-100">Statut</th>
                <th class="px-6 py-4 text-right text-sm font-bold text-[#112830] border-b border-gray-100">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="pc in paginatedParcelCrops" :key="pc.id" class="group hover:bg-gray-50/50 transition-colors">
                <td class="px-6 py-4 text-sm font-bold text-[#112830]">{{ pc.crop?.name || "-" }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ pc.parcel_name || pc.parcel }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ pc.area ? pc.area.toLocaleString() + ' m²' : '-' }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(pc.planting_date) }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(pc.harvest_date) || "-" }}</td>
                <td class="px-6 py-4">
                  <span v-if="pc.status?.name" :class="['px-3 py-1 rounded-full text-xs font-medium transition-all', statusClasses(pc.status.name)]">
                     {{ t(cropStatusKeyMap[pc.status.name] || pc.status?.name) }}
                  </span>
                  <span v-else class="text-gray-300">-</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-3 text-gray-400">
                    <button @click="showParcelCrop(pc.id)" class="hover:text-[#112830] transition-colors"><i class="bx bx-show text-lg"></i></button>
                    <button @click="editParcelCrop(pc.id)" class="hover:text-[#112830] transition-colors"><i class="bx bx-pencil text-lg"></i></button>
                    <button @click="deleteParcelCrop(pc.id)" class="hover:text-rose-500 transition-colors"><i class="bx bx-trash text-lg"></i></button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedParcelCrops.length === 0">
                <td colspan="7" class="px-6 py-12 text-center text-gray-400 text-sm">
                   Aucune plantation trouvée.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- PAGINATION -->
        <div class="flex flex-col sm:flex-row items-center justify-between px-6 py-4 border-t border-gray-100 bg-white gap-4">
          <p class="text-sm text-gray-500 font-medium">
            Affichage de {{ paginatedParcelCrops.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }} à {{ Math.min(currentPage * itemsPerPage, filteredParcelCrops.length) }} sur {{ filteredParcelCrops.length }} plantations
          </p>
          
          <div class="flex items-center gap-1">
            <button 
              @click="prevPage" 
              :disabled="currentPage === 1"
              class="px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mr-2"
            >
              Précédent
            </button>

            <button 
              v-for="(page, idx) in visiblePages" 
              :key="idx"
              @click="page !== '...' ? goToPage(page as number) : null"
              :disabled="page === '...'"
              :class="[
                page === '...' ? 'px-2 text-gray-400 cursor-default' : 'w-9 h-9 rounded-lg text-sm font-bold transition-all flex items-center justify-center cursor-pointer', 
                currentPage === page ? 'bg-[#0d2a23] text-white' : (page !== '...' ? 'text-gray-500 hover:bg-gray-100' : '')
              ]"
            >
              {{ page }}
            </button>

            <button 
              @click="nextPage" 
              :disabled="currentPage === totalPages"
              class="px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors ml-2"
            >
              Suivant
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">Mise à jour</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const cropStatusKeyMap: Record<string, string> = {
  Planned: "cropStatusPlanned",
  Planted: "cropStatusPlanted",
  Germinated: "cropStatusGerminated",
  Growing: "cropStatusGrowing",
  Flowering: "cropStatusFlowering",
  Fruiting: "cropStatusFruiting",
  Mature: "cropStatusMature",
  Harvested: "cropStatusHarvested",
  "Post-Harvest": "cropStatusPostHarvest",
  Failed: "cropStatusFailed",
};

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const isLoading = ref(false);
const searchQuery = ref("");
const notification = ref({ visible: false, message: "", type: "success" });

const parcelCropsState = useState<{ data: any[]; timestamp: number }>("parcelCropsData", () => ({
  data: [],
  timestamp: 0,
}));

const parcelCrops = ref<any[]>(parcelCropsState.value.data);
const parcelCache: Record<string, string> = {};

function showNotification(message: string, type: "success" | "error" = "success") {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
}

async function parcelName(id: string): Promise<string> {
  if (parcelCache[id]) return parcelCache[id];
  if (!authStore.isAuthenticated) return id;
  try {
    const data: any = await apiFetch(`/api/parcels/${id}/`);
    parcelCache[id] = data.parcel_name;
    return data.parcel_name;
  } catch (err) {
    return id;
  }
}

const statusClasses = (statusName: string) => {
  switch (statusName) {
    case "Planned": return "bg-sky-100 text-sky-700";
    case "Planted": return "bg-[#bbf7d0] text-[#166534]";
    case "Growing": return "bg-amber-100 text-amber-700";
    case "Harvested": return "bg-gray-100 text-gray-700";
    case "Failed": return "bg-rose-100 text-rose-700";
    default: return "bg-gray-100 text-gray-500";
  }
};

const itemsPerPage = 6;
const currentPage = ref(1);

const filteredParcelCrops = computed(() => {
  if (!searchQuery.value) return parcelCrops.value;
  const q = searchQuery.value.toLowerCase();
  return parcelCrops.value.filter(pc => 
    (pc.parcel_name || "").toLowerCase().includes(q) || 
    (pc.crop?.name || "").toLowerCase().includes(q)
  );
});

const paginatedParcelCrops = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredParcelCrops.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => Math.ceil(filteredParcelCrops.value.length / itemsPerPage) || 1);
const visiblePages = computed(() => {
  const pages = [];
  for (let i = 1; i <= totalPages.value; i++) {
    if (
      i === 1 || 
      i === totalPages.value || 
      (i >= currentPage.value - 1 && i <= currentPage.value + 1)
    ) {
      pages.push(i);
    } else if (pages[pages.length - 1] !== "...") {
      pages.push("...");
    }
  }
  return pages;
});

async function loadParcelCrops() {
  if (!authStore.isAuthenticated) return;
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/parcel-crops/');
    const records = data?.results || data || [];
    for (const crop of records) {
      if (crop.parcel) crop.parcel_name = await parcelName(crop.parcel);
    }
    parcelCrops.value = records;
    parcelCropsState.value = { data: records, timestamp: Date.now() };
    if (currentPage.value > totalPages.value) currentPage.value = 1;
  } catch (err) {
    showNotification("Erreur de chargement", "error");
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  const now = Date.now();
  if (parcelCropsState.value.data.length && now - parcelCropsState.value.timestamp < 30 * 60 * 1000) {
    parcelCrops.value = parcelCropsState.value.data;
  } else {
    await loadParcelCrops();
  }
});

const deleteParcelCrop = async (id: number) => {
  if (!confirm("Voulez-vous vraiment supprimer cette plantation ?")) return;
  try {
    await apiFetch(`/api/parcel-crops/${id}/`, { method: "DELETE" });
    parcelCrops.value = parcelCrops.value.filter((pc) => pc.id !== id);
    parcelCropsState.value.data = parcelCrops.value;
    showNotification("Plantation supprimée avec succès", "success");
  } catch (err) {
    showNotification("Erreur lors de la suppression", "error");
  }
};

const editParcelCrop = (id: number) => router.push(`/farmer/parcel-crops/edit/${id}`);
const showParcelCrop = (id: number) => router.push(`/farmer/parcel-crops/show/${id}`);
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
const goToPage = (page: number) => { currentPage.value = page; };

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleDateString(locale.value || "fr-FR", { year: "numeric", month: "short", day: "numeric" });
};
</script>

<style scoped>
.scrollbar-hidden::-webkit-scrollbar { display: none; }
.scrollbar-hidden { -ms-overflow-style: none; scrollbar-width: none; }

.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from,
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>
