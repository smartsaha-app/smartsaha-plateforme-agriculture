<template>
  <div class="p-6 space-y-8 max-w-[1500px] mx-auto text-[#112830]">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight">Compte utilisateur</h1>
        <p class="text-gray-500 font-medium">Gérez ses comptes existant au sein du système</p>
      </div>
      <div class="flex gap-3">
        <button @click="showInviteModal = true" class="px-6 py-3 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all duration-300 shadow-xl flex items-center gap-2 group">
          <i class="bx bx-user-plus text-xl group-hover:scale-110 transition-transform"></i>
          Ajouter un superviseur
        </button>
      </div>
    </div>

    <!-- ===== SEARCH & ADVANCED FILTERS ===== -->
    <div class="bg-white p-6 rounded-[2.5rem] border border-gray-100 shadow-sm space-y-6">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1 relative">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Rechercher par nom" 
            class="w-full pl-12 pr-4 py-4 bg-gray-50 rounded-2xl border-none focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium"
          />
        </div>
        <div class="flex gap-2 p-1 bg-gray-50 rounded-2xl">
          <button v-for="t in filterTypes" :key="t.val" 
                  @click="selectedType = t.val"
                  :class="['px-5 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all', selectedType === t.val ? 'bg-white text-[#112830] shadow-sm' : 'text-gray-400 hover:text-gray-600']">
            {{ t.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- ===== USER TABLE PREMIUM ===== -->
    <div class="bg-white rounded-[3rem] border border-gray-100 shadow-sm overflow-hidden">
      <div v-if="isLoading" class="p-20 text-center text-gray-300">
         <i class="bx bx-loader-alt animate-spin text-5xl mb-4"></i>
         <p class="font-bold">Chargement de l'annuaire...</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="border-b border-gray-50">
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Utilisateur</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Rôle</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Date d'inscription</th>
              <th class="px-8 py-6 text-[10px] font-black text-gray-400 uppercase tracking-widest">Statut</th>
              <th class="px-8 py-6 text-right"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="user in filteredUsers" :key="user.uuid" class="group hover:bg-gray-50/50 transition-colors">
              <td class="px-8 py-6">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-[#112830] text-white flex items-center justify-center font-black shadow-lg shadow-[#112830]/10 overflow-hidden">
                    <img v-if="user.avatar" :src="user.avatar" alt="" class="w-full h-full object-cover">
                    <span v-else>{{ user.username.charAt(0).toUpperCase() }}</span>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <p class="font-black text-sm group-hover:text-[#10b481] transition-colors">{{ user.first_name }} {{ user.last_name }}</p>
                      <span v-if="user.is_staff" class="bx bxs-badge-check text-blue-500" title="System Staff"></span>
                    </div>
                    <p class="text-xs text-gray-400">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-8 py-6">
                <div class="flex items-center gap-2">
                   <span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-gray-100 text-gray-600">
                     {{ getRoleLabel(user.role) }}
                   </span>
                </div>
              </td>
              <td class="px-8 py-6">
                <div class="flex flex-col">
                  <span class="text-xs font-bold">{{ formatDate(user.date_joined, 'Date Inconnue') }}</span>
                </div>
              </td>
              <td class="px-8 py-6">
                <span :class="['px-3 py-1 rounded-xl text-[10px] font-black uppercase tracking-widest', user.is_active ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-500']">
                  {{ user.is_active ? 'Compte Actif' : 'Désactivé' }}
                </span>
              </td>
              <td class="px-8 py-6 text-right">
                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="toggleStaff(user)" :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-all shadow-sm border', user.is_staff ? 'bg-blue-50 border-blue-100 text-blue-500 hover:bg-blue-500 hover:text-white' : 'bg-gray-50 border-gray-100 text-gray-400 hover:bg-gray-500 hover:text-white']" title="Basculer Staff">
                    <i class="bx bx-shield-quarter text-lg"></i>
                  </button>
                  <button @click="toggleStatus(user)" :class="['w-10 h-10 rounded-xl flex items-center justify-center transition-all shadow-sm border', user.is_active ? 'bg-rose-50 border-rose-100 text-rose-500 hover:bg-rose-500 hover:text-white' : 'bg-emerald-50 border-emerald-100 text-emerald-500 hover:bg-emerald-500 hover:text-white']" :title="user.is_active ? 'Désactiver' : 'Activer'">
                    <i :class="user.is_active ? 'bx bx-block' : 'bx bx-check-double'" class="text-lg"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Footer -->
      <div v-if="!isLoading && totalCount > 20" class="px-8 pb-6 border-t border-gray-50 pt-4">
        <PaginationBase 
          :totalCount="totalCount" 
          :perPage="20" 
          v-model:currentPage="currentPage"
          @change-page="(p) => currentPage = p" 
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!isLoading && filteredUsers.length === 0" class="py-24 text-center space-y-4">
      <div class="w-32 h-32 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-100">
        <i class="bx bx-user-x text-6xl"></i>
      </div>
      <p class="text-gray-400 font-medium italic">Aucun utilisateur trouvé pour cette recherche.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import PaginationBase from '~/components/ui/PaginationBase.vue';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const isLoading = ref(true);
const searchQuery = ref('');
const selectedType = ref('all');
const users = ref<any[]>([]);
const totalCount = ref(0);
const currentPage = ref(1);

const filterTypes = [
  { label: 'Tous les comptes', val: 'all' },
  { label: 'Entreprises', val: 'org' },
  { label: 'Producteurs', val: 'farmer' },
  { label: 'Superviseurs', val: 'staff' },
];

const filteredUsers = computed(() => {
  let result = users.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(u => 
      u.username.toLowerCase().includes(q) || 
      u.email.toLowerCase().includes(q) ||
      (u.org && u.org.toLowerCase().includes(q))
    );
  }
  if (selectedType.value !== 'all') {
    if (selectedType.value === 'staff') result = result.filter(u => u.is_staff);
    if (selectedType.value === 'org') result = result.filter(u => u.org);
    if (selectedType.value === 'farmer') result = result.filter(u => !u.is_staff && !u.org);
  }
  return result;
});

function formatDate(dateString: string, fallback: string = 'N/A') {
  if (!dateString) return fallback;
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

async function fetchUsers() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch(`/api/users/?page=${currentPage.value}${searchQuery.value ? '&search=' + searchQuery.value : ''}`);
    
    console.log("data", data);
    
    // Adjust mapping based on backend structure
    const rawUsers = data.results || data || [];
    totalCount.value = data.count || rawUsers.length;
    users.value = rawUsers.map((u: any) => ({
      ...u,
      org: u.organisations_created?.length ? u.organisations_created[0].name : null,
      avatar: u.avatar || null
    }));
  } catch (err) {
    console.error("Erreur fetchUsers:", err);
  } finally {
    isLoading.value = false;
  }
}

async function toggleStatus(user: any) {
  const newStatus = !user.is_active;
  try {
    await apiFetch(`/api/users/${user.uuid}/`, {
      method: 'PATCH',
      body: { is_active: newStatus }
    });
    user.is_active = newStatus;
  } catch (err) {
    console.error("Erreur toggleStatus:", err);
    alert("Erreur lors de la mise à jour du statut.");
  }
}

async function toggleStaff(user: any) {
  const newStaff = !user.is_staff;
  try {
    await apiFetch(`/api/users/${user.uuid}/`, {
      method: 'PATCH',
      body: { is_staff: newStaff }
    });
    user.is_staff = newStaff;
  } catch (err) {
    console.error("Erreur toggleStaff:", err);
    alert("Erreur lors de la mise à jour des privilèges.");
  }
}

const showInviteModal = ref(false);

watch(currentPage, () => {
  fetchUsers();
});

watch(searchQuery, () => {
  currentPage.value = 1;
  fetchUsers();
});

onMounted(() => {
  fetchUsers();
});
</script>
