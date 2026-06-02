<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- ===== HEADER ===== -->
    <PageHeader :title="t('admin.usersTitle')">
      <template #subtitle>
        <i class="bx bx-group"></i>
        {{ t('admin.usersDesc') }}
      </template>
      <template #breadcrumb>
        <NuxtLink to="/admin" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('admin.dashboardTitle') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('admin.usersTitle') }}</span>
      </template>
    </PageHeader>

    <div class="flex justify-end -mt-2">
      <button @click="showInviteModal = true"
        class="flex items-center gap-2 px-4 py-2.5 bg-[#112830] text-white rounded-xl text-sm font-bold hover:bg-[#10b481] transition-all shadow-sm">
        <i class="bx bx-user-plus text-base"></i>
        {{ t('admin.addSupervisor') }}
      </button>
    </div>

    <!-- ===== FILTERS ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-3 flex items-center gap-2 overflow-x-auto">
      <div class="flex-1 min-w-[160px] relative">
        <i class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base pointer-events-none"></i>
        <input v-model="searchQuery" type="text" :placeholder="t('admin.searchUser')"
          class="w-full pl-9 pr-8 py-2.5 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 transition-all font-medium text-[#112830]" />
        <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500">
          <i class="bx bx-x"></i>
        </button>
      </div>
      <div class="hidden md:block w-px h-7 bg-gray-100 flex-shrink-0"></div>
      <div class="flex gap-1 flex-shrink-0">
        <button v-for="t in filterTypes" :key="t.val" @click="selectedType = t.val"
          :class="['px-4 py-2 rounded-xl text-xs font-bold transition-all', selectedType === t.val ? 'bg-[#112830] text-white' : 'bg-gray-50 text-gray-400 hover:bg-gray-100']">
          {{ t.label }}
        </button>
      </div>
      <span class="ml-auto text-xs font-bold text-gray-400 whitespace-nowrap flex-shrink-0">
        {{ filteredUsers.length }} utilisateur{{ filteredUsers.length !== 1 ? 's' : '' }}
      </span>
    </div>

    <!-- ===== TABLE ===== -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div v-if="isLoading" class="py-20 flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-2 border-[#10b481] border-t-transparent rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-gray-400 uppercase tracking-widest">{{ t('admin.loadingUsers') }}</p>
      </div>

      <div v-else-if="filteredUsers.length === 0" class="py-20 text-center space-y-4">
        <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mx-auto">
          <i class="bx bx-user-x text-4xl text-gray-200"></i>
        </div>
        <p class="text-sm text-gray-400 font-medium">{{ t('admin.noUsers') }}</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-gray-50/70 border-b border-gray-100">
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('admin.colUser') }}</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('admin.colRole') }}</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest hidden md:table-cell">{{ t('admin.colJoined') }}</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest">{{ t('admin.colStatus') }}</th>
              <th class="px-6 py-4 text-[9px] font-black text-gray-400 uppercase tracking-widest text-right">{{ t('dashboard.thactions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="user in filteredUsers" :key="user.uuid" class="hover:bg-gray-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-[#112830] text-white flex items-center justify-center font-black text-sm overflow-hidden flex-shrink-0">
                    <img v-if="user.avatar" :src="user.avatar" alt="" class="w-full h-full object-cover" />
                    <span v-else>{{ (user.first_name || user.username || '?').charAt(0).toUpperCase() }}</span>
                  </div>
                  <div class="min-w-0">
                    <div class="flex items-center gap-1.5">
                      <p class="text-sm font-black text-[#112830] group-hover:text-[#10b481] transition-colors truncate">
                        {{ user.first_name }} {{ user.last_name }}
                      </p>
                      <i v-if="user.is_staff" class="bx bxs-badge-check text-blue-500 text-sm flex-shrink-0" title="Staff"></i>
                    </div>
                    <p class="text-xs text-gray-400 truncate">{{ user.email }}</p>
                  </div>
                </div>
              </td>

              <td class="px-6 py-4">
                <span class="px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest bg-gray-50 text-gray-500 border border-gray-100">
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>

              <td class="px-6 py-4 hidden md:table-cell">
                <span class="text-xs font-medium text-gray-400">{{ formatDate(user.date_joined) }}</span>
              </td>

              <td class="px-6 py-4">
                <span :class="['px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest', user.is_active ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-rose-50 text-rose-500 border border-rose-100']">
                  {{ user.is_active ? t('admin.statusActive') : t('admin.statusDisabled') }}
                </span>
              </td>

              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button @click="toggleStaff(user)"
                    :class="['flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border transition-all', user.is_staff ? 'bg-blue-50 border-blue-100 text-blue-500 hover:bg-blue-500 hover:text-white hover:border-blue-500' : 'bg-gray-50 border-gray-100 text-gray-400 hover:bg-gray-500 hover:text-white hover:border-gray-500']"
                    title="Basculer Staff">
                    <i class="bx bx-shield-quarter text-sm"></i>
                    <span class="hidden lg:inline">{{ t('admin.toggleStaff') }}</span>
                  </button>
                  <button @click="confirmToggleStatus(user)"
                    :class="['flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold border transition-all', user.is_active ? 'bg-rose-50 border-rose-100 text-rose-500 hover:bg-rose-500 hover:text-white hover:border-rose-500' : 'bg-emerald-50 border-emerald-100 text-emerald-500 hover:bg-emerald-500 hover:text-white hover:border-emerald-500']"
                    :title="user.is_active ? 'Désactiver' : 'Activer'">
                    <i :class="user.is_active ? 'bx bx-block' : 'bx bx-check-double'" class="text-sm"></i>
                    <span class="hidden lg:inline">{{ user.is_active ? t('admin.disableAccount') : t('admin.enableAccount') }}</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!isLoading && totalCount > 20" class="px-6 py-4 border-t border-gray-50">
        <PaginationBase :totalCount="totalCount" :perPage="20"
          v-model:currentPage="currentPage" @change-page="(p) => currentPage = p" />
      </div>
    </div>

    <!-- ===== MODALE INVITE ===== -->
    <div v-if="showInviteModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-11 h-11 bg-[#112830] rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-user-plus text-white text-lg"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">{{ t('admin.inviteModalTitle') }}</h2>
            <p class="text-xs text-gray-400">{{ t('admin.inviteModalDesc') }}</p>
          </div>
        </div>
        <div class="space-y-3">
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.inviteEmail') }}</label>
            <input v-model="inviteForm.email" type="email" placeholder="superviseur@example.com"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium" />
          </div>
          <div class="space-y-1.5">
            <label class="text-[9px] font-black text-gray-400 uppercase tracking-widest block">{{ t('admin.inviteFirstName') }}</label>
            <input v-model="inviteForm.first_name" type="text" :placeholder="t('admin.inviteFirstName')"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/30 font-medium" />
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="showInviteModal = false; inviteForm = { email: '', first_name: '' }"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="sendInvite" :disabled="!inviteForm.email || isInviting"
            class="flex-1 py-3 rounded-xl bg-[#112830] text-white font-bold text-sm hover:bg-[#10b481] transition-all disabled:opacity-40 flex items-center justify-center gap-2">
            <div v-if="isInviting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <i v-else class="bx bx-send"></i>
            {{ t('admin.inviteBtn') }}
          </button>
        </div>
      </div>
    </div>

    <!-- ===== MODALE CONFIRM STATUS ===== -->
    <div v-if="userToToggle" class="fixed inset-0 z-[100] flex items-center justify-center p-6 backdrop-blur-sm bg-black/20">
      <div class="bg-white w-full max-w-sm rounded-2xl p-8 shadow-2xl space-y-5 border border-gray-100">
        <div class="text-center space-y-3">
          <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mx-auto', userToToggle.is_active ? 'bg-rose-50' : 'bg-emerald-50']">
            <i :class="['text-2xl', userToToggle.is_active ? 'bx bx-block text-rose-500' : 'bx bx-check-double text-emerald-500']"></i>
          </div>
          <div>
            <h2 class="text-base font-black text-[#112830]">
              {{ userToToggle.is_active ? t('admin.deactivateConfirm') : t('admin.activateConfirm') }}
            </h2>
            <p class="text-sm text-gray-400 mt-1">
              <span class="font-bold text-[#112830]">{{ userToToggle.first_name }} {{ userToToggle.last_name }}</span>
            </p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="userToToggle = null"
            class="flex-1 py-3 rounded-xl border border-gray-100 text-gray-500 font-bold text-sm hover:bg-gray-50 transition-colors">
            {{ t('dashboard.cancel') }}
          </button>
          <button @click="executeToggleStatus"
            :class="['flex-1 py-3 rounded-xl text-white font-bold text-sm transition-all', userToToggle.is_active ? 'bg-rose-500 hover:bg-rose-600' : 'bg-[#10b481] hover:bg-emerald-400']">
            {{ t('dashboard.confirm') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <transition name="slide-up">
      <div v-if="toast.visible"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-sm font-bold"
        :class="toast.type === 'success' ? 'bg-[#112830] text-white' : 'bg-rose-500 text-white'">
        <i :class="toast.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'" class="text-lg"
          :style="toast.type === 'success' ? 'color:#10b481' : ''"></i>
        {{ toast.message }}
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '~/composables/useApi';
import PaginationBase from '~/components/ui/PaginationBase.vue';

definePageMeta({ layout: 'dashboard' });
const { t } = useI18n();

const { apiFetch } = useApi();

const isLoading    = ref(true);
const searchQuery  = ref('');
const selectedType = ref('all');
const users        = ref<any[]>([]);
const totalCount   = ref(0);
const currentPage  = ref(1);
const showInviteModal = ref(false);
const isInviting   = ref(false);
const inviteForm   = ref({ email: '', first_name: '' });
const userToToggle = ref<any>(null);
const toast = ref({ visible: false, message: '', type: 'success' as 'success' | 'error' });

const filterTypes = computed(() => [
  { label: t('admin.filterAll'),     val: 'all'    },
  { label: t('admin.filterOrgs'),    val: 'org'    },
  { label: t('admin.filterFarmers'), val: 'farmer' },
  { label: t('admin.filterStaff'),   val: 'staff'  },
]);

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toast.value = { visible: true, message, type };
  setTimeout(() => (toast.value.visible = false), 3000);
}

function getRoleLabel(role: string) {
  const map: Record<string, string> = {
    farmer:       t('admin.roleLabel_farmer'),
    buyer:        t('admin.roleLabel_buyer'),
    seller:       t('admin.roleLabel_seller'),
    organisation: t('admin.roleLabel_organisation'),
    admin:        t('admin.roleLabel_admin'),
    staff:        t('admin.roleLabel_staff'),
  };
  return map[role] || role || t('admin.roleLabel_farmer');
}

function formatDate(d: string) {
  if (!d) return '—';
  return new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' });
}

const filteredUsers = computed(() => {
  let result = users.value;
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(u =>
      (u.username || '').toLowerCase().includes(q) ||
      (u.email    || '').toLowerCase().includes(q) ||
      (u.first_name || '').toLowerCase().includes(q) ||
      (u.last_name  || '').toLowerCase().includes(q)
    );
  }
  if (selectedType.value !== 'all') {
    if (selectedType.value === 'staff')  result = result.filter(u => u.is_staff);
    if (selectedType.value === 'org')    result = result.filter(u => u.org);
    if (selectedType.value === 'farmer') result = result.filter(u => !u.is_staff && !u.org);
  }
  return result;
});

async function fetchUsers() {
  isLoading.value = true;
  try {
    const data: any = await apiFetch(`/api/users/?page=${currentPage.value}${searchQuery.value ? '&search=' + searchQuery.value : ''}`);
    const raw = data.results || data || [];
    totalCount.value = data.count || raw.length;
    users.value = raw.map((u: any) => ({
      ...u,
      org:    u.organisations_created?.length ? u.organisations_created[0].name : null,
      avatar: u.avatar || null,
    }));
  } catch (err) {
    console.error('Erreur fetchUsers:', err);
  } finally {
    isLoading.value = false;
  }
}

function confirmToggleStatus(user: any) { userToToggle.value = user; }

async function executeToggleStatus() {
  if (!userToToggle.value) return;
  const user = userToToggle.value;
  try {
    await apiFetch(`/api/users/${user.uuid}/`, { method: 'PATCH', body: { is_active: !user.is_active } });
    user.is_active = !user.is_active;
    showToast(user.is_active ? t('admin.toggleStatusSuccess_active') : t('admin.toggleStatusSuccess_disabled'));
  } catch {
    showToast(t('admin.toggleStatusError'), 'error');
  } finally {
    userToToggle.value = null;
  }
}

async function toggleStaff(user: any) {
  try {
    await apiFetch(`/api/users/${user.uuid}/`, { method: 'PATCH', body: { is_staff: !user.is_staff } });
    user.is_staff = !user.is_staff;
    showToast(user.is_staff ? t('admin.staffGranted') : t('admin.staffRevoked'));
  } catch {
    showToast(t('admin.staffError'), 'error');
  }
}

async function sendInvite() {
  if (!inviteForm.value.email) return;
  isInviting.value = true;
  try {
    await apiFetch('/api/users/', {
      method: 'POST',
      body: { ...inviteForm.value, is_staff: true, role: 'staff' },
    });
    showInviteModal.value = false;
    inviteForm.value = { email: '', first_name: '' };
    showToast(t('admin.inviteSuccess'));
    fetchUsers();
  } catch {
    showToast(t('admin.inviteError'), 'error');
  } finally {
    isInviting.value = false;
  }
}

watch(currentPage, () => fetchUsers());
watch(searchQuery, () => { currentPage.value = 1; fetchUsers(); });

onMounted(() => fetchUsers());
</script>

<style scoped>
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translate(-50%, 1rem); }
</style>