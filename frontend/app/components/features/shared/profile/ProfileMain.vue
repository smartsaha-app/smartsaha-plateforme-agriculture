<template>
  <div class="min-h-[calc(100vh-120px)] py-8 px-4 sm:px-6">
    <div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-6 items-start">

      <!-- ================= SIDEBAR (Profil) ================= -->
      <aside 
        class="md:col-span-4 bg-white rounded-2xl p-6 border border-gray-200/80 shadow-sm flex flex-col items-center text-center space-y-5 transition-all duration-300"
        :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'"
      >
        <!-- Avatar simple -->
        <div class="relative">
          <div class="w-16 h-16 rounded-2xl bg-[#edf8f3] text-[#10b481] flex items-center justify-center font-black text-xl shadow-inner border border-[#10b481]/20">
            <span class="text-2xl font-bold tracking-wider">
              {{ user?.first_name?.slice(0, 2).toUpperCase() || '?' }}
            </span>
          </div>
          <div class="absolute -bottom-1 -right-1 bg-white text-[#10b481] p-1 rounded-full border border-gray-200 shadow-sm" title="Compte vérifié">
            <i class="bx bx-check-circle text-base block"></i>
          </div>
        </div>

        <!-- Infos de base -->
        <div class="space-y-0.5 w-full">
          <h1 class="text-lg font-bold text-[#112830] truncate">
            {{ user?.first_name }} {{ user?.last_name }}
          </h1>
          <p class="text-xs text-gray-500 font-medium truncate">{{ user?.email || 'Chargement...' }}</p>
        </div>

        <!-- Badge Compte -->
        <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-gray-50 border border-gray-200 rounded-lg text-[11px] font-bold text-gray-600">
          <i class="bx bx-shield-alt-2 text-sm text-[#10b481]"></i>
          <span>Compte vérifié</span>
        </span>

        <!-- Actions -->
        <div class="w-full space-y-2 pt-2 border-t border-gray-100">
          <button 
            @click="openLogoutModal"
            class="flex items-center justify-center gap-2 w-full px-4 py-2.5 bg-white hover:bg-red-50 border border-gray-200 hover:border-red-200 rounded-xl text-xs font-bold text-red-600 transition-colors"
          >
            <i class="bx bx-log-out text-sm"></i>
            <span>{{ t("logout") }}</span>
          </button>
        </div>
      </aside>

      <!-- ================= MAIN (Informations) ================= -->
      <main 
        class="md:col-span-8 space-y-5 transition-all duration-300"
        :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'"
      >
        <!-- Carte Informations -->
        <div class="bg-white rounded-2xl border border-gray-200/80 shadow-sm p-6 space-y-5">
          <div class="flex items-center justify-between pb-4 border-b border-gray-100">
            <div>
              <h2 class="text-base font-bold text-[#112830]">Informations personnelles</h2>
              <p class="text-xs text-gray-500">Vos coordonnées de compte</p>
            </div>
            
            <button 
              @click="openProfileModal" 
              class="flex items-center gap-1.5 px-3 py-1.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-xs font-bold text-[#112830] transition-colors"
            >
              <i class="bx bx-edit text-sm text-gray-500"></i>
              <span>{{ t("editProfile") }}</span>
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Prénom -->
            <div class="p-3.5 bg-gray-50 border border-gray-100 rounded-xl space-y-1">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-400">{{ t("firstName") }}</span>
              <p class="text-sm font-bold text-[#112830]">{{ user?.first_name || '—' }}</p>
            </div>

            <!-- Nom -->
            <div class="p-3.5 bg-gray-50 border border-gray-100 rounded-xl space-y-1">
              <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-400">{{ t("lastName") }}</span>
              <p class="text-sm font-bold text-[#112830]">{{ user?.last_name || '—' }}</p>
            </div>

            <!-- Email -->
            <div class="sm:col-span-2 p-3.5 bg-gray-50 border border-gray-100 rounded-xl flex items-center justify-between gap-4">
              <div class="space-y-1 min-w-0">
                <span class="block text-[10px] font-bold uppercase tracking-wider text-gray-400">{{ t("email") }}</span>
                <p class="text-sm font-bold text-[#112830] truncate">{{ user?.email || '—' }}</p>
              </div>
              <span class="inline-flex items-center gap-1 text-xs font-bold text-[#10b481]">
                <i class="bx bx-check-circle"></i> Vérifié
              </span>
            </div>
          </div>
        </div>

        <!-- Carte Sécurité -->
        <div class="bg-white rounded-2xl border border-gray-200/80 shadow-sm p-6 space-y-4">
          <h2 class="text-xs font-bold uppercase tracking-wider text-gray-400">Sécurité</h2>

          <div 
            @click="openPasswordModal"
            class="p-4 bg-gray-50 hover:bg-gray-100/80 border border-gray-200/60 rounded-xl flex items-center justify-between cursor-pointer transition-colors"
          >
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-white border border-gray-200 flex items-center justify-center text-gray-600">
                <i class="bx bx-key text-base"></i>
              </div>
              <div>
                <h3 class="text-sm font-bold text-[#112830]">Mot de passe</h3>
                <p class="text-xs text-gray-500">Mettre à jour la sécurité de votre compte</p>
              </div>
            </div>

            <i class="bx bx-chevron-right text-xl text-gray-400"></i>
          </div>
        </div>

      </main>

    </div>

    <!-- ================= MODALE 1 : ÉDITION DU PROFIL ================= -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div 
          v-if="showProfileModal" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#112830]/40 backdrop-blur-sm"
          @click.self="closeProfileModal"
        >
          <div class="bg-white rounded-2xl border border-gray-200 shadow-xl max-w-md w-full overflow-hidden">
            
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-lg bg-emerald-50 text-[#10b481] flex items-center justify-center font-bold">
                  <i class="bx bx-user text-lg"></i>
                </div>
                <h3 class="text-base font-bold text-[#112830]">Modifier mes informations</h3>
              </div>
              <button @click="closeProfileModal" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
                <i class="bx bx-x text-xl block"></i>
              </button>
            </div>

            <div class="p-6">
              <!-- Accusé de réception / Succès -->
              <div v-if="profileSuccess" class="text-center py-4 space-y-3">
                <div class="w-12 h-12 bg-emerald-50 text-[#10b481] rounded-full flex items-center justify-center mx-auto">
                  <i class="bx bx-check text-2xl"></i>
                </div>
                <p class="text-sm font-bold text-[#112830]">Informations mises à jour avec succès !</p>
                <button @click="closeProfileModal" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-[#112830] font-bold text-xs rounded-xl transition-colors">
                  Fermer
                </button>
              </div>

              <!-- Formulaire -->
              <form v-else @submit.prevent="submitProfileChange" class="space-y-4">
                <div>
                  <label class="block text-xs font-bold text-gray-600 uppercase tracking-wider mb-1.5">{{ t("firstName") }}</label>
                  <input
                    v-model="editForm.first_name"
                    type="text"
                    required
                    class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-[#112830] focus:bg-white focus:border-[#10b481] outline-none transition-all"
                    :disabled="loadingProfile"
                  />
                </div>

                <div>
                  <label class="block text-xs font-bold text-gray-600 uppercase tracking-wider mb-1.5">{{ t("lastName") }}</label>
                  <input
                    v-model="editForm.last_name"
                    type="text"
                    required
                    class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-[#112830] focus:bg-white focus:border-[#10b481] outline-none transition-all"
                    :disabled="loadingProfile"
                  />
                </div>

                <div>
                  <label class="block text-xs font-bold text-gray-600 uppercase tracking-wider mb-1.5">{{ t("email") }}</label>
                  <input
                    v-model="editForm.email"
                    type="email"
                    required
                    class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-[#112830] focus:bg-white focus:border-[#10b481] outline-none transition-all"
                    :disabled="loadingProfile"
                  />
                </div>

                <div v-if="profileError" class="p-3 bg-red-50 border border-red-100 rounded-xl text-xs text-red-600 font-medium">
                  {{ profileError }}
                </div>

                <div class="flex items-center justify-end gap-2 pt-2">
                  <button
                    type="button"
                    @click="closeProfileModal"
                    class="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-bold transition-colors"
                  >
                    Annuler
                  </button>
                  <button
                    type="submit"
                    :disabled="loadingProfile"
                    class="px-5 py-2.5 bg-[#10b481] hover:bg-[#0ea072] disabled:opacity-50 text-white rounded-xl text-xs font-bold transition-colors flex items-center gap-2"
                  >
                    <i v-if="loadingProfile" class="bx bx-loader-alt animate-spin text-base"></i>
                    <span>Enregistrer</span>
                  </button>
                </div>
              </form>
            </div>

          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ================= MODALE 2 : MOT DE PASSE ================= -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div 
          v-if="showPasswordModal" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#112830]/40 backdrop-blur-sm"
          @click.self="closePasswordModal"
        >
          <div class="bg-white rounded-2xl border border-gray-200 shadow-xl max-w-md w-full overflow-hidden">
            
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-lg bg-emerald-50 text-[#10b481] flex items-center justify-center font-bold">
                  <i class="bx bx-shield-quarter text-lg"></i>
                </div>
                <h3 class="text-base font-bold text-[#112830]">Modifier le mot de passe</h3>
              </div>
              <button @click="closePasswordModal" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
                <i class="bx bx-x text-xl block"></i>
              </button>
            </div>

            <div class="p-6">
              <div v-if="passwordSuccess" class="text-center py-4 space-y-3">
                <div class="w-12 h-12 bg-emerald-50 text-[#10b481] rounded-full flex items-center justify-center mx-auto">
                  <i class="bx bx-check text-2xl"></i>
                </div>
                <p class="text-sm font-bold text-[#112830]">Mot de passe mis à jour avec succès !</p>
                <button @click="closePasswordModal" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-[#112830] font-bold text-xs rounded-xl">
                  Fermer
                </button>
              </div>

              <form v-else @submit.prevent="submitPasswordChange" class="space-y-4">
                <div>
                  <label class="block text-xs font-bold text-gray-600 uppercase tracking-wider mb-1.5">Nouveau mot de passe</label>
                  <div class="relative">
                    <input
                      v-model="newPassword"
                      :type="showNew ? 'text' : 'password'"
                      placeholder="Minimum 8 caractères"
                      class="w-full pl-3 pr-10 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-[#112830] focus:bg-white focus:border-[#10b481] outline-none transition-all"
                      :disabled="loadingPassword"
                    />
                    <button type="button" @click="showNew = !showNew" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                      <i :class="showNew ? 'bx bx-hide' : 'bx bx-show'" class="text-base"></i>
                    </button>
                  </div>
                </div>

                <div>
                  <label class="block text-xs font-bold text-gray-600 uppercase tracking-wider mb-1.5">Confirmer le mot de passe</label>
                  <div class="relative">
                    <input
                      v-model="confirmPassword"
                      :type="showConfirm ? 'text' : 'password'"
                      placeholder="Répétez le mot de passe"
                      class="w-full pl-3 pr-10 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm font-medium text-[#112830] focus:bg-white focus:border-[#10b481] outline-none transition-all"
                      :disabled="loadingPassword"
                    />
                    <button type="button" @click="showConfirm = !showConfirm" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                      <i :class="showConfirm ? 'bx bx-hide' : 'bx bx-show'" class="text-base"></i>
                    </button>
                  </div>
                  <p v-if="confirmPassword && newPassword !== confirmPassword" class="mt-1 text-[11px] text-red-500 font-bold">
                    Les mots de passe ne correspondent pas.
                  </p>
                </div>

                <div v-if="passwordError" class="p-3 bg-red-50 border border-red-100 rounded-xl text-xs text-red-600 font-medium">
                  {{ passwordError }}
                </div>

                <div class="flex items-center justify-end gap-2 pt-2">
                  <button type="button" @click="closePasswordModal" class="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-bold">
                    Annuler
                  </button>
                  <button
                    type="submit"
                    :disabled="loadingPassword || !isPasswordValid"
                    class="px-5 py-2.5 bg-[#10b481] hover:bg-[#0ea072] disabled:opacity-50 text-white rounded-xl text-xs font-bold transition-colors flex items-center gap-2"
                  >
                    <i v-if="loadingPassword" class="bx bx-loader-alt animate-spin text-base"></i>
                    <span>Enregistrer</span>
                  </button>
                </div>
              </form>
            </div>

          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ================= MODALE 3 : CONFIRMATION DÉCONNEXION ================= -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div 
          v-if="showLogoutModal" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#112830]/40 backdrop-blur-sm"
          @click.self="closeLogoutModal"
        >
          <div class="bg-white rounded-2xl border border-gray-200 shadow-xl max-w-sm w-full overflow-hidden p-6 text-center space-y-4">
            
            <div class="w-12 h-12 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto">
              <i class="bx bx-log-out text-2xl"></i>
            </div>

            <div class="space-y-1">
              <h3 class="text-base font-bold text-[#112830]">Confirmer la déconnexion</h3>
              <p class="text-xs text-gray-500">Êtes-vous sûr de vouloir vous déconnecter de votre session ?</p>
            </div>

            <div class="flex items-center justify-center gap-2 pt-2">
              <button
                type="button"
                @click="closeLogoutModal"
                class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-bold transition-colors"
                :disabled="loadingLogout"
              >
                Annuler
              </button>
              <button
                type="button"
                @click="confirmLogout"
                :disabled="loadingLogout"
                class="w-full py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold transition-colors flex items-center justify-center gap-2"
              >
                <i v-if="loadingLogout" class="bx bx-loader-alt animate-spin text-base"></i>
                <span>Déconnexion</span>
              </button>
            </div>

          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const props = defineProps<{
  role: string;
}>();

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const user = ref<any>(null);
const isLoaded = ref(false);

// ── Modale Édition Profil ────────────────────────────
const showProfileModal = ref(false);
const loadingProfile = ref(false);
const profileError = ref('');
const profileSuccess = ref(false);
const editForm = reactive({
  first_name: '',
  last_name: '',
  email: ''
});

const openProfileModal = () => {
  editForm.first_name = user.value?.first_name || '';
  editForm.last_name = user.value?.last_name || '';
  editForm.email = user.value?.email || '';
  profileError.value = '';
  profileSuccess.value = false;
  showProfileModal.value = true;
};

const closeProfileModal = () => {
  showProfileModal.value = false;
};

const submitProfileChange = async () => {
  loadingProfile.value = true;
  profileError.value = '';

  try {
    const updated = await apiFetch(`/api/users/${authStore.uuid}/`, {
      method: 'PATCH',
      body: editForm
    });
    
    user.value = { ...user.value, ...updated };
    profileSuccess.value = true;
  } catch (err: any) {
    profileError.value = err?.data?.error || "Erreur lors de la mise à jour des informations.";
  } finally {
    loadingProfile.value = false;
  }
};

// ── Modale Mot de Passe ──────────────────────────────
const showPasswordModal = ref(false);
const newPassword = ref('');
const confirmPassword = ref('');
const showNew = ref(false);
const showConfirm = ref(false);
const loadingPassword = ref(false);
const passwordError = ref('');
const passwordSuccess = ref(false);

const isPasswordValid = computed(() => {
  return newPassword.value.length >= 8 && newPassword.value === confirmPassword.value;
});

const openPasswordModal = () => {
  newPassword.value = '';
  confirmPassword.value = '';
  passwordError.value = '';
  passwordSuccess.value = false;
  showPasswordModal.value = true;
};

const closePasswordModal = () => {
  showPasswordModal.value = false;
};

const submitPasswordChange = async () => {
  if (!isPasswordValid.value) return;
  
  loadingPassword.value = true;
  passwordError.value = '';

  try {
    await apiFetch('/api/change-password/', {
      method: 'POST',
      body: {
        new_password: newPassword.value,
        confirm_password: confirmPassword.value,
      }
    });
    passwordSuccess.value = true;
  } catch (err: any) {
    passwordError.value = err?.data?.error || "Erreur lors de la modification du mot de passe.";
  } finally {
    loadingPassword.value = false;
  }
};

// ── Modale Confirmation Déconnexion ───────────────────
const showLogoutModal = ref(false);
const loadingLogout = ref(false);

const openLogoutModal = () => {
  showLogoutModal.value = true;
};

const closeLogoutModal = () => {
  showLogoutModal.value = false;
};

const confirmLogout = async () => {
  loadingLogout.value = true;
  await authStore.clearUserData();
  showLogoutModal.value = false;
  loadingLogout.value = false;
  router.push("/login");
};

// ── Initialisation ──────────────────────────────────
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
    return;
  }
  
  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    user.value = {
      username: data.username,
      email: data.email,
      first_name: data.first_name,
      last_name: data.last_name,
      id: data.id,
      date_joined: data.date_joined,
    };
    setTimeout(() => (isLoaded.value = true), 50);
  } catch (err) {
    console.error(err);
  }
});
</script>