<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481]">Parcel crops</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">Parcel crops</h1>
      </div>

      <div class="flex items-center gap-3">
        <button @click="loadParcelCrops" class="p-3 bg-white border border-gray-100 rounded-2xl text-gray-400 hover:text-[#10b481] hover:border-[#10b481]/20 transition-all shadow-sm">
          <i class="bx bx-refresh text-xl" :class="{ 'animate-spin': isLoading }"></i>
        </button>
        <NuxtLink
          to="/farmer/parcel-crops/create"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg shadow-[#112830]/10 hover:shadow-[#10b481]/20"
        >
          <i class="bx bx-plus text-lg"></i> {{ t("btnaddparcelcrop") }}
        </NuxtLink>
      </div>
    </div>

    <!-- ===== SEARCH & FILTERS ===== -->
    <div class="bg-white p-4 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col md:flex-row gap-4">
      <div class="relative flex-1 group">
        <i class="bx bx-search absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Rechercher une parcelle ou une culture..."
          class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300"
        >
      </div>
      <div class="flex items-center gap-2 px-4 py-2 bg-emerald-50 rounded-2xl border border-emerald-100/50">
        <span class="text-[10px] font-black text-[#10b481] uppercase tracking-widest">{{ parcelCrops.length }} Total</span>
      </div>
    </div>

    <!-- ===== PREMIUM TABLE ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <div class="overflow-x-auto scrollbar-hidden">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-50/50">
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("thparcelname") }}</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("crop") }}</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("plantingdate") }}</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("harvestdate") }}</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("area") }} (m²)</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">{{ t("status") }}</th>
              <th class="px-8 py-6 text-right text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-50">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="pc in paginatedParcelCrops" :key="pc.id" class="group hover:bg-gray-50/50 transition-colors">
              <td class="px-8 py-6 font-bold text-[#112830] tracking-tight">{{ pc.parcel_name || pc.parcel }}</td>
              <td class="px-8 py-6 text-sm font-medium text-gray-500">{{ pc.crop?.name || "-" }}</td>
              <td class="px-8 py-6 text-xs text-gray-400 font-mono">{{ formatDate(pc.planting_date) }}</td>
              <td class="px-8 py-6 text-xs text-gray-400 font-mono">{{ formatDate(pc.harvest_date) || "-" }}</td>
              <td class="px-8 py-6">
                <span class="px-3 py-1 bg-gray-100 rounded-lg text-xs font-black text-gray-500">{{ pc.area }}</span>
              </td>
              <td class="px-8 py-6">
                <span v-if="pc.status?.name" :class="['px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border transition-all', statusClasses(pc.status.name)]">
                   {{ t(cropStatusKeyMap[pc.status.name] || pc.status?.name) }}
                </span>
                <span v-else class="text-gray-300">-</span>
              </td>
              <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all">
                  <button @click="showParcelCrop(pc.id)" class="w-10 h-10 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center hover:bg-[#10b481] hover:text-white transition-all shadow-sm">
                    <i class="bx bx-show text-lg"></i>
                  </button>
                  <button @click="editParcelCrop(pc.id)" class="w-10 h-10 rounded-xl bg-amber-50 text-amber-500 flex items-center justify-center hover:bg-amber-500 hover:text-white transition-all shadow-sm">
                    <i class="bx bx-edit text-lg"></i>
                  </button>
                  <button @click="deleteParcelCrop(pc.id)" class="w-10 h-10 rounded-xl bg-rose-50 text-rose-500 flex items-center justify-center hover:bg-rose-500 hover:text-white transition-all shadow-sm">
                    <i class="bx bx-trash text-lg"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedParcelCrops.length === 0">
              <td colspan="7" class="px-8 py-20 text-center italic text-gray-300 uppercase tracking-widest text-[10px]">
                 {{ t("noparcelcropfound") }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ===== PREMIUM PAGINATION ===== -->
    <div class="flex items-center justify-between px-10 py-6 bg-white rounded-[2rem] border border-gray-100 shadow-sm">
      <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest">Page {{ currentPage }} / {{ totalPages }}</p>
      
      <div class="flex items-center gap-2">
        <button 
          @click="prevPage" 
          :disabled="currentPage === 1"
          class="w-10 h-10 rounded-xl bg-gray-50 text-gray-400 flex items-center justify-center disabled:opacity-30 disabled:cursor-not-allowed hover:bg-[#112830] hover:text-white transition-all"
        >
          <i class="bx bx-chevron-left text-2xl"></i>
        </button>

        <div class="flex items-center gap-1">
          <button 
            v-for="page in visiblePages" 
            :key="page"
            @click="goToPage(page as number)"
            :class="['w-10 h-10 rounded-xl text-[10px] font-black transition-all', currentPage === page ? 'bg-[#10b481] text-white shadow-lg shadow-[#10b481]/30 scale-110' : 'bg-gray-50 text-gray-400 hover:bg-gray-100']"
          >
            {{ page }}
          </button>
        </div>

        <button 
          @click="nextPage" 
          :disabled="currentPage === totalPages"
          class="w-10 h-10 rounded-xl bg-gray-50 text-gray-400 flex items-center justify-center disabled:opacity-30 disabled:cursor-not-allowed hover:bg-[#112830] hover:text-white transition-all"
        >
          <i class="bx bx-chevron-right text-2xl"></i>
        </button>
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
            <p class="text-[10px] font-medium text-gray-400">Assignation mise à jour</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, computed, onMounted, watch } from "vue";
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
    case "Planned": return "bg-sky-50 text-sky-600 border-sky-100";
    case "Planted": return "bg-emerald-50 text-emerald-600 border-emerald-100";
    case "Growing": return "bg-amber-50 text-amber-600 border-amber-100";
    case "Harvested": return "bg-gray-50 text-gray-600 border-gray-100";
    case "Failed": return "bg-rose-50 text-rose-600 border-rose-100";
    default: return "bg-gray-50 text-gray-400 border-gray-100";
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
const visiblePages = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1));

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
  if (!confirm("Voulez-vous vraiment supprimer cette assignation ?")) return;
  try {
    await apiFetch(`/api/parcel-crops/${id}/`, { method: "DELETE" });
    parcelCrops.value = parcelCrops.value.filter((pc) => pc.id !== id);
    parcelCropsState.value.data = parcelCrops.value;
    showNotification("Assignation supprimée avec succès", "success");
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
  return new Date(dateStr).toLocaleDateString(locale.value, { year: "numeric", month: "short", day: "numeric" });
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
