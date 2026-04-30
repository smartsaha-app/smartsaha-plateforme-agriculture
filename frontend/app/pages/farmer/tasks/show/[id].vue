<template>
  <div class="p-6 space-y-8 text-[#112830]">
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1 font-bold">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <NuxtLink to="/farmer/tasks" class="hover:text-[#10b481] transition-colors font-bold">Tâches</NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481] font-bold italic">Détails de la Tâche</span>
        </nav>
        <h1 class="text-4xl font-black tracking-tighter">Détails de Mission</h1>
      </div>

      <div class="flex items-center gap-3 font-bold">
        <button @click="goBack" class="p-3 bg-white border border-gray-100 rounded-2xl text-gray-400 hover:text-[#10b481] transition-all shadow-sm">
          <i class="bx bx-arrow-back text-xl"></i>
        </button>
        <button
          @click="editTask"
          class="flex items-center gap-2 px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold text-xs uppercase tracking-widest hover:bg-[#10b481] transition-all shadow-lg"
        >
          <i class="bx bx-edit-alt text-lg"></i> {{ t("edit") }}
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- MAIN CONTENT -->
      <div class="lg:col-span-2 space-y-8">
        <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm p-8 md:p-12 space-y-10 font-bold">
          <!-- Title & Description -->
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center text-2xl shadow-sm">
                <i class="bx bx-task font-bold"></i>
              </div>
              <h2 class="text-3xl font-black tracking-tight text-[#112830]">{{ task.name }}</h2>
            </div>
            <p class="text-gray-500 leading-relaxed font-bold">{{ task.description || "Aucune description fournie pour cette tâche." }}</p>
          </div>

          <!-- Status Tracker -->
          <div class="space-y-6 pt-6 border-t border-gray-50 font-bold">
             <div class="flex items-center justify-between font-bold">
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">Progression de la tâche</p>
                <span :class="['px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border font-bold', statusClasses(statusName)]">
                  {{ t(statusKeyMap[statusName] ?? statusName) }}
                </span>
             </div>
             <div class="w-full h-3 bg-gray-50 rounded-full overflow-hidden font-bold">
                <div 
                  class="h-full bg-[#10b481] transition-all duration-1000 shadow-[0_0_15px_rgba(16,180,129,0.3)] font-bold" 
                  :style="{ width: getStatusProgress(statusName) + '%' }"
                ></div>
             </div>
             <div class="grid grid-cols-4 text-[8px] font-black uppercase tracking-widest text-gray-300 font-bold">
               <span>Prévu</span>
               <span class="text-center">En cours</span>
               <span class="text-center font-bold">Réalisé</span>
               <span class="text-right">Terminé</span>
             </div>
          </div>

          <!-- Metadata Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 font-bold">
            <div class="p-6 bg-gray-50 rounded-[2rem] border border-gray-50 font-bold">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Culture / Parcelle Associée</p>
              <div class="flex items-center gap-3 text-[#112830] font-bold">
                <i class="bx bx-link-alt text-xl text-[#10b481]"></i>
                <span class="font-bold text-lg tracking-tight">{{ task.parcelCropFull || "Non spécifié" }}</span>
              </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-[2rem] border border-gray-50">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">Priorité de Mission</p>
              <div class="flex items-center gap-3 font-bold">
                <span :class="['w-3 h-3 rounded-full font-bold', priorityDotClass(priorityName)]"></span>
                <span class="font-bold text-lg tracking-tight">{{ t(priorityKeyMap[priorityName] ?? priorityName) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SIDEBAR / TIME METRICS -->
      <div class="space-y-8 font-bold text-bold">
        <div class="bg-[#112830] rounded-[3rem] p-8 text-white relative overflow-hidden group shadow-2xl font-bold">
           <div class="absolute -right-10 -top-10 w-40 h-40 bg-[#10b481] opacity-10 rounded-full filter blur-3xl group-hover:opacity-20 transition-opacity font-bold"></div>
           
           <div class="relative space-y-8 font-bold">
              <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-3xl text-rose-400 font-bold">
                <i class="bx bx-time-five font-bold"></i>
              </div>

              <div class="space-y-1 font-bold">
                <p class="text-[10px] font-black uppercase tracking-widest text-gray-400">Échéance</p>
                <p class="text-3xl font-black tracking-tighter text-rose-400">{{ formatDate(task.due_date) }}</p>
                <p class="text-xs text-gray-500 font-bold italic">{{ timeRemaining }}</p>
              </div>

              <div class="pt-6 border-t border-white/5 space-y-4 font-bold">
                <div class="flex items-center justify-between text-xs font-bold">
                  <span class="text-gray-400">Créé le</span>
                  <span class="font-bold font-bold">{{ formatDate(task.created_at) }}</span>
                </div>
                <div class="flex items-center justify-between text-xs font-bold">
                  <span class="text-gray-400">MàJ le</span>
                  <span class="font-bold">{{ formatDate(task.updated_at) }}</span>
                </div>
                <div v-if="task.completed_at" class="flex items-center justify-between text-xs font-bold">
                  <span class="text-emerald-400">Terminé le</span>
                  <span class="font-bold text-emerald-400">{{ formatDate(task.completed_at) }}</span>
                </div>
              </div>
           </div>
        </div>

        <div class="bg-gray-50 rounded-[2rem] p-8 space-y-6 border border-gray-100 font-bold">
           <h3 class="text-[10px] font-black uppercase tracking-widest text-gray-400 tracking-[0.2em] font-bold">Tags</h3>
           <div class="flex flex-wrap gap-2">
             <span class="px-4 py-2 bg-white border border-gray-200 rounded-xl text-[10px] font-black uppercase tracking-widest text-gray-500 shadow-sm font-bold">Agriculture</span>
             <span class="px-4 py-2 bg-white border border-gray-200 rounded-xl text-[10px] font-black uppercase tracking-widest text-gray-500 shadow-sm font-bold">Saison 2024</span>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const priorityKeyMap = { Low: "priorityLow", Medium: "priorityMedium", High: "priorityHigh" };
const statusKeyMap = { Pending: "statusPending", "In Progress": "statusInProgress", Done: "statusDone", Canceled: "statusCancelled" };

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const id = route.params.id as string;

const task = ref<any>({});
const priorityName = ref<string>("");
const statusName = ref<string>("");

onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  try {
    const data: any = await apiFetch(`/api/tasks/${id}/`);
    task.value = data;

    if (task.value.parcelCrop) {
      try {
        const pc: any = await apiFetch(`/api/parcel-crops/${task.value.parcelCrop}/`);
        const p: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
        task.value.parcelCropFull = `${p.parcel_name} - ${pc.crop.name}`;
      } catch { task.value.parcelCropFull = "-"; }
    }

    if (task.value.priority) {
      const p: any = await apiFetch(`/api/task-priority/${task.value.priority}/`);
      priorityName.value = p.name;
    }

    if (task.value.status) {
      const s: any = await apiFetch(`/api/task-status/${task.value.status}/`);
      statusName.value = s.name;
    }
  } catch (err) {}
});

const getStatusProgress = (status: string) => {
  const steps: Record<string, number> = { "Pending": 20, "In Progress": 50, "Done": 100, "Canceled": 100 };
  return steps[status] || 0;
};

const statusClasses = (status: string) => {
  if (status === "Done") return "bg-emerald-50 text-emerald-600 border-emerald-100";
  if (status === "In Progress") return "bg-sky-50 text-sky-600 border-sky-100";
  if (status === "Pending") return "bg-amber-50 text-amber-600 border-amber-100";
  return "bg-gray-50 text-gray-500 border-gray-100";
};

const priorityDotClass = (p: string) => {
  if (p === "High") return "bg-rose-500";
  if (p === "Medium") return "bg-amber-500";
  return "bg-[#10b481]";
};

const timeRemaining = computed(() => {
  if (!task.value.due_date) return "";
  const diff = new Date(task.value.due_date).getTime() - new Date().getTime();
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  return days > 0 ? `Il reste environ ${days} jours` : "L'échéance est passée";
});

const formatDate = (date: string | null) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString(locale.value, { year: "numeric", month: "long", day: "numeric" });
};

const goBack = () => router.push("/farmer/tasks");
const editTask = () => router.push(`/farmer/tasks/edit/${id}`);
</script>
