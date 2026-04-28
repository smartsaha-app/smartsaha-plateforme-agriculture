<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto text-[#112830]">
    <!-- ===== HEADER & BREADCRUMB ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-2">
        <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
          <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
            <i class="bx bx-home text-xs"></i> Home
          </NuxtLink>
          <i class="bx bx-chevron-right text-[8px]"></i>
          <span class="text-[#10b481]">Crops</span>
        </nav>
        <h1 class="text-3xl font-extrabold tracking-tight">Cultures & Variétés</h1>
        <p class="text-gray-500 font-medium">Gérez votre catalogue de cultures pour une traçabilité optimale.</p>
      </div>

      <div class="flex gap-3">
        <NuxtLink
          to="/farmer/crops/create"
          class="px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all duration-300 shadow-xl flex items-center gap-2 group"
        >
          <i class="bx bx-plus text-xl group-hover:scale-110 transition-transform"></i>
          Ajouter une culture
        </NuxtLink>
      </div>
    </div>

    <!-- ===== MAIN CONTENT CARD ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <!-- Loading State -->
      <div v-if="isLoading" class="p-32 text-center text-gray-300">
         <div class="w-16 h-16 border-4 border-t-[#10b481] border-gray-100 rounded-full animate-spin mx-auto mb-6"></div>
         <p class="font-bold uppercase tracking-widest text-xs">Chargement de votre catalogue...</p>
      </div>

      <!-- Table Content -->
      <div v-else-if="crops.length > 0" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="border-b border-gray-50">
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Nom de la Culture</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Variété</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Date de création</th>
              <th class="px-8 py-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50 text-sm">
            <tr v-for="crop in paginatedCrops" :key="crop.id" class="group hover:bg-gray-50/50 transition-colors">
              <td class="px-8 py-6">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center text-xl shadow-sm group-hover:scale-110 transition-transform">
                    <i class="bx bx-leaf"></i>
                  </div>
                  <span class="font-black text-[#112830] tracking-tight">{{ crop.name }}</span>
                </div>
              </td>
              <td class="px-8 py-6">
                <span class="px-3 py-1 bg-gray-50 rounded-lg text-xs font-bold text-gray-500">
                  {{ crop.variety?.name || "Variété standard" }}
                </span>
              </td>
              <td class="px-8 py-6 text-gray-400 font-medium lowercase">
                {{ new Date(crop.created_at).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }) }}
              </td>
              <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300">
                  <button
                    @click="editCrop(crop.id)"
                    class="w-10 h-10 rounded-xl bg-white border border-gray-100 text-[#10b481] flex items-center justify-center hover:bg-[#10b481] hover:text-white hover:-translate-y-1 transition-all shadow-sm"
                    title="Modifier"
                  >
                    <i class="bx bx-edit text-lg"></i>
                  </button>
                  <button
                    @click="deleteCrop(crop.id)"
                    class="w-10 h-10 rounded-xl bg-white border border-gray-100 text-rose-500 flex items-center justify-center hover:bg-rose-500 hover:text-white hover:-translate-y-1 transition-all shadow-sm"
                    title="Supprimer"
                  >
                    <i class="bx bx-trash text-lg"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-8 py-6 border-t border-gray-50 flex items-center justify-between">
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">
            Page {{ currentPage }} sur {{ totalPages }}
          </p>
          <div class="flex gap-2">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="w-10 h-10 rounded-xl bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-white hover:shadow-sm disabled:opacity-30 disabled:hover:bg-gray-50 transition-all"
            >
              <i class="bx bx-chevron-left text-xl"></i>
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page as number)"
              :class="['w-10 h-10 rounded-xl text-xs font-black transition-all', currentPage === page ? 'bg-[#112830] text-white shadow-lg' : 'bg-gray-50 text-gray-400 hover:bg-white hover:shadow-sm']"
            >
              {{ page }}
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="w-10 h-10 rounded-xl bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-white hover:shadow-sm disabled:opacity-30 disabled:hover:bg-gray-50 transition-all"
            >
              <i class="bx bx-chevron-right text-xl"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="p-32 text-center space-y-6">
        <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto">
          <i class="bx bx-leaf text-5xl text-gray-200"></i>
        </div>
        <div class="space-y-2">
          <h3 class="text-xl font-bold">Aucune culture enregistrée</h3>
          <p class="text-gray-400 max-w-xs mx-auto text-sm">Commencez par ajouter votre première culture pour alimenter vos historiques d'incidents et de récoltes.</p>
        </div>
        <NuxtLink
          to="/farmer/crops/create"
          class="inline-flex items-center gap-2 px-8 py-3 bg-[#10b481] text-white rounded-2xl font-bold hover:scale-105 transition-all shadow-lg"
        >
          <i class="bx bx-plus"></i> Créer maintenant
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const crops = ref<any[]>([]);
const isLoading = ref(true);

const itemsPerPage = 4;
const currentPage = ref(1);
const paginatedCrops = ref<any[]>([]);

const totalPages = computed(() => Math.ceil(crops.value.length / itemsPerPage));
const visiblePages = computed(() => {
  const pages = [];
  for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  return pages;
});

const updatePaginated = () => {
  const start = (currentPage.value - 1) * itemsPerPage;
  paginatedCrops.value = crops.value.slice(start, start + itemsPerPage);
};

watch([crops, currentPage], updatePaginated, { immediate: true });

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/crops/');
    crops.value = data?.results || data || [];
  } catch (err) {
    console.error("Failed to load crops:", err);
  } finally {
    isLoading.value = false;
  }
});

const deleteCrop = async (id: number) => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }

  if (!confirm("Are you sure you want to delete this crop?")) return;

  try {
    await apiFetch(`/api/crops/${id}/`, {
      method: "DELETE",
    });
    crops.value = crops.value.filter((c) => c.id !== id);
    updatePaginated();
    alert("Crop deleted successfully");
  } catch (err) {
    console.error(err);
    alert("Failed to delete crop");
  }
};

const editCrop = (id: number) => {
  router.push(`/farmer/crops/edit/${id}`);
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
const goToPage = (page: number) => {
  currentPage.value = page;
};
</script>
