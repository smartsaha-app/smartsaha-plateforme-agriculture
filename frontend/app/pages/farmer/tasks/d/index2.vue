<template>
  <div class="mt-10 w-[300px] h-[300px]">
    <h3 class="text-xl font-bold mb-4">{{ t("upcomingTasksCalendar") }}</h3>

    <client-only>
      <VueCal
  :events="calendarEvents"
  default-view="['month']"
  :hide-title-bar="true"
  :hide-view-selector="true"  
  :hide-week-numbers="true"
  style="height: 100%; width: 100%;"
  class="rounded-2xl shadow-lg border border-gray-200 compact-calendar"
  :on-day-click="handleDayClick"
/>

    </client-only>

    <!-- Modal -->
    <transition name="fade">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      >
        <div
          class="bg-white rounded-2xl shadow-xl w-11/12 max-w-md p-6 relative"
        >
          <button
            @click="closeModal"
            class="absolute top-3 right-3 text-gray-500 hover:text-gray-900"
          >
            ✕
          </button>
          <h2 class="text-lg font-bold mb-4">
            Tasks for {{ formatDate(selectedDay) }}
          </h2>
          <ul class="space-y-3 max-h-96 overflow-y-auto">
            <li
              v-for="event in selectedEvents"
              :key="event.title"
              class="p-3 border rounded-lg shadow-sm hover:shadow-md transition"
            >
              <h3 class="font-semibold">{{ event.title }}</h3>
              <p class="text-gray-600 text-sm">{{ event.content }}</p>
            </li>
          </ul>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import VueCal from "vue-cal";
import "vue-cal/dist/vuecal.css";
import { ref, computed } from "vue";
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const tasks = ref([
  {
    id: 1,
    name: "Task 1",
    due_date: "2025-11-21",
    parcelCropFull: "Parcel A - Corn",
    status: "Pending",
  },
  {
    id: 2,
    name: "Task 2",
    due_date: "2025-11-23",
    parcelCropFull: "Parcel B - Rice",
    status: "In Progress",
  },
]);

const calendarEvents = computed(() =>
  tasks.value
    .map((task) => {
      if (!task.due_date) return null;
      const date = new Date(task.due_date);
      if (isNaN(date.getTime())) return null;
      return {
        start: date,
        end: date,
        title: task.name,
        content: `${task.parcelCropFull} - ${task.status}`,
        allDay: true,
      };
    })
    .filter(Boolean)
);

const showModal = ref(false);
const selectedEvents = ref<any[]>([]);
const selectedDay = ref<Date | null>(null);

function handleDayClick(day: Date) {
  const eventsOfDay = calendarEvents.value.filter((ev) => {
    const evDate = new Date(ev.start);
    return evDate.toDateString() === day.toDateString();
  });
  if (eventsOfDay.length > 0) {
    selectedEvents.value = eventsOfDay;
    selectedDay.value = day;
    showModal.value = true;
  }
}

function closeModal() {
  showModal.value = false;
  selectedEvents.value = [];
  selectedDay.value = null;
}

function formatDate(date: Date | null) {
  if (!date) return "";
  return date.toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
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

.compact-calendar {
  --vc-primary: #10b481;
  --vc-bg: #ffffff;
  --vc-border: #e5e7eb;
  font-family: "Inter", sans-serif;
  font-size: 0.75rem;
}

.vuecal__cell {
  position: relative;
}

.vuecal__event {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10b481;
  position: absolute;
  top: 4px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0;
}
</style>
