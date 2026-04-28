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
          <span class="text-[#10b481] italic">Récoltes</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">Journal des Récoltes</h1>
      </div>

      <div class="flex items-center gap-3">
        <div class="relative group hidden md:block font-bold">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-[#10b481] transition-colors"></i>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Rechercher une récolte..." 
            class="pl-11 pr-6 py-3 bg-white border border-gray-100 rounded-2xl text-sm focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all w-64 shadow-sm"
          >
        </div>
        <button
          @click="goToCreate"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg shadow-[#112830]/10 hover:shadow-[#10b481]/20"
        >
          <i class="bx bx-plus text-lg"></i> {{ t("btnyield") }}
        </button>
      </div>
    </div>

    <!-- PREMIUM TABLE -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden min-h-[400px]">
      <div class="overflow-x-auto scrollbar-hidden font-bold">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-gray-50">
              <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium">Date</th>
              <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium">Parcelle / Culture</th>
              <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-center">Surface (m²)</th>
              <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-center">Rendement</th>
              <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="y in paginatedYields" :key="y.id" class="group hover:bg-gray-50/50 transition-colors">
              <td class="px-8 py-6">
                <div class="flex items-center gap-2 text-gray-500 font-medium text-sm">
                  <i class="bx bx-calendar text-lg opacity-40"></i>
                  {{ formatDate(y.date) }}
                </div>
              </td>
              <td class="px-8 py-6">
                <div class="flex flex-col">
                  <span class="font-bold text-[#112830] tracking-tight">{{ y.parcel_name || "-" }}</span>
                  <span class="text-[10px] font-black uppercase tracking-widest text-[#10b481] italic">
                    {{ y.parcelCrop?.crop?.name || "-" }}
                  </span>
                </div>
              </td>
              <td class="px-8 py-6 text-center">
                <span class="inline-flex items-center px-3 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[10px] font-bold text-gray-500 uppercase tracking-tight">
                  <i class="bx bx-area mr-1 opacity-50"></i> {{ y.area }}
                </span>
              </td>
              <td class="px-8 py-6 text-center">
                <div class="inline-flex flex-col items-center">
                  <span class="text-lg font-black text-[#112830]">{{ y.yield_amount }}</span>
                  <span class="text-[8px] font-black uppercase tracking-widest text-gray-300">unités</span>
                </div>
              </td>
              <td class="px-8 py-6 text-right font-bold">
                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0 font-bold">
                  <button @click="goShow(y.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-[#10b481] hover:border-[#10b481]/20 transition-all shadow-sm">
                    <i class="bx bx-show text-lg"></i>
                  </button>
                  <button @click="goEdit(y.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-amber-500 hover:border-amber-500/20 transition-all shadow-sm">
                    <i class="bx bx-edit-alt text-lg font-bold"></i>
                  </button>
                  <button @click="deleteYield(y.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-rose-500 hover:border-rose-500/20 transition-all shadow-sm">
                    <i class="bx bx-trash text-lg font-bold"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedYields.length === 0">
              <td colspan="5" class="px-8 py-20 text-center">
                <div class="flex flex-col items-center gap-4 grayscale opacity-30">
                  <i class="bx bx-layer text-6xl"></i>
                  <p class="text-sm font-black uppercase tracking-widest font-bold">Aucune récolte enregistrée</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div class="px-8 py-8 flex items-center justify-between border-t border-gray-50 font-bold">
        <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">
          Page {{ currentPage }} sur {{ totalPages }}
        </p>
        <div class="flex items-center gap-2">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 border border-gray-100 text-gray-400 hover:text-[#112830] disabled:opacity-30 disabled:cursor-not-allowed transition-all font-bold"
          >
            <i class="bx bx-chevron-left text-xl"></i>
          </button>
          <div class="flex items-center gap-1 font-bold">
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page as number)"
              :class="['w-10 h-10 rounded-xl text-[10px] font-black transition-all border font-bold', currentPage === page ? 'bg-[#10b481] border-[#10b481] text-white shadow-lg shadow-[#10b481]/20' : 'bg-white border-gray-100 text-gray-400 hover:bg-gray-50']"
            >
              {{ page }}
            </button>
          </div>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 border border-gray-100 text-gray-400 hover:text-[#112830] disabled:opacity-30 disabled:cursor-not-allowed transition-all font-bold"
          >
            <i class="bx bx-chevron-right text-xl"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100 font-bold', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 font-bold', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1 font-bold">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">Confirmation du système</p>
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

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

// ===== STATE =====
const yields = ref<any[]>([]);
const searchQuery = ref("");
const currentPage = ref(1);
const perPage = 6;
const notification = ref({ visible: false, message: "", type: "success" as "success" | "error" });

const yieldsState = useState<{ data: any[]; timestamp: number }>("yieldsYieldsData", () => ({ data: [], timestamp: 0 }));

// ===== HELPERS =====
const showNotification = (message: string, type: "success" | "error" = "success") => {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
};

const formatDate = (date: string | number | Date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "short", day: "numeric" });
};

// ===== DATA FETCHING =====
const fetchYields = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  const now = Date.now();
  if (yieldsState.value.data.length && now - yieldsState.value.timestamp < 30 * 60 * 1000) {
    yields.value = yieldsState.value.data;
    return;
  }

  try {
    const rawData: any = await apiFetch('/api/yield-records/');
    const records = rawData?.results || rawData || [];

    yields.value = await Promise.all(records.map(async (y: any) => {
      if (y.parcelCrop) {
        try {
          const pc: any = await apiFetch(`/api/parcel-crops/${y.parcelCrop}/`);
          const p: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
          return { ...y, parcelCrop: pc, parcel_name: p.parcel_name };
        } catch { return y; }
      }
      return y;
    }));

    yieldsState.value = { data: yields.value, timestamp: Date.now() };
  } catch (err) {
    showNotification("Erreur lors du chargement des récoltes", "error");
  }
};

// ===== COMPUTED =====
const filteredYields = computed(() => {
  if (!searchQuery.value) return yields.value;
  const q = searchQuery.value.toLowerCase();
  return yields.value.filter(y => 
    y.parcel_name?.toLowerCase().includes(q) || 
    y.parcelCrop?.crop?.name?.toLowerCase().includes(q)
  );
});

const totalPages = computed(() => Math.ceil(filteredYields.value.length / perPage));
const paginatedYields = computed(() => {
  const start = (currentPage.value - 1) * perPage;
  return filteredYields.value.slice(start, start + perPage);
});

const visiblePages = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1));

// ===== ACTIONS =====
const goToCreate = () => router.push("/farmer/yield-records/create");
const goShow = (id: number) => router.push(`/farmer/yield-records/show/${id}`);
const goEdit = (id: number) => router.push(`/farmer/yield-records/edit/${id}`);

const deleteYield = async (id: number) => {
  if (!confirm("Voulez-vous vraiment supprimer cet enregistrement ?")) return;
  try {
    await apiFetch(`/api/yield-records/${id}/`, { method: "DELETE" });
    yields.value = yields.value.filter(y => y.id !== id);
    yieldsState.value.data = yields.value;
    showNotification("Récolte supprimée avec succès");
  } catch {
    showNotification("Erreur lors de la suppression", "error");
  }
};

const goToPage = (p: number) => currentPage.value = p;
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };

// ===== LIFECYCLE =====
onMounted(fetchYields);
watch(searchQuery, () => currentPage.value = 1);
</script>

<style scoped>
.scrollbar-hidden::-webkit-scrollbar { display: none; }
.scrollbar-hidden { -ms-overflow-style: none; scrollbar-width: none; }

.pop-notification-enter-active, .pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from, .pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>
