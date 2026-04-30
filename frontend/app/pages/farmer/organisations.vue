<template>
  <div class="p-6 space-y-8 max-w-[1400px] mx-auto">
    <!-- ===== HEADER ===== -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div>
        <h1 class="text-3xl font-extrabold text-[#112830]">Découverte des Organisations</h1>
        <p class="text-gray-500 font-medium">Trouvez une organisation ou un groupe à rejoindre pour bénéficier d'un accompagnement.</p>
      </div>
    </div>

    <!-- ===== SEARCH & FILTERS ===== -->
    <!-- <div class="bg-white p-4 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col md:flex-row gap-4">
      <div class="flex-1 relative">
        <i class="bx bx-search absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 text-xl"></i>
        <input v-model="searchQuery" type="text" placeholder="Rechercher une organisation ou un groupe..." 
               class="w-full pl-14 pr-6 py-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium" />
      </div>
      <div class="w-full md:w-64 relative">
        <i class="bx bx-filter-alt absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 text-xl"></i>
        <select v-model="membershipFilter" class="w-full pl-14 pr-6 py-4 bg-gray-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/30 transition-all font-medium appearance-none">
          <option value="all">Tous les groupes</option>
          <option value="member">Déjà membre</option>
          <option value="non-member">Pas encore membre</option>
        </select>
      </div>
      <button @click="fetchOrganisations" class="px-8 py-4 bg-[#112830] text-white rounded-2xl font-bold hover:bg-[#10b481] transition-all shadow-lg hover:shadow-[#10b481]/20">
        Rechercher
      </button>
    </div> -->

    <!-- ===== ORGANISATION LIST ===== -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 space-y-4">
       <div class="w-12 h-12 border-4 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
       <p class="text-gray-400 font-bold animate-pulse">Chargement des organisations...</p>
    </div>

    <div v-else-if="groups.length === 0" class="bg-white p-20 rounded-[3rem] text-center border border-dashed border-gray-200">
       <i class="bx bx-buildings text-6xl text-gray-200 mb-4"></i>
       <h3 class="text-xl font-bold text-gray-400">Aucune organisation trouvée</h3>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="group in groups" :key="group.uuid" 
           class="group bg-white rounded-[3rem] border border-gray-100 shadow-sm hover:shadow-2xl transition-all duration-500 overflow-hidden flex flex-col relative">
        
        <!-- Header Image/Pattern -->
        <div class="h-32 bg-gradient-to-br from-[#112830] to-[#10b481] relative overflow-hidden">
           <div class="absolute inset-0 opacity-10 flex items-center justify-center pointer-events-none">
              <i class="bx bx-buildings text-[120px]"></i>
           </div>
           <div class="absolute -bottom-8 left-8 w-20 h-20 rounded-3xl bg-white shadow-xl flex items-center justify-center text-3xl font-black text-[#112830] border-4 border-white">
              {{ group.organisation?.name?.[0]?.toUpperCase() || 'O' }}
           </div>
        </div>

        <div class="p-8 pt-12 space-y-6 flex-1 flex flex-col">
          <div>
            <div class="flex items-center gap-2 mb-2">
               <span class="px-3 py-1 bg-emerald-50 text-[#10b481] rounded-full text-[10px] font-black uppercase tracking-widest">
                  {{ group.type?.name || 'Groupe' }}
               </span>
               <span v-if="group.membershipStatus === 'MEMBER'" class="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-[9px] font-black uppercase tracking-widest border border-blue-100 flex items-center gap-1">
                  <i class="bx bx-check-double"></i> Membre
               </span>
               <span v-else-if="group.membershipStatus === 'PENDING'" class="px-3 py-1 bg-amber-50 text-amber-600 rounded-full text-[9px] font-black uppercase tracking-widest border border-amber-100 flex items-center gap-1">
                  <i class="bx bx-time"></i> En attente
               </span>
               <span v-else class="px-3 py-1 bg-gray-50 text-gray-400 rounded-full text-[9px] font-black uppercase tracking-widest border border-gray-100">
                  Disponible
               </span>
            </div>
            <h3 class="text-2xl font-black text-[#112830] group-hover:text-[#10b481] transition-colors line-clamp-1">
              {{ group.name }}
            </h3>
            <p class="text-sm text-gray-400 font-bold">
              {{ group.organisation?.name }}
            </p>
          </div>

          <p class="text-gray-500 text-sm leading-relaxed line-clamp-3 min-h-[4.5rem]">
            {{ group.description || 'Ce groupe travaille sur l\'amélioration des rendements et le partage de bonnes pratiques de culture.' }}
          </p>

          <div class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl">
             <div class="flex flex-col">
                <span class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Membres</span>
                <span class="text-sm font-black text-[#112830]">{{ group.active_members_count }} actifs</span>
             </div>
             <div class="w-px h-8 bg-gray-200"></div>
             <div class="flex flex-col text-right">
                <span class="text-[9px] font-black text-gray-400 uppercase tracking-widest">Zone</span>
                <span class="text-sm font-black text-[#112830] truncate max-w-[120px]">{{ group.organisation?.address || 'Antsirabe' }}</span>
             </div>
          </div>

          <div class="mt-auto pt-4">
             <button @click="requestToJoin(group)" 
                     :disabled="group.membershipStatus !== 'NONE'"
                     class="w-full py-4 rounded-2xl font-black text-sm uppercase tracking-widest transition-all flex items-center justify-center gap-2 group/btn"
                     :class="group.membershipStatus !== 'NONE' 
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200' 
                        : 'bg-[#112830] text-white hover:bg-[#10b481] shadow-xl shadow-[#112830]/10 hover:shadow-[#10b481]/20'">
               <i :class="group.membershipStatus === 'PENDING' ? 'bx bx-time' : (group.membershipStatus === 'MEMBER' ? 'bx bx-check-circle' : 'bx bx-user-plus')" class="text-lg"></i>
               {{ group.membershipStatus === 'PENDING' ? 'Demande envoyée' : (group.membershipStatus === 'MEMBER' ? 'Déjà membre' : 'Rejoindre le groupe') }}
             </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const authStore = useAuthStore();
const searchQuery = ref('');
const membershipFilter = ref('all');
const isLoading = ref(true);
const groups = ref<any[]>([]);

async function fetchOrganisations() {
  isLoading.value = true;
  try {
    const data = await apiFetch(`/api/groups/?discovery=true&search=${searchQuery.value}`);
    const allGroups = (data as any).results || data || [];
    
    const myMemberships = await apiFetch('/api/member-groups/');
    const membershipsList = ((myMemberships as any).results || myMemberships || []);

    groups.value = allGroups.map((g: any) => {
      const membership = membershipsList.find((m: any) => m.group.uuid === g.uuid);
      let status = 'NONE';
      if (membership) {
        status = membership.status === 'ACTIVE' ? 'MEMBER' : 'PENDING';
      }
      return { ...g, membershipStatus: status };
    }).filter((g: any) => {
      if (membershipFilter.value === 'all') return true;
      if (membershipFilter.value === 'member') return g.membershipStatus === 'MEMBER';
      if (membershipFilter.value === 'non-member') return g.membershipStatus === 'NONE';
      return true;
    });

  } catch (err) {
    console.error("Erreur fetchOrganisations:", err);
  } finally {
    isLoading.value = false;
  }
}

async function requestToJoin(group: any) {
  try {
    const rolesData = await apiFetch('/api/group-roles/');
    const roles = (rolesData as any).results || rolesData || [];
    const memberRole = roles.find((r: any) => r.name.toLowerCase().includes('membre')) || roles[0];

    await apiFetch('/api/member-groups/', {
      method: 'POST',
      body: {
        group_id: group.uuid,
        user_id: authStore.uuid,
        role_id: memberRole?.uuid,
        status: 'PENDING'
      }
    });

    group.membershipStatus = 'PENDING';
    alert("Votre demande a été envoyée avec succès au chef de groupe !");
  } catch (err) {
    console.error("Erreur requestToJoin:", err);
    alert("Erreur lors de l'envoi de la demande.");
  }
}

onMounted(() => {
  fetchOrganisations();
});
</script>
