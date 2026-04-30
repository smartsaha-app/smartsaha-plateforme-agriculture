<template>
  <div class="p-6 space-y-8 text-[#112830] min-h-screen">
    
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481]">{{ t("parcels") }}</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">{{ t("parcels") }}</h1>
      </div>

      <div class="flex items-center gap-3">
        <!-- Export Dropdown -->
        <div class="relative group">
          <button class="flex items-center gap-2 px-6 py-3 bg-white border border-gray-100 rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-gray-50 transition-all shadow-sm">
            <i class="bx bx-export text-lg"></i>
            {{ t("export") }}
            <i class="bx bx-chevron-down text-[10px] opacity-40"></i>
          </button>
          <div class="absolute right-0 mt-2 w-40 bg-white rounded-2xl shadow-xl border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 overflow-hidden">
            <button @click="exportData('pdf')" class="w-full px-4 py-3 text-left text-xs font-black uppercase tracking-widest hover:bg-[#10b481]/10 hover:text-[#10b481] transition-colors flex items-center gap-3">
              <i class="bx bxs-file-pdf"></i> PDF
            </button>
            <button @click="exportData('csv')" class="w-full px-4 py-3 text-left text-xs font-black uppercase tracking-widest hover:bg-[#10b481]/10 hover:text-[#10b481] transition-colors flex items-center gap-3">
              <i class="bx bx-file"></i> CSV
            </button>
          </div>
        </div>

        <NuxtLink
          to="/farmer/parcels/create"
          class="flex items-center gap-2 px-8 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg hover:-translate-y-1"
        >
          <i class="bx bx-plus text-lg"></i>
          {{ t("addparcel") }}
        </NuxtLink>
      </div>
    </div>

    <!-- ===== TOOLBAR / FILTERS ===== -->
    <div class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm flex flex-col lg:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3 w-full lg:w-auto">
        <div class="relative flex-1 lg:w-80">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-300"></i>
          <input
            v-model="filters.parcel_name"
            type="text"
            :placeholder="t('filterbyparcel')"
            class="w-full pl-12 pr-4 py-3 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300 text-sm"
          />
        </div>
        <button
          @click="resetFilters"
          class="p-3 bg-gray-50 text-gray-400 hover:text-[#10b481] hover:bg-[#10b481]/10 rounded-2xl transition-all"
          title="Réinitialiser"
        >
          <i class="bx bx-refresh text-2xl"></i>
        </button>
      </div>

      <div class="flex items-center gap-4 text-xs font-black uppercase tracking-widest text-gray-400">
        <span>Afficher</span>
        <select
          v-model.number="rowsPerPage"
          @change="currentPage = 1"
          class="bg-gray-50 border-none rounded-xl px-4 py-2 focus:ring-2 focus:ring-[#10b481]/20 outline-none text-[#112830] font-bold"
        >
          <option :value="4">4</option>
          <option :value="8">8</option>
          <option :value="12">12</option>
        </select>
        <span>Par page</span>
      </div>
    </div>

    <!-- ===== PARCEL TABLE ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden min-h-[400px] flex flex-col relative">
      <div class="overflow-x-auto flex-1 h-full scrollbar-hidden">
        <table class="w-full text-left border-separate border-spacing-0">
          <thead>
            <tr class="bg-gray-50/50">
              <th class="px-10 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-100">{{ t("thparcelname") }}</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-100 hidden sm:table-cell">Coordonnées (Lat, Lng)</th>
              <th class="px-10 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest border-b border-gray-100 text-right">{{ t("thactions") }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <template v-if="isLoading">
              <!-- Loading indicators would go here if not using the overlay -->
            </template>
            <template v-else-if="paginatedFields.length > 0">
              <tr
                v-for="field in paginatedFields"
                :key="field.id"
                class="group hover:bg-emerald-50/30 transition-all"
              >
                <td class="px-10 py-7">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-[#112830] rounded-2xl flex items-center justify-center text-white text-xl shadow-lg group-hover:scale-110 transition-transform">
                      <i class="bx bx-map-alt"></i>
                    </div>
                    <div>
                      <NuxtLink :to="`/farmer/parcels/show/${field.fieldId}`" class="block font-bold text-[#112830] hover:text-[#10b481] transition-colors">
                        {{ field.parcel_name }}
                      </NuxtLink>
                      <span class="text-[10px] uppercase font-black text-gray-300 tracking-tighter">ID: {{ field.fieldId.slice(0,8) }}</span>
                    </div>
                  </div>
                </td>
                <td class="px-8 py-7 hidden sm:table-cell group">
                  <div class="flex items-center gap-2 font-mono text-xs text-gray-400 group-hover:text-gray-600 transition-colors">
                    <span class="px-2 py-1 bg-gray-50 rounded-lg">{{ formatCoord(field.latitude) }}</span>
                    <span class="opacity-30">,</span>
                    <span class="px-2 py-1 bg-gray-50 rounded-lg">{{ formatCoord(field.longitude) }}</span>
                  </div>
                </td>
                <td class="px-10 py-7 text-right">
                  <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all translate-x-4 group-hover:translate-x-0">
                    <NuxtLink
                      :to="`/farmer/parcels/show/${field.fieldId}`"
                      class="w-10 h-10 flex items-center justify-center bg-white rounded-xl shadow-sm text-gray-400 hover:text-[#10b481] hover:scale-110 transition-all border border-gray-50"
                      :title="t('show')"
                    >
                      <i class="bx bx-show text-xl"></i>
                    </NuxtLink>
                    <NuxtLink
                      :to="`/farmer/parcels/edit/${field.fieldId}`"
                      class="w-10 h-10 flex items-center justify-center bg-white rounded-xl shadow-sm text-gray-400 hover:text-amber-500 hover:scale-110 transition-all border border-gray-50"
                      :title="t('edit')"
                    >
                      <i class="bx bx-edit text-xl"></i>
                    </NuxtLink>
                    <button
                      @click="confirmDelete(field.fieldId)"
                      class="w-10 h-10 flex items-center justify-center bg-white rounded-xl shadow-sm text-gray-400 hover:text-rose-500 hover:scale-110 transition-all border border-gray-50"
                      :title="t('delete_confirm')"
                    >
                      <i class="bx bx-trash text-xl"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="3" class="px-10 py-20 text-center">
                <div class="flex flex-col items-center gap-4 text-gray-300">
                  <div class="w-20 h-20 bg-gray-50 rounded-[2rem] flex items-center justify-center text-5xl">
                    <i class="bx bx-landscape"></i>
                  </div>
                  <div class="space-y-1">
                    <p class="text-lg font-black text-[#112830] tracking-tighter">{{ t("noparcelsfound") }}</p>
                    <p class="text-xs font-medium max-w-xs mx-auto">Commencez par délimiter votre première parcelle sur la carte.</p>
                  </div>
                  <NuxtLink to="/farmer/parcels/create" class="mt-4 px-8 py-3 bg-[#10b481]/10 text-[#10b481] rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-[#10b481] hover:text-white transition-all">
                    Créer une parcelle
                  </NuxtLink>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div v-if="totalPages > 1" class="px-10 py-8 bg-gray-50/30 border-t border-gray-50 flex flex-col sm:flex-row items-center justify-between gap-6">
        <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest">Page {{ currentPage }} sur {{ totalPages }}</p>
        <div class="flex items-center gap-1">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="w-10 h-10 flex items-center justify-center rounded-xl bg-white border border-gray-100 text-gray-400 hover:text-[#10b481] disabled:opacity-20 transition-all shadow-sm"
          >
            <i class="bx bx-chevron-left text-2xl"></i>
          </button>
          
          <div class="flex items-center gap-1 px-2">
            <template v-for="page in visiblePages" :key="page">
              <button
                v-if="page !== '...'"
                @click="goToPage(page)"
                :class="[
                  'w-10 h-10 rounded-xl text-xs font-black transition-all',
                  currentPage === page
                    ? 'bg-[#112830] text-white shadow-lg scale-110'
                    : 'bg-white border border-gray-100 text-gray-400 hover:text-[#112830] hover:bg-gray-50 shadow-sm',
                ]"
              >
                {{ page }}
              </button>
              <span v-else class="px-2 text-gray-300 text-xs">...</span>
            </template>
          </div>

          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="w-10 h-10 flex items-center justify-center rounded-xl bg-white border border-gray-100 text-gray-400 hover:text-[#10b481] disabled:opacity-20 transition-all shadow-sm"
          >
            <i class="bx bx-chevron-right text-2xl"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- ===== OVERLAYS & MODALS ===== -->
    
    <!-- Delete Modal -->
    <Teleport to="body">
      <transition name="pop-notification">
        <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
          <div class="absolute inset-0 bg-[#112830]/80 backdrop-blur-sm" @click="cancelDelete"></div>
          <div class="bg-white rounded-[3rem] p-12 w-full max-w-sm text-center shadow-2xl relative z-10 border border-gray-100">
            <div class="w-24 h-24 bg-rose-50 rounded-[2.5rem] flex items-center justify-center mx-auto mb-8">
              <i class="bx bx-trash text-5xl text-rose-500"></i>
            </div>
            <h3 class="text-2xl font-black text-[#112830] tracking-tighter mb-4">{{ t("deleteParcel") }}</h3>
            <p class="text-gray-500 font-medium mb-10 text-sm leading-relaxed">{{ t("textConfirmDeleteParcel") }}</p>
            <div class="flex flex-col gap-3">
              <button @click="deleteParcelConfirmed" class="w-full py-4 bg-rose-500 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-rose-600 transition-all shadow-lg shadow-rose-500/20">
                Supprimer définitivement
              </button>
              <button @click="cancelDelete" class="w-full py-4 bg-gray-50 text-gray-400 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-gray-100 transition-all">
                Annuler
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Global Loader -->
    <Teleport to="body">
      <div v-if="isLoading" class="fixed inset-0 bg-[#112830]/60 backdrop-blur-[2px] flex flex-col items-center justify-center z-[110]">
        <div class="w-16 h-16 border-4 border-white/20 border-t-[#10b481] rounded-full animate-spin mb-4"></div>
        <p class="text-[10px] font-black uppercase tracking-[0.2em] text-white">Traitement...</p>
      </div>
    </Teleport>

    <!-- Notifications -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[120] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">Smartsaha Platform</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

// ===== INITIALISATION =====
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();

const t = (key: string) => nuxtT(`dashboard.${key}`);

definePageMeta({ layout: "dashboard" });

// ===== ÉTAT DE L'UI =====
const isLoading = ref(false);

const notification = reactive({
  visible: false,
  message: "",
  type: "success" as "success" | "error",
});

const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.message = message;
  notification.type = type;
  notification.visible = true;
  setTimeout(() => (notification.visible = false), duration);
};

// ===== EXPORT PDF / CSV =====
async function exportData(type: "pdf" | "csv") {
  const data = filteredFields.value.map((f) => ({
    Owner:      f.owner,
    FieldID:    f.fieldId,
    ParcelName: f.parcel_name,
    Latitude:   f.latitude,
    Longitude:  f.longitude,
  }));

  if (!data.length) return;

  if (type === "pdf") {
    if (process.client) {
      const { jsPDF } = await import("jspdf");
      const autoTableModule = await import("jspdf-autotable");
      const doc = new jsPDF();
      autoTableModule.default(doc, {
        head: [["Owner", "FieldID", "ParcelName", "Latitude", "Longitude"]],
        body: data.map(Object.values),
        startY: 20,
      });
      doc.save("parcels.pdf");
    }
  } else {
    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(","),
      ...data.map((row) =>
        headers.map((h) => `"${(row as Record<string, unknown>)[h]}"`).join(",")
      ),
    ];
    const blob = new Blob([csvRows.join("\n")], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "parcels.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// ===== FILTRES ET DONNÉES =====
const filters = reactive({
  owner: "",
  parcel_name: "",
});

const fields = ref<any[]>([]);
const rowsPerPage = ref(4);
const currentPage = ref(1);

function formatCoord(value: unknown): string {
  return typeof value === "number" ? value.toFixed(6) : "-";
}

// ===== CHARGEMENT DES DONNÉES =====
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    alert("Vous devez être connecté");
    return;
  }

  try {
    // ✅ FIX : suppression du .filter() — le backend filtre déjà par owner
    const data: any = await apiFetch('/api/parcels/');
    const records = data?.results || data || [];

    fields.value = records.map((parcel: any, idx: number) => ({
      id:          idx + 1,
      fieldId:     parcel.uuid,
      owner:       "Moi",
      parcel_name: parcel.parcel_name,
      latitude:    parcel.parcel_points?.[0]?.latitude ?? null,
      longitude:   parcel.parcel_points?.[0]?.longitude ?? null,
    }));
  } catch (err) {
    console.error("Erreur réseau:", err);
    showNotification("Erreur lors du chargement des parcelles", "error");
  }
});

// ===== COMPUTED =====
const filteredFields = computed(() =>
  fields.value.filter(
    (f) =>
      f.owner.toLowerCase().includes(filters.owner.toLowerCase()) &&
      f.parcel_name.toLowerCase().includes(filters.parcel_name.toLowerCase())
  )
);

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredFields.value.length / rowsPerPage.value))
);

const paginatedFields = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return filteredFields.value.slice(start, start + rowsPerPage.value);
});

const visiblePages = computed(() => {
  const pages: (number | string)[] = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 15) {
    for (let i = 1; i <= total; i++) pages.push(i);
  } else if (current <= 7) {
    pages.push(...Array.from({ length: 8 }, (_, i) => i + 1), "...", total);
  } else if (current >= total - 6) {
    pages.push(1, "...", ...Array.from({ length: 8 }, (_, i) => total - 7 + i));
  } else {
    pages.push(1, "...", current - 2, current - 1, current, current + 1, current + 2, "...", total);
  }
  return pages;
});

// ===== ACTIONS =====
function resetFilters() {
  filters.owner = "";
  filters.parcel_name = "";
  currentPage.value = 1;
}

const showDeleteModal = ref(false);
const parcelToDelete = ref<string | null>(null);

function confirmDelete(uuid: string) {
  parcelToDelete.value = uuid;
  showDeleteModal.value = true;
}

function cancelDelete() {
  showDeleteModal.value = false;
  parcelToDelete.value = null;
}

async function deleteParcelConfirmed() {
  if (!parcelToDelete.value) return;

  if (!authStore.isAuthenticated) {
    alert("Vous devez être connecté");
    return;
  }

  isLoading.value = true;

  try {
    await apiFetch(`/api/parcels/${parcelToDelete.value}/`, {
      method: "DELETE",
    });

    fields.value = fields.value.filter((f) => f.fieldId !== parcelToDelete.value);

    if (paginatedFields.value.length === 0 && currentPage.value > 1) {
      currentPage.value--;
    }

    showDeleteModal.value = false;
    parcelToDelete.value = null;
    showNotification("Parcel deleted successfully!", "success");

  } catch (err) {
    console.error(err);
    showNotification("Failed to delete parcel", "error");
  } finally {
    isLoading.value = false;
  }
}

// ===== PAGINATION =====
function prevPage() {
  if (currentPage.value > 1) currentPage.value--;
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++;
}

function goToPage(page: number | string) {
  if (typeof page === "number") currentPage.value = page;
}
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

.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>