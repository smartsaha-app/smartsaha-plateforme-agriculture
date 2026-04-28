<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
      <i class="bx bx-task text-3xl text-[#10b481]"></i>
      Dashboard des Tâches
    </h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white shadow rounded-xl p-4 flex flex-col items-center">
        <i class="bx bx-hourglass text-3xl text-yellow-500 mb-2"></i>
        <span class="text-gray-500">En attente</span>
        <span class="text-xl font-bold">{{ summary.status.pending || 0 }}</span>
      </div>
      <div class="bg-white shadow rounded-xl p-4 flex flex-col items-center">
        <i class="bx bx-check-double text-3xl text-green-500 mb-2"></i>
        <span class="text-gray-500">Terminées</span>
        <span class="text-xl font-bold">{{
          summary.status.completed || 0
        }}</span>
      </div>
      <div class="bg-white shadow rounded-xl p-4 flex flex-col items-center">
        <i class="bx bx-error text-3xl text-red-500 mb-2"></i>
        <span class="text-gray-500">Haute priorité</span>
        <span class="text-xl font-bold">{{ summary.priority.high || 0 }}</span>
      </div>
      <div class="bg-white shadow rounded-xl p-4 flex flex-col items-center">
        <i class="bx bx-low-vision text-3xl text-blue-500 mb-2"></i>
        <span class="text-gray-500">Basse priorité</span>
        <span class="text-xl font-bold">{{ summary.priority.low || 0 }}</span>
      </div>
    </div>

    <div class="bg-white shadow rounded-xl overflow-hidden">
      <table class="min-w-full text-left">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2">#</th>
            <th class="px-4 py-2">Nom</th>
            <th class="px-4 py-2">Description</th>
            <th class="px-4 py-2">Échéance</th>
            <th class="px-4 py-2">Priorité</th>
            <th class="px-4 py-2">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(task, index) in tasks"
            :key="task.id"
            class="border-b hover:bg-gray-50 transition"
          >
            <td class="px-4 py-2">{{ index + 1 }}</td>
            <td class="px-4 py-2">{{ task.name }}</td>
            <td class="px-4 py-2">{{ task.description }}</td>
            <td class="px-4 py-2">{{ task.due_date }}</td>
            <td class="px-4 py-2">
              <span
                :class="{
                  'text-red-600 font-bold': task.priority === 3,
                  'text-yellow-500 font-semibold': task.priority === 2,
                  'text-green-500 font-medium': task.priority === 1,
                }"
              >
                {{ getPriorityText(task.priority) }}
              </span>
            </td>
            <td class="px-4 py-2">
              <span
                :class="{
                  'text-green-500 font-bold': task.status === 2,
                  'text-yellow-500 font-semibold': task.status === 1,
                  'text-gray-500': task.status === 0,
                }"
              >
                {{ getStatusText(task.status) }}
              </span>
            </td>
          </tr>
          <tr v-if="tasks.length === 0">
            <td colspan="6" class="text-center p-6 text-gray-500">
              Aucune tâche trouvée
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { API_URL } from "~/config";

const router = useRouter();

const tasks = ref<any[]>([]);
const summary = ref<any>({
  status: {},
  priority: {},
});

const getStatusText = (status: number) => {
  switch (status) {
    case 0:
      return "En attente";
    case 1:
      return "En cours";
    case 2:
      return "Terminée";
    default:
      return "-";
  }
};

const getPriorityText = (priority: number) => {
  switch (priority) {
    case 1:
      return "Basse";
    case 2:
      return "Moyenne";
    case 3:
      return "Haute";
    default:
      return "-";
  }
};

const updateSummary = (tasksData: any[]) => {
  summary.value.status = tasksData.reduce((acc: any, t) => {
    const s = getStatusText(t.status);
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, {});
  summary.value.priority = tasksData.reduce((acc: any, t) => {
    const p = getPriorityText(t.priority);
    acc[p.toLowerCase()] = (acc[p.toLowerCase()] || 0) + 1;
    return acc;
  }, {});
};

onMounted(async () => {
  const token = sessionStorage.getItem("token");

  if (!token) router.push("/login");
  try {
    const res = await fetch(`${API_URL}/api/tasks/dashboard/`, {
      headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) throw new Error("Erreur API");
    const data = await res.json();
    console.log("Dashboard task", data);

    tasks.value = Array.isArray(data) ? data : data.tasks || [];
    updateSummary(tasks.value);
  } catch (err) {
    console.error(err);
    alert("Impossible de charger les tâches.");
  }
});
</script>
