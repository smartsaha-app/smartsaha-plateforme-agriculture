<template>
  <div class="h-screen bg-[#fefefe] flex flex-col">

    <!-- ═══════════════════════════════════════════
         HEADER — Barre de navigation supérieure fixe
         ═══════════════════════════════════════════ -->
    <header
      class="fixed top-0 left-0 right-0 z-50 flex items-center px-4 sm:px-8 h-20 bg-[#fefefe] backdrop-blur-md shadow-sm"
    >
      <!-- Logo + Titre -->
      <div class="flex items-center gap-2">
        <button class="sm:hidden p-2 text-gray-800" @click="toggleMobileMenu">
          <i class="bx bx-menu text-2xl"></i>
        </button>

        <div class="flex items-center gap-4 -ml-0 sm:-ml-5">
          <div class="h-12 w-12 sm:h-14 sm:w-14 rounded flex items-center justify-center">
            <img src="/logo.png" alt="Logo SmartSaha" />
          </div>
          <div class="hidden sm:flex flex-col text-left">
            <h1 class="text-xl font-extrabold text-[#112830] tracking-tight">SmartSaha</h1>
            <p class="text-sm text-gray-500">{{ t("dashboard.slogan") }}</p>
          </div>
        </div>
      </div>

      <!-- Actions header (desktop uniquement) -->
      <div class="hidden sm:flex items-center gap-6 ml-auto">

        <!-- Sélecteur de langue -->
        <div class="relative inline-block w-40" data-lang-dropdown>
          <button
            @click="open = !open"
            class="w-full bg-gray-50 rounded p-4 flex items-center justify-between shadow-inner"
          >
            <span class="flex items-center gap-2" v-if="currentLocale">
              <img :src="currentLocale.flag" alt="" class="w-5 h-5 rounded-full" />
              <span class="text-sm font-medium">{{ currentLocale.name }}</span>
            </span>
            <i class="bx bx-chevron-down text-lg"></i>
          </button>
          <transition name="fade">
            <ul v-if="open" class="absolute mt-1 w-full bg-white rounded shadow-lg overflow-hidden z-50">
              <li
                v-for="loc in locales"
                :key="loc.code"
                @click="selectLocale(loc.code)"
                class="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-[#10b481]/10 transition-colors"
              >
                <img :src="loc.flag" alt="" class="w-5 h-5 rounded-full" />
                <span class="text-sm font-medium">{{ loc.name }}</span>
              </li>
            </ul>
          </transition>
        </div>

        <!-- Menu utilisateur -->
        <div class="relative" data-user-dropdown>
          <button
            @click="userMenuOpen = !userMenuOpen"
            class="flex items-center gap-1 p-1 backdrop-blur-sm rounded transition"
          >
            <div class="h-10 w-10 rounded-full bg-[#10b481] flex items-center justify-center">
              <i class="bx bxs-user text-white text-lg"></i>
            </div>
            <div class="ml-2 text-left">
              <p class="font-semibold text-[#222831] text-sm">{{ user?.first_name }}</p>
              <p class="text-xs text-gray-500">{{ user?.email }}</p>
            </div>
            <i class="bx bx-chevron-down ml-auto text-sm"></i>
          </button>

          <transition name="fade">
            <ul
              v-if="userMenuOpen"
              class="absolute right-0 top-[calc(100%+8px)] w-56 bg-white border border-gray-100 rounded-2xl shadow-[0_4px_6px_-1px_rgba(0,0,0,0.06),_0_16px_40px_-4px_rgba(0,0,0,0.12)] z-50 overflow-hidden list-none p-1.5 origin-top-right"
            >
              <li class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-gradient-to-br mb-1">
                <div class="w-9 h-9 rounded-full bg-gradient-to-br from-[#10b481] to-[#10b481] flex items-center justify-center text-white text-base flex-shrink-0">
                  <i class="bx bxs-user"></i>
                </div>
                <div class="flex flex-col flex-1 min-w-0">
                  <span class="text-[0.82rem] font-semibold text-[#1a2130] truncate">{{ user?.first_name }}</span>
                  <span class="text-[0.68rem] text-gray-400 truncate">{{ user?.email }}</span>
                </div>
              </li>

              <li class="h-px bg-gray-100 my-1 mx-1"></li>

              <li
                v-for="(item, index) in userMenuItems"
                :key="item.labelKey"
                @click="handleMenuClick(item)"
                :class="[
                  'group flex items-center gap-2.5 px-3 py-2 rounded-xl cursor-pointer transition-all duration-150 text-sm',
                  index === userMenuItems.length - 1 ? 'mt-1 border-t border-gray-100 pt-2' : '',
                  item.danger
                    ? 'text-red-500 hover:bg-red-50 hover:text-red-600'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                ]"
              >
                <span
                  :class="[
                    'w-7 h-7 rounded-lg flex items-center justify-center text-sm flex-shrink-0 transition-colors duration-150',
                    item.danger
                      ? 'bg-red-50 text-red-400 group-hover:text-red-500'
                      : 'bg-gray-100 text-gray-400 group-hover:text-[#10b481]'
                  ]"
                >
                  <i :class="item.icon"></i>
                </span>
                <span class="flex-1">{{ t(item.labelKey) }}</span>
                <i
                  v-if="!item.danger"
                  class="bx bx-chevron-right text-gray-300 text-sm opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all duration-150"
                ></i>
              </li>
            </ul>
          </transition>
        </div>
      </div>
    </header>
    <!-- FIN HEADER -->


    <!-- ═══════════════════════════════════════════
         MENU MOBILE
         ═══════════════════════════════════════════ -->
    <aside
      v-if="isMobileMenuOpen"
      class="fixed inset-0 z-50 bg-[#112830]/95 backdrop-blur-sm flex flex-col sm:hidden"
    >
      <div class="flex justify-between items-center p-4 border-b border-gray-700">
        <div class="flex items-center gap-3">
          <div class="h-10 w-10 rounded-full bg-[#f4a261] flex items-center justify-center">
            <i class="bx bxs-user text-white text-lg"></i>
          </div>
          <div class="flex flex-col">
            <p class="text-white font-semibold text-sm">{{ user?.first_name }}</p>
            <p class="text-gray-300 text-xs font-light">{{ user?.email }}</p>
          </div>
        </div>
        <button @click="toggleMobileMenu" class="text-white text-2xl">
          <i class="bx bx-x"></i>
        </button>
      </div>

      <!-- Sélecteur de langue mobile -->
      <div class="flex flex-col gap-4 px-4 py-4 border-b border-gray-700">
        <div>
          <label class="text-white text-sm mb-1 block">Language</label>
          <select v-model="locale" class="w-full p-2 rounded bg-[#112830] text-white">
            <option v-for="loc in locales" :key="loc.code" :value="loc.code">
              {{ loc.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Navigation principale mobile -->
      <nav class="flex-1 overflow-y-auto py-4 px-2 flex flex-col gap-2">
        <button
          @click="goTo(`/${rolePath}/assistant`)"
          class="relative flex items-center gap-3 px-4 py-3 text-white hover:bg-[#10b481]/20 rounded w-full text-left transition-colors duration-200"
        >
          <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(`/${rolePath}/assistant`) ? 'opacity-100' : 'opacity-0']"></span>
          <i class="bx bx-robot text-xl ml-2 text-white"></i>
          <span class="text-sm font-light">Sesily</span>
        </button>

        <template v-for="(item, index) in sidebarMenu" :key="'m_'+index">
          <div v-if="item.isHeader" class="px-4 py-2 mt-2 text-xs font-bold text-gray-400 uppercase tracking-widest border-b border-gray-700/50 pb-1 mb-2">
            {{ item.label }}
          </div>
          <button
            v-else
            @click="goTo(item.to)"
            class="relative flex items-center gap-3 px-4 py-3 text-white hover:bg-[#10b481]/20 rounded w-full text-left transition-colors duration-200"
          >
            <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(item.to) ? 'opacity-100' : 'opacity-0']"></span>
            <i :class="item.icon + ' text-xl ml-2'"></i>
            <span class="text-sm font-light flex-1">{{ item.label }}</span>
          </button>
        </template>

        <button
          @click="logout"
          class="flex items-center gap-3 px-3 py-2 hover:bg-red-500/20 rounded text-white"
        >
          <i class="bx bx-log-out text-xl"></i>
          <span>{{ t("dashboard.logout") }}</span>
        </button>
      </nav>
    </aside>
    <!-- FIN MENU MOBILE -->


    <!-- ═══════════════════════════════════════════
         LAYOUT PRINCIPAL — Sidebar fixe + Contenu
         ═══════════════════════════════════════════ -->
    <div class="flex flex-1 pt-20">

      <aside class="hidden sm:flex fixed top-20 left-0 h-[calc(100vh-5rem)] flex-col bg-[#112830] shadow-lg w-56 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
        <nav class="flex flex-col space-y-1 py-4">
          <template v-for="(item, index) in sidebarMenu" :key="index">
            <div v-if="item.isHeader" class="px-4 py-2 mt-4 text-[10px] font-black text-gray-500 uppercase tracking-[0.2em] border-b border-gray-700 pb-1 mb-2">
              {{ item.label }}
            </div>
            <button
              v-else
              @click="router.push(item.to)"
              class="relative flex items-center gap-3 px-4 py-2 text-white transition-colors duration-200 hover:bg-white/10 w-full text-left"
            >
              <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(item.to) ? 'opacity-100' : 'opacity-0']"></span>
              <i :class="item.icon + ' text-xl ml-2 font-light'"></i>
              <span class="font-light text-sm flex-1">{{ item.label }}</span>
            </button>
          </template>
        </nav>

        <!-- Bas de la sidebar -->
        <div class="mt-auto flex flex-col space-y-1 px-2 py-4 border-t border-gray-600">
          <button
            @click="router.push(`/${rolePath}/profil`)"
            class="relative flex items-center gap-3 px-3 py-2 text-white hover:bg-[#10b481]/20 rounded transition-colors duration-200"
          >
            <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(`/${rolePath}/profil`) ? 'opacity-100' : 'opacity-0']"></span>
            <i class="bx bx-user text-xl ml-2 text-white"></i>
            <span class="text-white font-light text-sm">Mon profil</span>
          </button>

          <button
            @click="router.push(`/${rolePath}/assistant`)"
            class="relative flex items-center gap-3 px-3 py-2 text-white hover:bg-[#10b481]/20 rounded transition-colors duration-200"
          >
            <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(`/${rolePath}/assistant`) ? 'opacity-100' : 'opacity-0']"></span>
            <i class="bx bx-robot text-xl ml-2 text-white"></i>
            <span class="text-white font-light text-sm">Assistant IA</span>
          </button>

          <button
            @click="router.push(`/${rolePath}/help`)"
            class="relative flex items-center gap-3 px-3 py-2 text-white hover:bg-[#10b481]/20 rounded transition-colors duration-200"
          >
            <span :class="['absolute left-0 top-1/2 -translate-y-1/2 h-[60%] border-l-[3px] border-white transition-all duration-200', isActive(`/${rolePath}/help`) ? 'opacity-100' : 'opacity-0']"></span>
            <i class="bx bx-info-circle text-xl ml-2 text-white"></i>
            <span class="text-white font-light text-sm">{{ t("dashboard.help") }}</span>
          </button>
        </div>
      </aside>

      <main class="flex-1 p-6 sm:ml-56">
        <slot />
      </main>
    </div>
    <!-- FIN LAYOUT PRINCIPAL -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

// ─── Router & Store & i18n ───────────────────────────────────────────────────
const router      = useRouter();
const route       = useRoute();
const authStore   = useAuthStore();
const { apiFetch } = useApi();
const { t, locale, setLocale } = useI18n();

const isActive = (path: string): boolean => {
  if (path === "/farmer/dashboard" || path === "/organization/dashboard" || path === "/admin") {
    return route.path === path;
  }
  return route.path === path || route.path.startsWith(path + "/");
};

// ─── Langues disponibles ──────────────────────────────────────────────────────
const locales = [
  { code: "en", name: "English",  flag: "/flags/en.png" },
  { code: "fr", name: "Français", flag: "/flags/fr.png" },
  { code: "mg", name: "Malagasy", flag: "/flags/mg.png" },
];

const currentLocale = computed(
  () => locales.find((l) => l.code === locale.value) ?? locales[0]
);

const selectLocale = async (code: string) => {
  await setLocale(code);
  open.value = false;
};

// ─── États UI ─────────────────────────────────────────────────────────────────
const open            = ref(false);
const userMenuOpen    = ref(false);
const isMobileMenuOpen = ref(false);
const isScrolled      = ref(false);
const activeSpace     = ref('agriculture');

// ─── Logique de détection de l'espace actif ───────────────────────────
const updateActiveSpace = (p: string) => {
  if (p.startsWith('/organization')) {
    activeSpace.value = 'organisation';
  } else if (p.startsWith('/farmer')) {
    activeSpace.value = 'agriculture';
  } else if (p.startsWith('/admin')) {
    activeSpace.value = 'admin';
  }
};

// Initialisation immédiate
updateActiveSpace(route.path);

// Suivi de la navigation pour mettre à jour l'espace actif
watch(() => route.path, (newPath) => {
  updateActiveSpace(newPath);
});

// ─── Utilisateur connecté ─────────────────────────────────────────────────────
const user = ref<{ first_name: string; email: string } | null>(null);

const rolePath = computed(() => {
  if (activeSpace.value === 'organisation') return 'organization';
  if (activeSpace.value === 'agriculture') return 'farmer';
  return 'admin';
});

// ─── Menu utilisateur ─────────────────────────────────────────────────────────
const userMenuItems = computed(() => [
  { labelKey: "dashboard.account", icon: "bx bx-user",    action: () => router.push(`/${rolePath.value}/profil`) },
  { labelKey: "dashboard.policy",  icon: "bx bx-shield",  action: () => router.push(`/${rolePath.value}/help/conditions/privacy-policy`) },
  { labelKey: "dashboard.terms",   icon: "bx bx-file",    action: () => router.push(`/${rolePath.value}/help/conditions/terms-of-service`) },
  { labelKey: "dashboard.signOut", icon: "bx bx-log-out", action: logout, danger: true },
]);

function handleMenuClick(item: { action: () => void }) {
  item.action();
  userMenuOpen.value = false;
}

async function logout() {
  await authStore.clearUserData();
  navigateTo("/");
}

// ─── Navigation mobile ────────────────────────────────────────────────────────
function goTo(path: string) {
  router.push(path);
  isMobileMenuOpen.value = false;
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// ─── Fermeture des dropdowns au clic en dehors ────────────────────────────────
function handleOutsideClick(e: MouseEvent) {
  const target = e.target as HTMLElement;
  if (!target.closest("[data-lang-dropdown]")) open.value = false;
  if (!target.closest("[data-user-dropdown]")) userMenuOpen.value = false;
}

// ─── Sidebar menu ─────────────────────────────────────────────────────────────
const sidebarMenu = computed(() => {
  const spaces = authStore.spaces || { agriculture: true };

  if (spaces.superviseur) {
    return [
      { to: "/admin",        icon: "bx bxs-dashboard",   label: "Dashboard" },
      { to: "/admin/users",  icon: "bx bx-user-pin",     label: "Utilisateurs" },
      { to: "/admin/audits", icon: "bx bx-check-shield", label: "Validations" },
      { to: "/admin/rapports",     icon: "bx bx-folder-open",  label: "Archive Rapports" },
    ];
  }

  const items: any[] = [];

  if (activeSpace.value === 'agriculture' && spaces.agriculture) {
    items.push(
      { to: "/farmer/dashboard",      icon: "bx bxs-dashboard",     label: t("dashboard.dashboard") },
      { to: "/farmer/crops",          icon: "bx bx-leaf",            label: t("dashboard.crops") },
      { to: "/farmer/parcels",        icon: "bx bx-location-alt-2",  label: t("dashboard.parcels") },
      { to: "/farmer/parcel-crops",   icon: "bx bx-layers",          label: t("dashboard.parcelCrops") },
      { to: "/farmer/tasks",          icon: "bx bx-task",            label: t("dashboard.tasks") },
      { to: "/farmer/yield-records",  icon: "bx bx-bar-chart",       label: t("dashboard.yields") },
      { to: "/farmer/organisations",  icon: "bx bx-buildings",       label: t("dashboard.organisations") },
      { to: "/farmer/invitations",    icon: "bx bx-envelope",        label: t("dashboard.invitations") },
      { to: "/farmer/marketplace",    icon: "bx bx-store",           label: t("dashboard.marketplace") },
    );
  }

  if (activeSpace.value === 'organisation' && spaces.organisation) {
    items.push(
      { to: "/organization/dashboard",   icon: "bx bxs-dashboard",      label: "Dashboard" },
      { to: "/organization/groups",      icon: "bx bx-group",           label: "Groupes" },
      { to: "/organization/recruitment", icon: "bx bx-search-alt",      label: "Recrutement" },
      { to: "/organization/requests",    icon: "bx bx-envelope",      label: "Boîte d'invitations" },
      { to: "/organization/indicators",  icon: "bx bx-bar-chart-alt-2", label: "Suivi Indicateurs" },
    );
  }

  return items;
});

// ─── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    await navigateTo("/login");
    return;
  }

  try {
    const data: any = await apiFetch(`/api/users/${authStore.uuid}/`);
    user.value = { first_name: data.first_name, email: data.email };

    if (data.spaces) {
      authStore.setUserData({ spaces: data.spaces });
    }
  } catch (err) {
    console.error("Impossible de charger l'utilisateur :", err);
    await navigateTo("/login");
  }

  window.addEventListener("scroll", handleScroll);
  document.addEventListener("click", handleOutsideClick);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  document.removeEventListener("click", handleOutsideClick);
});

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};
</script>

<style scoped>
::-webkit-scrollbar       { width: 3px; }
::-webkit-scrollbar-thumb { background-color: transparent; border-radius: 10px; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>