<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Cultures & Variétés">
      <template #subtitle>
        <i class="bx bx-leaf"></i>
        Gérez votre catalogue de cultures pour une traçabilité optimale.
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Cultures</span>
      </template>
    </PageHeader>

    <!-- ===== TOOLBAR ===== -->
    <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
      <!-- Search -->
      <div class="relative flex-1 max-w-sm">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
        <input
          v-model="search"
          type="text"
          placeholder="Rechercher une culture..."
          class="w-full pl-11 pr-4 py-2.5 bg-white border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830] shadow-sm"
        />
        <button v-if="search" @click="search = ''" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x text-lg"></i>
        </button>
      </div>

      <!-- Count + Add button -->
      <div class="flex items-center gap-3">
        <span class="text-xs font-bold text-gray-400">
          {{ filteredCrops.length }} culture{{ filteredCrops.length !== 1 ? 's' : '' }}
        </span>
        <NuxtLink
          to="/farmer/crops/create"
          class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm"
        >
          <i class="bx bx-plus text-base"></i>
          Ajouter une culture
        </NuxtLink>
      </div>
    </div>

    <!-- ===== TABLE CARD ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">

      <!-- Loading -->
      <div v-if="isLoading" class="py-24 flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-3 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">Chargement...</p>
      </div>

      <!-- Table -->
      <div v-else-if="filteredCrops.length > 0" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50/70 border-b border-gray-100">
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Culture</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Variété</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest hidden sm:table-cell">Ajoutée le</th>
              <th class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr
              v-for="crop in paginatedCrops"
              :key="crop.id"
              class="hover:bg-gray-50/50 transition-colors group"
            >
              <!-- Name -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-xl bg-emerald-50 text-[#10b481] flex items-center justify-center flex-shrink-0 group-hover:bg-[#10b481] group-hover:text-white transition-colors">
                    <i class="bx bx-leaf text-base"></i>
                  </div>
                  <span class="font-black text-[#112830] text-sm">{{ crop.name }}</span>
                </div>
              </td>

              <!-- Variety -->
              <td class="px-6 py-4">
                <span class="inline-flex items-center gap-1 px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[10px] font-bold text-gray-500 uppercase tracking-wide">
                  <i class="bx bx-category text-xs"></i>
                  {{ crop.variety?.name || 'Standard' }}
                </span>
              </td>

              <!-- Date -->
              <td class="px-6 py-4 hidden sm:table-cell">
                <span class="text-xs font-medium text-gray-400">
                  {{ new Date(crop.created_at).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }) }}
                </span>
              </td>

              <!-- Actions — always visible -->
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="editCrop(crop.id)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-500 hover:bg-[#112830] hover:text-white hover:border-[#112830] transition-all text-xs font-bold"
                    title="Modifier"
                  >
                    <i class="bx bx-edit text-sm"></i>
                  </button>
                  <button
                    @click="openDeleteModal(crop)"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100 text-gray-400 hover:bg-rose-50 hover:text-rose-500 hover:border-rose-100 transition-all text-xs font-bold"
                    title="Supprimer"
                  >
                    <i class="bx bx-trash text-sm"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-50 flex items-center justify-between">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
            Page {{ currentPage }} / {{ totalPages }}
          </p>
          <div class="flex gap-1.5">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="w-9 h-9 rounded-lg bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-[#112830] hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-left text-lg"></i>
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page as number)"
              :class="[
                'w-9 h-9 rounded-lg text-xs font-black transition-all',
                currentPage === page ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100'
              ]"
            >
              {{ page }}
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="w-9 h-9 rounded-lg bg-gray-50 text-gray-400 flex items-center justify-center hover:bg-[#112830] hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
            >
              <i class="bx bx-chevron-right text-lg"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="py-24 flex flex-col items-center gap-5 text-center">
        <div class="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center">
          <i class="bx bx-leaf text-4xl text-gray-200"></i>
        </div>
        <div>
          <h3 class="text-base font-black text-[#112830] mb-1">
            {{ search ? 'Aucun résultat pour "' + search + '"' : 'Aucune culture enregistrée' }}
          </h3>
          <p class="text-sm text-gray-400 max-w-xs mx-auto">
            {{ search ? 'Essayez un autre terme de recherche.' : 'Commencez par ajouter votre première culture.' }}
          </p>
        </div>
        <NuxtLink
          v-if="!search"
          to="/farmer/crops/create"
          class="flex items-center gap-2 px-5 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm"
        >
          <i class="bx bx-plus"></i>
          Créer maintenant
        </NuxtLink>
      </div>
    </div>

    <!-- ===== DELETE MODAL ===== -->
    <div v-if="cropToDelete" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div class="w-14 h-14 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto">
            <i class="bx bx-trash text-2xl text-rose-500"></i>
          </div>
          <div>
            <h2 class="text-lg font-black text-[#112830]">Supprimer cette culture ?</h2>
            <p class="text-sm text-gray-400 mt-1">
              "<span class="font-bold text-[#112830]">{{ cropToDelete.name }}</span>" sera définitivement supprimée.
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button
            @click="cropToDelete = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors"
          >
            Annuler
          </button>
          <button
            @click="confirmDelete"
            :disabled="isDeleting"
            class="flex-1 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <div v-if="isDeleting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-trash"></i>
            Supprimer
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'dashboard' });

import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useApi } from '~/composables/useApi';

const router    = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const crops     = ref<any[]>([]);
const isLoading = ref(true);
const search    = ref('');

// Delete modal
const cropToDelete = ref<any>(null);
const isDeleting   = ref(false);

// Pagination
const itemsPerPage = 8;
const currentPage  = ref(1);

const filteredCrops = computed(() => {
  if (!search.value) return crops.value;
  const q = search.value.toLowerCase();
  return crops.value.filter(c =>
    c.name?.toLowerCase().includes(q) ||
    c.variety?.name?.toLowerCase().includes(q)
  );
});

const totalPages = computed(() => Math.ceil(filteredCrops.value.length / itemsPerPage));

const paginatedCrops = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredCrops.value.slice(start, start + itemsPerPage);
});

const visiblePages = computed(() => {
  const pages = [];
  for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  return pages;
});

watch(search, () => { currentPage.value = 1; });

onMounted(async () => {
  if (!authStore.isAuthenticated) { router.push('/login'); return; }
  try {
    const data: any = await apiFetch('/api/crops/');
    crops.value = data?.results || data || [];
  } catch (err) {
    console.error('Failed to load crops:', err);
  } finally {
    isLoading.value = false;
  }
});

function editCrop(id: number) {
  router.push(`/farmer/crops/edit/${id}`);
}

function openDeleteModal(crop: any) {
  cropToDelete.value = crop;
}

async function confirmDelete() {
  if (!cropToDelete.value) return;
  isDeleting.value = true;
  try {
    await apiFetch(`/api/crops/${cropToDelete.value.id}/`, { method: 'DELETE' });
    crops.value = crops.value.filter(c => c.id !== cropToDelete.value.id);
    cropToDelete.value = null;
  } catch (err) {
    console.error(err);
  } finally {
    isDeleting.value = false;
  }
}

function nextPage() { if (currentPage.value < totalPages.value) currentPage.value++; }
function prevPage() { if (currentPage.value > 1) currentPage.value--; }
function goToPage(page: number) { currentPage.value = page; }
</script>