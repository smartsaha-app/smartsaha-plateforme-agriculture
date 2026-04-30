<template>
  <div>
  <div class="mb-12">
    <div class="flex flex-col lg:flex-row gap-6">
      <div class="flex-1 grid grid-cols-1 gap-6">
        <div class="flex gap-6">
          <div
            class="flex-1 p-6 bg-white rounded-2xl shadow-md flex flex-col justify-center items-center border border-gray-100"
          >
            <h2
              class="text-gray-500 uppercase tracking-wide text-sm font-semibold mb-2"
            >
              {{ t("totalTask") }}
            </h2>
            <div class="text-5xl font-bold text-gray-800">
              {{ totalTasks }}
            </div>
            <div
              class="mt-6 w-2/3 h-1 bg-gray-200 rounded-full overflow-hidden"
            >
              <div
                class="h-full bg-[#10b481]"
                :style="{ width: tasksCompletedPercent + '%' }"
              ></div>
            </div>
            <p class="mt-2 text-sm text-gray-500">
              {{ t("completedtasks") }} : {{ tasksCompletedPercent }}%
            </p>
          </div>

          <div
            class="flex-1 p-6 bg-white rounded-2xl shadow-md flex flex-col border border-gray-100 justify-center"
          >
            <h2
              class="text-gray-500 uppercase tracking-wide text-sm font-semibold mb-6"
            >
              {{ t("taskByPriority") }}
            </h2>
            <ul class="space-y-2">
              <li
                v-for="(count, prio) in tasksByPriority"
                :key="prio"
                class="flex justify-between items-center"
              >
                <span class="text-gray-700 font-medium">{{
                  t(priorityKeyMap[prio])
                }}</span>
                <span class="font-semibold text-gray-900">{{ count }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="p-6 bg-white rounded-2xl shadow-md border border-gray-100">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-gray-800 text-sm font-semibold tracking-tight">
              {{ t("taskProgression") }}
            </h2>
            <span class="text-xs text-gray-400 font-medium">
              {{ Object.values(tasksByStatus).reduce((a, b) => a + b, 0) }} tâches
            </span>
          </div>

          <!-- Barre de progression segmentée -->
          <div class="w-full h-3 flex rounded-full overflow-hidden gap-0.5 mb-4">
            <div
              v-for="(count, statusId) in tasksByStatus"
              :key="statusId"
              :style="{
                width: getStatusPercent(count) + '%',
                backgroundColor: statusColors[statusId],
              }"
              class="relative transition-all duration-500 first:rounded-l-full last:rounded-r-full"
            />
          </div>

          <!-- Légende -->
          <div class="flex flex-wrap gap-x-4 gap-y-2">
            <div
              v-for="(count, statusId) in tasksByStatus"
              :key="statusId"
              class="flex items-center gap-1.5"
            >
              <span
                class="w-2 h-2 rounded-full shrink-0"
                :style="{ backgroundColor: statusColors[statusId] }"
              />
              <span class="text-xs text-gray-500">
                {{ t(statusKeyMap[statusNames[statusId]]) }}
              </span>
              <span class="text-xs font-semibold text-gray-800">{{ count }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Calendrier -->
      <div class="w-full lg:w-[350px] p-4 rounded-2xl shadow-md flex flex-col border border-gray-100 bg-white">
        <div class="flex justify-between items-center mb-3">
          <button @click="prevMonth" class="text-gray-500 hover:text-gray-900">
            <i class="bxr bx-chevron-left"></i>
          </button>
          <h3 class="text-lg font-semibold">{{ currentMonthYear }}</h3>
          <button @click="nextMonth" class="text-gray-500 hover:text-gray-900">
            <i class="bxr bx-chevron-right"></i>
          </button>
        </div>

        <div class="grid grid-cols-7 text-center text-gray-400 text-sm mb-2">
          <div v-for="d in weekDays" :key="d">{{ d }}</div>
        </div>

        <div class="grid grid-cols-7 gap-2">
          <div
            v-for="day in calendarDays"
            :key="day.dateKey"
            class="relative h-12 flex items-center justify-center rounded cursor-pointer hover:bg-gray-100 transition"
            @click="selectDay(day)"
          >
            <span
              :class="[
                'flex items-center justify-center w-8 h-8 rounded-full transition text-sm font-medium',
                day.events.length
                  ? priorities[day.events[0].priority] === 'High'
                    ? 'bg-[#e63946]/10 text-[#e63946] border border-[#e63946]/50e'
                    : priorities[day.events[0].priority] === 'Medium'
                    ? 'bg-[#f4a261]/10 text-[#f4a261] border border-[#f4a261]/50'
                    : 'bg-[#10b481]/10 text-[#10b481] border border-[#10b481]/50'
                  : 'text-gray-900',
                !day.isCurrentMonth && 'text-gray-400 opacity-50',
                isToday(day.date) && 'bg-gray-200 p-2 text-gray-900',
              ]"
            >
              {{ day.date.getDate() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <transition name="fade">
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm"
    >
      <div
        class="bg-white rounded shadow-md w-full max-w-lg p-6 relative border border-gray-200"
      >
        <button
          @click="closeModal"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-700 transition"
        >
          <i class="bxr bx-x text-xl"></i>
        </button>

        <h2 class="text-xl font-bold mb-6 text-gray-800">
          {{ t("tasks_for") }}
          <span class="text-[#10b481]">{{ formatDate(selectedDay) }}</span>
        </h2>

        <ul
          v-if="selectedEvents.length && !showAddForm"
          class="space-y-4 max-h-96 overflow-y-auto pr-2"
        >
          <li
            v-for="ev in selectedEvents"
            :key="ev.id"
            class="p-4 rounded shadow transition border border-gray-100"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="font-semibold text-gray-900 text-lg">
                  {{ ev.name }}
                </h3>
                <p class="text-gray-500 text-sm mt-1">{{ ev.description }}</p>
              </div>
              <span
                v-if="ev.completed_at"
                class="text-green-500 font-medium text-sm mt-1"
              >
                ✔ {{ t("done") }}
              </span>
            </div>

            <button
              v-if="!ev.completed_at"
              @click="markDone(ev)"
              class="mt-3 w-full text-white bg-[#10b481] transition py-2 rounded font-semibold shadow"
            >
              {{ t("markDone") }}
            </button>
          </li>
        </ul>

        <div
          v-if="selectedEvents.length && !showAddForm"
          class="mt-4 text-right"
        >
          <button
            @click="showAddForm = true"
            class="inline-flex items-center px-3 py-1 text-[#222831] bg-gray-100 rounded transition"
          >
            <i class="bx bx-plus mr-1"></i> {{ t("addtask") }}
          </button>
        </div>

        <div
          v-if="!selectedEvents.length || showAddForm"
          class="mt-4 space-y-5"
        >
          <div class="flex flex-col">
            <label class="text-gray-700 text-sm font-medium mb-1"
              >{{ t("taskname") }} *</label
            >
            <input
              v-model="newTask.name"
              type="text"
              placeholder="Enter task name"
              class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
            />
          </div>

          <div class="flex flex-col">
            <label class="text-gray-700 text-sm font-medium mb-1"
              >{{ t("desc") }} *</label
            >
            <textarea
              v-model="newTask.description"
              placeholder="Enter task description"
              rows="3"
              class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
            ></textarea>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1 flex flex-col hidden">
              <label class="text-gray-700 text-sm font-medium mb-1"
                >{{ t("due") }} *</label
              >
              <input
                v-model="newTask.due_date"
                type="date"
                class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
              />
            </div>

            <div class="flex-1 flex flex-col">
              <label class="text-gray-700 text-sm font-medium mb-1">{{
                t("priority")
              }}</label>
              <select
                v-model="newTask.priority"
                class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
              >
                <option v-for="p in priorities" :key="p.id" :value="p.id">
                  {{ t(priorityKeyMap[p.name]) }}
                </option>
              </select>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1 flex flex-col">
              <label class="text-gray-700 text-sm font-medium mb-1">{{
                t("status")
              }}</label>
              <select
                v-model="newTask.status"
                class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
              >
                <option v-for="s in statuses" :key="s.id" :value="s.id">
                  {{ t(statusKeyMap[s.name]) }}
                </option>
              </select>
            </div>

            <div class="flex-1 flex flex-col">
              <label class="text-gray-700 text-sm font-medium mb-1">{{
                t("parcelcrop")
              }}</label>
              <select
                v-model="newTask.parcelCrop"
                class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-[#10b481] focus:border-transparent transition"
              >
                <option v-for="c in parcelCrops" :key="c.id" :value="c.id">
                  {{ c.fullName }}
                </option>
              </select>
            </div>
          </div>

          <button
            @click="createTask"
            class="w-full py-3 rounded bg-[#10b481] text-white font-semibold hover:opacity-90 transition shadow-md"
          >
            {{ t("addtask") }}
          </button>
        </div>
      </div>
    </div>
  </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const showAddForm = ref(false);

interface Task {
  id: number;
  name: string;
  description: string;
  due_date: string;
  priority: number;
  completed_at?: string | null;
}
const tasksState = useState("tasksData", () => ({
  data: [] as any[],
  timestamp: 0,
}));

const tasks = ref<any[]>(tasksState.value.data);
const statusColors: Record<number, string> = {};
const statusNames: Record<number, string> = {};

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const today = new Date();
const currentYear = ref(today.getFullYear());
const currentMonth = ref(today.getMonth());

const weekDays = computed(() => [
  t("sun"),
  t("mon"),
  t("tue"),
  t("wed"),
  t("thu"),
  t("fri"),
  t("sat"),
]);

const currentMonthYear = computed(() => {
  const monthNames = [
    t("january"),
    t("february"),
    t("march"),
    t("april"),
    t("may"),
    t("june"),
    t("july"),
    t("august"),
    t("september"),
    t("october"),
    t("november"),
    t("december"),
  ];
  return `${monthNames[currentMonth.value]} ${currentYear.value}`;
});

const priorityKeyMap = {
  Low: "priorityLow",
  Medium: "priorityMedium",
  High: "priorityHigh",
};

const statusKeyMap = {
  Pending: "statusPending",
  "In Progress": "statusInProgress",
  Done: "statusDone",
  Cancelled: "statusCancelled",
};

function isToday(date: Date) {
  const now = new Date();
  return (
    date.getDate() === now.getDate() &&
    date.getMonth() === now.getMonth() &&
    date.getFullYear() === now.getFullYear()
  );
}

function formatDateISO(date: Date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

const loadTasks = async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  if (
    tasksState.value.data.length
  ) {
    tasks.value = tasksState.value.data;
    return;
  }

  try {
    const rawData: any = await apiFetch("/api/tasks/");
    tasks.value = rawData?.results || rawData || [];
  } catch (err) {
    console.error("Failed to load tasks:", err);
  }
};

const formattedTasks = computed(() => JSON.stringify(tasks.value, null, 2));

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1);
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
  const days: any[] = [];

  const prevDaysCount = firstDay.getDay();
  for (let i = prevDaysCount; i > 0; i--) {
    const date = new Date(currentYear.value, currentMonth.value, 1 - i);
    days.push({
      date,
      isCurrentMonth: false,
      dateKey: date.toDateString(),
      events: tasks.value.filter(
        (t) =>
          t.due_date === formatDateISO(date) && t.status !== 3 && t.status !== 4
      ),
    });
  }

  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(currentYear.value, currentMonth.value, i);
    days.push({
      date,
      isCurrentMonth: true,
      dateKey: date.toDateString(),
      events: tasks.value.filter(
        (t) =>
          t.due_date === formatDateISO(date) && t.status !== 3 && t.status !== 4
      ),
    });
  }

  let nextDate = 1;
  while (days.length % 7 !== 0) {
    const date = new Date(
      currentYear.value,
      currentMonth.value + 1,
      nextDate++
    );
    days.push({
      date,
      isCurrentMonth: false,
      dateKey: date.toDateString(),
      events: tasks.value.filter(
        (t) =>
          t.due_date === formatDateISO(date) && t.status !== 3 && t.status !== 4
      ),
    });
  }

  return days;
});

const showModal = ref(false);
const selectedDay = ref<Date | null>(null);
const selectedEvents = ref<Task[]>([]);

function selectDay(day: any) {
  const activeEvents = day.events.filter(
    (ev) => ev.status !== 3 && ev.status !== 4
  );
  selectedDay.value = day.date;
  if (activeEvents.length) {
    selectedEvents.value = activeEvents;
  } else {
    selectedEvents.value = [];
  }
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedEvents.value = [];
  selectedDay.value = null;
}

function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11;
    currentYear.value--;
  } else currentMonth.value--;
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else currentMonth.value++;
}

function formatDate(date: Date | null) {
  if (!date) return "";
  const weekday = `weekday_${date.getDay()}`;
  const month = `month_${date.getMonth()}`;
  return `${t(weekday)} ${date.getDate()} ${t(month)} ${date.getFullYear()}`;
}

async function markDone(task: Task) {
  if (!authStore.isAuthenticated) return router.push("/login");
  try {
    await apiFetch(`/api/tasks/${task.id}/mark_done/`, {
      method: "POST",
      body: task,
    });
    task.completed_at = new Date().toISOString();
  } catch (err) {
    console.error("Failed to mark done:", err);
  }
}

const newTask = ref({
  name: "",
  description: "",
  due_date: "",
  parcelCrop: null,
  priority: null,
  status: null,
});

const priorities = ref<any[]>([]);
const statuses = ref<any[]>([]);
const parcelCrops = ref<any[]>([]);

const prioritiesJson = computed(() =>
  JSON.stringify(priorities.value, null, 2)
);

onMounted(async () => {
  if (!authStore.isAuthenticated) return router.push("/login");

  try {
    const priorityData: any = await apiFetch("/api/task-priority/");
    priorities.value = priorityData?.results || priorityData || [];

    const statusData: any = await apiFetch("/api/task-status/");
    statuses.value = statusData?.results || statusData || [];

    statuses.value.forEach((s) => {
      statusNames[s.id] = s.name;
      switch (s.name) {
        case "Pending":
          statusColors[s.id] = "#f4a261";
          break;
        case "In Progress":
          statusColors[s.id] = "#219ebc";
          break;
        case "Done":
          statusColors[s.id] = "#10b481";
          break;
        case "Cancelled":
          statusColors[s.id] = "#9ca3af";
          break;
        default:
          statusColors[s.id] = "#9ca3af";
      }
    });

    const rawCropsData: any = await apiFetch("/api/parcel-crops/");
    const cropsData: any[] = rawCropsData?.results || rawCropsData || [];

    const enrichedCrops = await Promise.all(
      cropsData.map(async (pc: any) => {
        try {
          const parcelData: any = await apiFetch(`/api/parcels/${pc.parcel}/`);
          return {
            ...pc,
            fullName: `${parcelData.parcel_name} - ${pc.crop.name}`,
          };
        } catch (err) {
          console.error("Erreur fetch parcel:", err);
          return { ...pc, fullName: `${pc.crop.name}` };
        }
      })
    );
    parcelCrops.value = enrichedCrops;
  } catch (err) {
    console.error("Erreur lors du chargement des options:", err);
  }
});

watch(selectedDay, (day) => {
  if (day) newTask.value.due_date = formatDateISO(day);
});

async function createTask() {
  if (!authStore.isAuthenticated) return router.push("/login");

  if (
    !newTask.value.name ||
    !newTask.value.description ||
    !newTask.value.due_date ||
    !newTask.value.priority ||
    !newTask.value.status
  ) {
    alert("Please fill in all required fields");
    return;
  }

  try {
    const created: any = await apiFetch("/api/tasks/", {
      method: "POST",
      body: newTask.value,
    });
    tasks.value.push(created);
    selectedEvents.value.push(created);

    newTask.value = {
      name: "",
      description: "",
      due_date: formatDateISO(selectedDay.value!),
      parcelCrop: null,
      priority: null,
      status: null,
    };
  } catch (err) {
    console.error("Failed to create task:", err);
  }
}

onMounted(loadTasks);

const totalTasks = computed(() => tasks.value.length);

const tasksByPriority = computed(() => {
  const stats: Record<string, number> = {};
  priorities.value.forEach((p) => {
    stats[p.name] = tasks.value.filter((t) => t.priority === p.id).length;
  });
  return stats;
});

const tasksCompletedPercent = computed(() => {
  if (tasks.value.length === 0) return 0;
  const done = tasks.value.filter((t) => t.completed_at).length;
  return Math.round((done / tasks.value.length) * 100);
});

const tasksByStatus = computed(() => {
  const counts: Record<number, number> = {};
  statuses.value.forEach((s) => (counts[s.id] = 0));

  tasks.value.forEach((t) => {
    if (statusNames[t.status] !== undefined) {
      counts[t.status]++;
    }
  });
  return counts;
});

function getStatusPercent(count: number) {
  if (!tasks.value.length) return 0;
  return (count / tasks.value.length) * 100;
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.grid > div span {
  transition: transform 0.2s, background-color 0.2s;
}
.grid > div:hover span {
  transform: scale(1.1);
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
