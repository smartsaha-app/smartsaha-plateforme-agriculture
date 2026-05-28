<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">
    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('organisations.title')">
      <template #subtitle>
        <i class="bx bx-buildings"></i>
        {{ t('organisations.subtitle') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Organisations</span>
      </template>
    </PageHeader>

    <!-- ===== SEARCH & FILTERS ===== -->
    <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-3">
      <div class="flex-1 relative">
        <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Rechercher une organisation ou un groupe..."
          class="w-full pl-11 pr-4 py-3 bg-gray-50 rounded-xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 transition-all text-sm font-medium text-[#112830]"
          @input="onSearchInput"
        />
        <button
          v-if="searchQuery"
          @click="searchQuery = ''; fetchOrganisations()"
          class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500 transition-colors"
        >
          <i class="bx bx-x text-lg"></i>
        </button>
      </div>

      <div class="w-full md:w-56 relative">
        <i class="bx bx-filter-alt absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-lg pointer-events-none"></i>
        <select
          v-model="membershipFilter"
          class="w-full pl-11 pr-4 py-3 bg-gray-50 rounded-xl border-none outline-none focus:ring-2 focus:ring-[#10b481]/20 transition-all text-sm font-medium text-[#112830] appearance-none cursor-pointer"
        >
          <option value="all">Tous les groupes</option>
          <option value="member">Déjà membre</option>
          <option value="non-member">Pas encore membre</option>
        </select>
        <i class="bx bx-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
      </div>

      <div class="flex items-center gap-2 text-xs font-bold text-gray-400 px-2 whitespace-nowrap">
        <i class="bx bx-buildings text-base"></i>
        {{ filteredGroups.length }} groupe{{ filteredGroups.length !== 1 ? 's' : '' }}
      </div>
    </div>

    <!-- ===== LOADING ===== -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="h-64 bg-white rounded-2xl border border-gray-100 shadow-sm animate-pulse"></div>
    </div>

    <!-- ===== EMPTY STATE ===== -->
    <div v-else-if="filteredGroups.length === 0" class="bg-white py-24 rounded-2xl border border-gray-100 text-center space-y-4 shadow-sm">
      <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-200">
        <i class="bx bx-buildings text-5xl"></i>
      </div>
      <div>
        <h3 class="text-lg font-black text-[#112830]">{{ t('organisations.noOrganisations') }}</h3>
        <p class="text-gray-400 text-sm mt-1">Essayez de modifier votre recherche ou filtre</p>
      </div>
    </div>

    <!-- ===== ORGANISATION CARDS ===== -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="group in filteredGroups"
        :key="group.uuid"
        class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden flex flex-col"
      >
        <!-- Card header stripe -->
        <div class="h-2 w-full"
          :class="group.membershipStatus === 'MEMBER' ? 'bg-[#10b481]' : group.membershipStatus === 'PENDING' ? 'bg-amber-400' : 'bg-[#112830]'">
        </div>

        <div class="p-6 flex-1 flex flex-col gap-4">
          <!-- Organisation info row -->
          <div class="flex items-start gap-4">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-xl font-black text-white shrink-0 transition-colors duration-300"
              :class="group.membershipStatus === 'MEMBER' ? 'bg-[#10b481]' : group.membershipStatus === 'PENDING' ? 'bg-amber-400' : 'bg-[#112830] group-hover:bg-[#10b481]'">
              {{ group.organisation?.name?.[0]?.toUpperCase() || 'O' }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <span class="px-2 py-0.5 bg-gray-50 text-[#112830] border border-gray-100 rounded-lg text-[9px] font-black uppercase tracking-widest">
                  {{ group.type?.name || 'Groupe' }}
                </span>
                <span
                  v-if="group.membershipStatus === 'MEMBER'"
                  class="px-2 py-0.5 bg-emerald-50 text-[#10b481] border border-emerald-100 rounded-lg text-[9px] font-black uppercase tracking-widest flex items-center gap-1"
                >
                  <i class="bx bx-check-double"></i> {{ t('organisations.memberStatus') }}
                </span>
                <span
                  v-else-if="group.membershipStatus === 'PENDING'"
                  class="px-2 py-0.5 bg-amber-50 text-amber-600 border border-amber-100 rounded-lg text-[9px] font-black uppercase tracking-widest flex items-center gap-1"
                >
                  <i class="bx bx-time"></i> {{ t('organisations.pendingStatus') }}
                </span>
              </div>
              <h3 class="text-base font-black text-[#112830] group-hover:text-[#10b481] transition-colors truncate">
                {{ group.name }}
              </h3>
              <p class="text-xs text-gray-400 font-bold truncate">{{ group.organisation?.name }}</p>
            </div>
          </div>

          <!-- Description -->
          <p class="text-gray-500 text-sm leading-relaxed line-clamp-2 flex-1">
            {{ group.description || t('organisations.defaultGroupDesc') }}
          </p>

          <!-- Stats row -->
          <div class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
            <div class="flex items-center gap-2">
              <i class="bx bx-group text-[#10b481] text-base"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none">{{ t('organisations.members') }}</p>
                <p class="text-sm font-black text-[#112830] leading-tight">{{ group.active_members_count }}</p>
              </div>
            </div>
            <div class="w-px h-8 bg-gray-200 mx-1"></div>
            <div class="flex items-center gap-2">
              <i class="bx bx-map-pin text-gray-400 text-base"></i>
              <div>
                <p class="text-[8px] font-black text-gray-400 uppercase tracking-widest leading-none">{{ t('organisations.zone') }}</p>
                <p class="text-sm font-black text-[#112830] leading-tight truncate max-w-[120px]">
                  {{ group.organisation?.address || 'Antsirabe' }}
                </p>
              </div>
            </div>
          </div>

          <!-- CTA button -->
          <button
            @click="requestToJoin(group)"
            :disabled="group.membershipStatus !== 'NONE'"
            class="w-full py-3 rounded-xl font-black text-xs uppercase tracking-widest transition-all flex items-center justify-center gap-2"
            :class="group.membershipStatus !== 'NONE'
              ? 'bg-gray-50 text-gray-400 cursor-not-allowed border border-gray-100'
              : 'bg-[#112830] text-white hover:bg-[#10b481] shadow-md shadow-[#112830]/10 hover:shadow-[#10b481]/20'"
          >
            <i
              :class="group.membershipStatus === 'PENDING'
                ? 'bx bx-time'
                : group.membershipStatus === 'MEMBER'
                  ? 'bx bx-check-circle'
                  : 'bx bx-user-plus'"
            ></i>
            {{ group.membershipStatus === 'PENDING'
              ? t('organisations.requestSent')
              : group.membershipStatus === 'MEMBER'
                ? t('organisations.alreadyMember')
                : t('organisations.joinGroup') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useApi } from '~/composables/useApi';
import { useAuthStore } from '~/stores/auth';

definePageMeta({ layout: 'dashboard' });

const { apiFetch } = useApi();
const authStore = useAuthStore();
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(key);

const searchQuery = ref('');
const membershipFilter = ref('all');
const isLoading = ref(true);
const allGroups = ref<any[]>([]);

let searchTimer: ReturnType<typeof setTimeout> | null = null;

function onSearchInput() {
  if (searchTimer) clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    fetchOrganisations();
  }, 400);
}

const filteredGroups = computed(() => {
  return allGroups.value.filter((g: any) => {
    if (membershipFilter.value === 'member') return g.membershipStatus === 'MEMBER';
    if (membershipFilter.value === 'non-member') return g.membershipStatus === 'NONE';
    return true;
  });
});

watch(membershipFilter, () => {
  // client-side filter on membership, no refetch needed
});

async function fetchOrganisations() {
  isLoading.value = true;
  try {
    const userUuid = authStore.uuid;
    const [data, activeMemberships, pendingMemberships] = await Promise.all([
      apiFetch(`/api/groups/?discovery=true&search=${searchQuery.value}`),
      apiFetch(`/api/member-groups/?user=${userUuid}`),
      apiFetch(`/api/member-groups/?user=${userUuid}&status=PENDING`),
    ]);

    const groups = (data as any).results || data || [];
    const membershipsList = [
      ...((activeMemberships as any).results || activeMemberships || []),
      ...((pendingMemberships as any).results || pendingMemberships || []),
    ];

    // Deduplicate by uuid in case some records appear in both calls
    const seen = new Set<string>();
    const uniqueMemberships = membershipsList.filter((m: any) => {
      if (seen.has(m.uuid)) return false;
      seen.add(m.uuid);
      return true;
    });

    allGroups.value = groups.map((g: any) => {
      const membership = uniqueMemberships.find((m: any) => m.group?.uuid === g.uuid || m.group === g.uuid);
      let status = 'NONE';
      if (membership) {
        status = membership.status === 'ACTIVE' ? 'MEMBER' : 'PENDING';
      }
      return { ...g, membershipStatus: status };
    });
  } catch (err) {
    console.error('Erreur fetchOrganisations:', err);
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
    alert(t('organisations.successRequest'));
  } catch (err) {
    console.error('Erreur requestToJoin:', err);
    alert(t('organisations.errorRequest'));
  }
}

onMounted(() => {
  fetchOrganisations();
});
</script>