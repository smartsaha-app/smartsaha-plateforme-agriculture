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
          <span class="text-[#10b481] italic">Tasks</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">{{ t("titiletaskslist") }}</h1>
      </div>

      <div class="flex items-center gap-3">
        <div class="relative group hidden md:block">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-[#10b481] transition-colors"></i>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Rechercher une tâche..." 
            class="pl-11 pr-6 py-3 bg-white border border-gray-100 rounded-2xl text-sm focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all w-64 shadow-sm"
          >
        </div>
        <NuxtLink
          to="/farmer/tasks/create"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg shadow-[#112830]/10 hover:shadow-[#10b481]/20"
        >
          <i class="bx bx-plus text-lg"></i> {{ t("btnaddtask") }}
        </NuxtLink>
      </div>
    </div>

    <!-- ===== CALENDAR SECTION ===== -->
    <div class="overflow-hidden p-2">
       <TaskCalendar />
    </div>

    <!-- ===== TABS & CONTENT ===== -->
    <div class="space-y-6">
      <div class="flex items-center gap-8 border-b border-gray-100 px-4">
        <button
          @click="activeTab = 'historique'"
          :class="['pb-4 text-[10px] font-black uppercase tracking-widest transition-all relative', activeTab === 'historique' ? 'text-[#10b481]' : 'text-gray-400 hover:text-[#112830]']"
        >
          Historique
          <div v-if="activeTab === 'historique'" class="absolute bottom-0 left-0 w-full h-0.5 bg-[#10b481] rounded-full"></div>
        </button>
        <button
          @click="activeTab = 'upcoming'"
          :class="['pb-4 text-[10px] font-black uppercase tracking-widest transition-all relative', activeTab === 'upcoming' ? 'text-[#10b481]' : 'text-gray-400 hover:text-[#112830]']"
        >
          À venir
          <div v-if="activeTab === 'upcoming'" class="absolute bottom-0 left-0 w-full h-0.5 bg-[#10b481] rounded-full"></div>
        </button>
      </div>

      <!-- PREMIUM TABLE -->
      <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden min-h-[400px]">
        <div class="overflow-x-auto scrollbar-hidden">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-gray-50">
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium">Tâche</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium">Échéance</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium">Culture / Parcelle</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-center">Priorité</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-center">Statut</th>
                <th class="px-8 py-6 text-[10px] font-black uppercase tracking-widest text-gray-400 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="task in paginatedTasks" :key="task.id" class="group hover:bg-gray-50/50 transition-colors">
                <td class="px-8 py-6 font-bold text-[#112830]">{{ task.name }}</td>
                <td class="px-8 py-6">
                  <div class="flex items-center gap-2 text-gray-500 font-medium text-sm">
                    <i class="bx bx-calendar text-lg opacity-40"></i>
                    {{ formatDate(task.due_date) }}
                  </div>
                </td>
                <td class="px-8 py-6">
                  <span class="inline-flex items-center gap-2 px-3 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[10px] font-bold text-gray-500 uppercase tracking-tight">
                    <i class="bx bx-link-alt"></i> {{ task.parcelCropFull || "-" }}
                  </span>
                </td>
                <td class="px-8 py-6 text-center">
                  <span v-if="taskPriorities[task.priority]" :class="['px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border', priorityClasses(taskPriorities[task.priority])]">
                    {{ t(priorityKeyMap[taskPriorities[task.priority]]) }}
                  </span>
                </td>
                <td class="px-8 py-6 text-center">
                  <span v-if="taskStatuses[task.status]" :class="['px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border', statusClasses(taskStatuses[task.status])]">
                    {{ t(statusKeyMap[taskStatuses[task.status]]) }}
                  </span>
                </td>
                <td class="px-8 py-6 text-right">
                  <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all translate-x-2 group-hover:translate-x-0">
                    <button @click="showTask(task.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-[#10b481] hover:border-[#10b481]/20 transition-all shadow-sm">
                      <i class="bx bx-show text-lg"></i>
                    </button>
                    <button @click="editTask(task.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-amber-500 hover:border-amber-500/20 transition-all shadow-sm">
                      <i class="bx bx-edit-alt text-lg"></i>
                    </button>
                    <button @click="deleteTask(task.id)" class="p-2 bg-white border border-gray-100 rounded-xl text-gray-400 hover:text-rose-500 hover:border-rose-500/20 transition-all shadow-sm">
                      <i class="bx bx-trash text-lg"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedTasks.length === 0">
                <td colspan="6" class="px-8 py-20 text-center">
                  <div class="flex flex-col items-center gap-4 grayscale opacity-30">
                    <i class="bx bx-task text-6xl"></i>
                    <p class="text-sm font-black uppercase tracking-widest">{{ t("notaskfound") }}</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- PAGINATION -->
        <div class="px-8 py-8 flex items-center justify-between border-t border-gray-50">
          <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">
            Page {{ currentPage }} sur {{ totalPages }}
          </p>
          <div class="flex items-center gap-2">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 border border-gray-100 text-gray-400 hover:text-[#112830] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-left text-xl"></i>
            </button>
            <div class="flex items-center gap-1">
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="['w-10 h-10 rounded-xl text-[10px] font-black transition-all border', currentPage === page ? 'bg-[#10b481] border-[#10b481] text-white shadow-lg shadow-[#10b481]/20' : 'bg-white border-gray-100 text-gray-400 hover:bg-gray-50']"
              >
                {{ page }}
              </button>
            </div>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-50 border border-gray-100 text-gray-400 hover:text-[#112830] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-right text-xl"></i>
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
import TaskCalendar from "~/components/features/tasks/TaskCalendar.vue";

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const priorityKeyMap = { Low: "priorityLow", Medium: "priorityMedium", High: "priorityHigh" };
const statusKeyMap = { Pending: "statusPending", "In Progress": "statusInProgress", Done: "statusDone", Cancelled: "statusCancelled" };

// ===== STATE =====
const tasks = ref<any[]>([]);
const taskPriorities = ref<Record<number, string>>({});
const taskStatuses = ref<Record<number, string>>({});
const searchQuery = ref("");
const activeTab = ref<"historique" | "upcoming">("historique");
const itemsPerPage = 6;
const currentPage = ref(1);
const paginatedTasks = ref<any[]>([]);
const notification = ref({ visible: false, message: "", type: "success" as "success" | "error" });

const showNotification = (message: string, type: "success" | "error" = "success") => {
  notification.value = { visible: true, message, type };
  setTimeout(() => notification.value.visible = false, 3000);
};

// ===== DATA LOADING =====
const loadLookups = async () => {
  try {
    const [pData, sData]: [any, any] = await Promise.all([
      apiFetch('/api/task-priority/'),
      apiFetch('/api/task-status/'),
    ]);
    taskPriorities.value = Object.fromEntries((pData?.results || pData || []).map((p: any) => [p.id, p.name]));
    taskStatuses.value = Object.fromEntries((sData?.results || sData || []).map((s: any) => [s.id, s.name]));
  } catch (err) {}
};

const fetchTasks = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  try {
    const rawData: any = await apiFetch('/api/tasks/');
    const results = rawData?.results || rawData || [];
    
    // Detailed data enrichment
    tasks.value = await Promise.all(results.map(async (task: any) => {
      if (task.parcelCrop) {
        try {
          const pc: any = await apiFetch(`/api/parcel-crops/${task.parcelCrop}/`);
          const p: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
          return { ...task, parcelCropFull: `${p.parcel_name} - ${pc.crop.name}` };
        } catch { return { ...task, parcelCropFull: "-" }; }
      }
      return { ...task, parcelCropFull: "-" };
    }));
    updatePaginated();
  } catch (err) {
    showNotification(t("error_load_data"), "error");
  }
};

// ===== COMPUTED & HELPERS =====
const filteredTasks = computed(() => {
  let list = tasks.value;
  if (activeTab.value === "upcoming") {
    const now = new Date();
    list = list.filter(t => new Date(t.due_date) >= now && taskStatuses.value[t.status] !== "Done");
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(t => t.name.toLowerCase().includes(q) || t.parcelCropFull.toLowerCase().includes(q));
  }
  return list;
});

const totalPages = computed(() => Math.ceil(filteredTasks.value.length / itemsPerPage));
const visiblePages = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1));

const updatePaginated = () => {
  const start = (currentPage.value - 1) * itemsPerPage;
  paginatedTasks.value = filteredTasks.value.slice(start, start + itemsPerPage);
};

const priorityClasses = (name: string) => {
  if (name === "High") return "bg-rose-50 text-rose-600 border-rose-100";
  if (name === "Medium") return "bg-amber-50 text-amber-600 border-amber-100";
  return "bg-emerald-50 text-emerald-600 border-emerald-100";
};

const statusClasses = (name: string) => {
  if (name === "Pending") return "bg-amber-50 text-amber-600 border-amber-100";
  if (name === "In Progress") return "bg-sky-50 text-sky-600 border-sky-100";
  if (name === "Done") return "bg-emerald-50 text-emerald-600 border-emerald-100";
  return "bg-gray-50 text-gray-500 border-gray-100";
};

// ===== ACTIONS =====
const deleteTask = async (id: number) => {
  if (!confirm("Voulez-vous vraiment supprimer cette tâche ?")) return;
  try {
    await apiFetch(`/api/tasks/${id}/`, { method: "DELETE" });
    tasks.value = tasks.value.filter(t => t.id !== id);
    updatePaginated();
    showNotification("Tâche supprimée avec succès");
  } catch {
    showNotification("Erreur lors de la suppression", "error");
  }
};

const editTask = (id: number) => router.push(`/farmer/tasks/edit/${id}`);
const showTask = (id: number) => router.push(`/farmer/tasks/show/${id}`);
const prevPage = () => { if (currentPage.value > 1) currentPage.value--; };
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++; };
const goToPage = (p: number) => currentPage.value = p;

const formatDate = (date: string | null) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "short", day: "numeric" });
};

// ===== LIFECYCLE =====
onMounted(async () => {
  await loadLookups();
  await fetchTasks();
});

watch([activeTab, searchQuery, tasks], () => { currentPage.value = 1; updatePaginated(); });
watch(currentPage, updatePaginated);
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
