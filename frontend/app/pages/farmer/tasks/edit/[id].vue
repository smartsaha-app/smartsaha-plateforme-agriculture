<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="space-y-2">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
          <i class="bx bx-home text-xs"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/tasks" class="hover:text-[#10b481] transition-colors">Tâches</NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481]">Modifier la Tâche</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Édition de Mission</h1>
    </div>

    <div v-if="initialLoading" class="min-h-[400px] flex flex-col items-center justify-center gap-4 text-gray-400">
      <div class="w-12 h-12 border-4 border-t-[#10b481] border-gray-100 rounded-full animate-spin"></div>
      <p class="text-[10px] font-black uppercase tracking-widest">Chargement des données...</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-2">
        <form @submit.prevent="submitTask" class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12 space-y-10">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-bold">
            <!-- Task Name -->
            <div class="space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("taskname") }} *</label>
              <div class="relative group">
                <i class="bx bx-task absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <input 
                  v-model="form.name"
                  type="text" 
                  required
                  placeholder="Nom de la tâche"
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all placeholder:text-gray-300"
                >
              </div>
            </div>

            <!-- Due Date -->
            <div class="space-y-3">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("due") }} *</label>
              <div class="relative group">
                <i class="bx bx-calendar-event absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <input 
                  v-model="form.due_date"
                  type="date" 
                  required
                  class="w-full pl-14 pr-6 py-4 bg-gray-50 border border-gray-50 rounded-2xl focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all text-[#112830]"
                >
              </div>
            </div>

            <!-- Description -->
            <div class="md:col-span-2 space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("desc") }} *</label>
              <div class="relative group">
                <i class="bx bx-align-left absolute left-5 top-6 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <textarea 
                  v-model="form.description"
                  required
                  placeholder="Détails de la mission..."
                  class="w-full pl-14 pr-6 py-5 bg-gray-50 border border-gray-50 rounded-[2rem] focus:bg-white focus:border-[#10b481]/30 focus:ring-4 focus:ring-[#10b481]/5 outline-none transition-all min-h-[120px] resize-none placeholder:text-gray-300"
                ></textarea>
              </div>
            </div>

            <!-- Parcel Crop Selection -->
            <div class="space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("parcelcrop") }} *</label>
              <div class="relative group">
                <i class="bx bx-link-alt absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <select 
                  v-model="form.parcelCrop" 
                  required
                  class="w-full pl-14 pr-10 py-4 bg-gray-50 border border-gray-50 rounded-2xl appearance-none focus:bg-white focus:border-[#10b481]/30 outline-none transition-all font-bold"
                >
                  <option :value="null" disabled>{{ t("select_parcel_crop") }}</option>
                  <option v-for="pc in parcelCrops" :key="pc.id" :value="pc.id">{{ pc.label }}</option>
                </select>
                <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
              </div>
            </div>

            <!-- Priority Selection -->
            <div class="space-y-3 font-bold">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("priority") }} *</label>
              <div class="relative group">
                <i class="bx bx-flag absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
                <select 
                  v-model="form.priority" 
                  required
                  class="w-full pl-14 pr-10 py-4 bg-gray-50 border border-gray-50 rounded-2xl appearance-none focus:bg-white focus:border-[#10b481]/30 outline-none transition-all font-bold"
                >
                  <option :value="null" disabled>{{ t("select_priority") }}</option>
                  <option v-for="p in taskPriorities" :key="p.id" :value="p.id">{{ t(priorityKeyMap[p.name] ?? p.name) }}</option>
                </select>
                <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
              </div>
            </div>

            <!-- Status Choice -->
             <div class="md:col-span-2 space-y-4">
               <label class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 px-1">{{ t("status") }}</label>
               <div class="grid grid-cols-2 md:grid-cols-4 gap-3 font-bold">
                 <button 
                  v-for="s in taskStatuses" 
                  :key="s.id"
                  type="button"
                  @click="form.status = s.id"
                  :class="['px-4 py-3 rounded-xl border text-[10px] font-black uppercase tracking-widest transition-all', form.status === s.id ? 'bg-[#112830] border-[#112830] text-emerald-400 scale-[1.02] shadow-lg shadow-[#112830]/10' : 'bg-white border-gray-100 text-gray-400 hover:border-[#10b481]/30 hover:text-[#10b481]']"
                 >
                   {{ t(statusKeyMap[s.name] ?? s.name) }}
                 </button>
               </div>
             </div>
          </div>

          <!-- Actions -->
          <div class="flex flex-col md:flex-row items-center justify-end gap-4 pt-6">
            <NuxtLink to="/farmer/tasks" class="w-full md:w-auto px-8 py-4 text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-[#112830] transition-colors text-center font-bold">
              {{ t("cancel") }}
            </NuxtLink>
            <button 
              type="submit" 
              :disabled="isLoading"
              class="w-full md:w-auto px-10 py-4 bg-[#112830] text-white rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] hover:bg-[#10b481] transition-all shadow-xl shadow-[#112830]/10 disabled:opacity-50 flex items-center justify-center gap-3"
            >
              <div v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin font-bold"></div>
              <span>Enregistrer les modifications</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Preview Sidebar -->
      <div class="space-y-6">
        <div class="bg-gray-50 rounded-[3rem] p-10 border border-gray-100 space-y-8">
           <div class="w-16 h-16 rounded-2xl bg-white flex items-center justify-center text-3xl text-[#10b481] shadow-sm font-bold">
            <i class="bx bx-history"></i>
          </div>
          <div class="space-y-4">
             <h3 class="text-xl font-black tracking-tight tracking-tighter">Historique Tâche</h3>
             <div class="space-y-4 font-bold">
               <div class="flex items-center gap-3 text-xs">
                 <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                 <span class="text-gray-400">Date de création :</span>
                 <span class="text-[#112830]">{{ formatDate(taskRaw.created_at) }}</span>
               </div>
               <div class="flex items-center gap-3 text-xs">
                 <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                 <span class="text-gray-400">Dernière modification :</span>
                 <span class="text-[#112830]">{{ formatDate(taskRaw.updated_at) }}</span>
               </div>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Notification system -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500 font-bold']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1 font-bold">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <span class="text-[10px] font-medium text-gray-400 uppercase tracking-widest">Confirmation</span>
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

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const priorityKeyMap: Record<string, string> = { Low: "priorityLow", Medium: "priorityMedium", High: "priorityHigh" };
const statusKeyMap: Record<string, string> = { Pending: "statusPending", "In Progress": "statusInProgress", Done: "statusDone", Cancelled: "statusCancelled" };

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const id = route.params.id as string;

// ===== STATE =====
const isLoading = ref(false);
const initialLoading = ref(true);
const taskRaw = ref<any>({});
const taskPriorities = ref<any[]>([]);
const taskStatuses = ref<any[]>([]);
const parcelCrops = ref<any[]>([]);
const notification = ref({ visible: false, message: "", type: "success" as "success" | "error" });

const form = ref({
  name: "",
  description: "",
  due_date: "",
  parcelCrop: null as number | null,
  priority: null as number | null,
  status: null as number | null,
});

// ===== HELPERS =====
const showNotification = (message: string, type: "success" | "error" = "success") => {
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
    const [data, priData, staData, cropData]: [any, any, any, any] = await Promise.all([
      apiFetch(`/api/tasks/${id}/`),
      apiFetch('/api/task-priority/'),
      apiFetch('/api/task-status/'),
      apiFetch('/api/parcel-crops/'),
    ]);

    taskRaw.value = data;
    form.value = {
      name: data.name,
      description: data.description,
      due_date: data.due_date,
      parcelCrop: data.parcelCrop,
      priority: data.priority,
      status: data.status,
    };

    taskPriorities.value = (priData as any)?.results || priData || [];
    taskStatuses.value = (staData as any)?.results || staData || [];
    const parcelCropsRaw = (cropData as any)?.results || cropData || [];

    parcelCrops.value = await Promise.all(
      parcelCropsRaw.map(async (pc: any) => {
        try {
          const p: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
          return { ...pc, label: `${p.parcel_name} - ${pc.crop.name}` };
        } catch { return { ...pc, label: pc.crop.name }; }
      })
    );
  } catch (err) {
    showNotification(t("error_load_data"), "error");
  } finally {
    initialLoading.value = false;
  }
});

// ===== SOUMISSION =====
const submitTask = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");
  isLoading.value = true;
  try {
    await apiFetch(`/api/tasks/${id}/`, { method: "PUT", body: form.value });
    showNotification("Mission mise à jour avec succès !", "success");
    setTimeout(() => router.push({ path: "/farmer/tasks", query: { refresh: "1" } }), 2000);
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
