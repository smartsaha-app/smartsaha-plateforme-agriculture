<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Membres & Groupes</h1>
        <p class="text-gray-500 font-medium">Gérez la structure de votre organisation et suivez l'activité des membres.</p>
      </div>
      <button @click="openCreateModal()" class="px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all duration-300 shadow-xl flex items-center gap-2 group">
        <i class="bx bx-plus text-xl group-hover:rotate-90 transition-transform"></i>
        Créer un nouveau groupe
      </button>
    </div>

    <!-- ===== STATS FAST VIEW ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in quickStats" :key="stat.label" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex items-center gap-4">
        <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-xl shadow-sm', stat.bg, stat.text]">
          <i :class="stat.icon"></i>
        </div>
        <div>
          <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ stat.label }}</p>
          <p class="text-2xl font-black text-[#112830]">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <!-- ===== SEARCH & FILTERS ===== -->
    <div class="bg-white p-4 rounded-3xl border border-gray-100 shadow-sm flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Rechercher un groupe..." 
          class="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all"
        />
      </div>
      <div class="flex gap-2">
        <select v-model="filterType" class="px-4 py-3 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-[#10b481]/20 outline-none cursor-pointer text-sm font-medium text-gray-600">
          <option value="all">Tous les types</option>
          <option v-for="t in groupTypes" :key="t.uuid" :value="t.uuid">{{ t.name }}</option>
        </select>
      </div>
    </div>

    <!-- ===== GROUPS GRID ===== -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-64 bg-gray-50 rounded-3xl animate-pulse"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="group in filteredGroups" :key="group.uuid" 
          class="group bg-white rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-500 overflow-hidden flex flex-col relative">

        <div class="p-8 space-y-4 flex-1">
          <!-- Header: icône + actions toujours visibles -->
          <div class="flex items-start justify-between">
            <div @click="viewDetails(group)" class="w-14 h-14 rounded-2xl bg-gray-50 flex items-center justify-center text-[#112830] group-hover:bg-[#10b481] group-hover:text-white transition-all duration-500 shadow-sm border border-gray-100 cursor-pointer">
              <i class="bx bx-group text-2xl"></i>
            </div>

            <!-- Boutons Edit / Delete toujours visibles -->
            <div class="flex items-center gap-2">
              <button @click.stop="openEditModal(group)" 
                      class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-blue-400 hover:bg-blue-500 hover:text-white transition-all duration-200 shadow-sm">
                <i class="bx bx-edit text-lg"></i>
              </button>
              <button @click.stop="confirmDelete(group)" 
                      class="w-8 h-8 rounded-lg bg-rose-50 flex items-center justify-center text-rose-400 hover:bg-rose-500 hover:text-white transition-all duration-200 shadow-sm">
                <i class="bx bx-trash text-lg"></i>
              </button>
            </div>
          </div>

          <!-- Badge type -->
          <div>
            <span class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest">
              {{ group.type?.name || 'Standard' }}
            </span>
          </div>

          <!-- Nom + description -->
          <div @click="viewDetails(group)" class="cursor-pointer">
            <h3 class="text-xl font-black text-[#112830] mb-1">{{ group.name }}</h3>
            <p class="text-sm text-gray-400 line-clamp-2">{{ group.description || 'Aucune description fournie.' }}</p>
          </div>

          <!-- Membres -->
          <div class="flex items-center gap-4 pt-2">
            <span class="text-xs font-bold text-gray-500">{{ group.active_members_count || 0 }} Membres</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-8 py-5 bg-gray-50/50 border-t border-gray-50 flex items-center justify-between">
          <div class="flex items-center gap-2 text-xs font-bold text-gray-400">
            <i class="bx bx-calendar"></i>
            <span>{{ new Date(group.created_at).toLocaleDateString() }}</span>
          </div>
          <button @click="viewDetails(group)" class="text-[#10b481] text-sm font-bold hover:underline flex items-center gap-1">
            Gérer <i class="bx bx-right-arrow-alt"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!isLoading && filteredGroups.length === 0" class="py-20 text-center space-y-4">
      <div class="w-24 h-24 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-folder-open text-5xl"></i>
      </div>
      <p class="text-gray-400 font-medium italic">Aucun groupe ne correspond à votre recherche.</p>
    </div>

    <!-- CRUD MODAL -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-md bg-black/20">
       <div class="bg-white w-full max-w-lg rounded-[2.5rem] p-10 shadow-2xl space-y-6 relative border border-white/20">
          <button @click="showModal = false" class="absolute top-6 right-6 w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors">
            <i class="bx bx-x text-2xl"></i>
          </button>
          
          <h2 class="text-2xl font-black text-[#112830]">{{ isEditing ? 'Modifier le Groupe' : 'Nouveau Groupe' }}</h2>
          
          <div class="space-y-4">
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Nom du groupe</label>
              <input v-model="formGroup.name" type="text" placeholder="Ex: Collecteurs Vakinankaratra" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium" />
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Type</label>
              <select v-model="formGroup.type_id" class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium">
                <option v-for="t in groupTypes" :key="t.uuid" :value="t.uuid">{{ t.name }}</option>
              </select>
            </div>
            <div class="space-y-1">
              <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Description</label>
              <textarea v-model="formGroup.description" placeholder="Brève description..." class="w-full p-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium h-24 resize-none"></textarea>
            </div>
          </div>
          
          <div class="flex gap-3 pt-4">
            <button @click="showModal = false" class="flex-1 py-4 text-gray-400 font-bold hover:text-gray-600 transition">Annuler</button>
            <button @click="saveGroup" class="flex-2 py-4 px-10 bg-[#112830] text-white rounded-2xl font-bold shadow-xl shadow-[#112830]/20 hover:bg-[#10b481] transition-all duration-300">
              {{ isEditing ? 'Enregistrer' : 'Créer le groupe' }}
            </button>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';

definePageMeta({ layout: 'dashboard' });

const router = useRouter();
const { apiFetch } = useApi();
const authStore = useAuthStore();

const isLoading = ref(true);
const showModal = ref(false);
const isEditing = ref(false);
const searchQuery = ref('');
const filterType = ref('all');

const groups = ref<any[]>([]);
const groupTypes = ref<any[]>([]);

const formGroup = ref({
  uuid: '',
  name: '',
  description: '',
  type_id: '',
  organisation_id: ''
});

const quickStats = computed(() => [
  { label: 'Total Groupes', value: groups.value.length.toString(), icon: 'bx bx-layer', bg: 'bg-emerald-50', text: 'text-emerald-600' },
  { label: 'Membres Actifs', value: groups.value.reduce((acc, g) => acc + (g.active_members_count || 0), 0).toString(), icon: 'bx bx-user-check', bg: 'bg-blue-50', text: 'text-blue-600' },
  { label: 'Statut', value: 'Opérationnel', icon: 'bx bx-check-shield', bg: 'bg-amber-50', text: 'text-amber-600' },
]);

const filteredGroups = computed(() => {
  let result = groups.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(g => 
      g.name.toLowerCase().includes(q) ||
      (g.description && g.description.toLowerCase().includes(q))
    );
  }
  if (filterType.value !== 'all') {
    result = result.filter(g => g.type?.uuid === filterType.value);
  }
  return result;
});

async function fetchGroups() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/groups/');
    groups.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchGroups:", err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchTypes() {
  try {
    const data: any = await apiFetch('/api/group-types/');
    groupTypes.value = data.results || data || [];
  } catch (err) {
    console.error("Erreur fetchTypes:", err);
  }
}

function openCreateModal() {
  isEditing.value = false;
  formGroup.value = { uuid: '', name: '', description: '', type_id: groupTypes.value[0]?.uuid || '', organisation_id: '' };
  showModal.value = true;
}

function openEditModal(group: any) {
  isEditing.value = true;
  formGroup.value = {
    uuid: group.uuid,
    name: group.name,
    description: group.description,
    type_id: group.type?.uuid,
    organisation_id: group.organisation?.uuid
  };
  showModal.value = true;
}

async function saveGroup() {
  try {
    // Obtenir l'organisation de l'utilisateur
    const userData: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    const orgId = userData.organisations_created?.[0]?.uuid;
    
    if (!orgId) {
      alert("Erreur: Organisation non trouvée.");
      return;
    }

    const payload = {
      name: formGroup.value.name,
      description: formGroup.value.description,
      type_id: formGroup.value.type_id,
      organisation_id: orgId
    };

    if (isEditing.value) {
      await apiFetch(`/api/groups/${formGroup.value.uuid}/`, {
        method: 'PATCH',
        body: payload
      });
    } else {
      await apiFetch('/api/groups/', {
        method: 'POST',
        body: payload
      });
    }
    
    showModal.value = false;
    fetchGroups();
  } catch (err) {
    console.error("Erreur saveGroup:", err);
    alert("Erreur lors de l'enregistrement du groupe.");
  }
}

async function confirmDelete(group: any) {
  if (confirm(`Êtes-vous sûr de vouloir supprimer le groupe "${group.name}" ?`)) {
    try {
      await apiFetch(`/api/groups/${group.uuid}/`, { method: 'DELETE' });
      fetchGroups();
    } catch (err) {
      console.error("Erreur deleteGroup:", err);
      alert("Erreur lors de la suppression.");
    }
  }
}

function viewDetails(group: any) {
  router.push(`/group/${group.uuid}`);
}

onMounted(() => {
  fetchGroups();
  fetchTypes();
});
</script>
