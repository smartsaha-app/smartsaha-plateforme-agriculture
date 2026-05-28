<template>
  <div class="h-screen bg-[#fefefe] flex flex-col font-['Readex_Pro']">

    <!-- ═══════════════════════════════════════════
         HEADER — Barre de navigation supérieure fixe
         ═══════════════════════════════════════════ -->
    <header
      class="fixed top-0 left-0 right-0 z-50 flex items-center px-4 sm:px-8 h-16 bg-[#fefefe] border-b border-gray-100 shadow-sm"
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

      <!-- Conteneur global des actions (Panier + Desktop Actions) -->
      <div class="ml-auto flex items-center gap-4 sm:gap-6">
        
        <!-- Icône Panier (Visible Espace Acheteur, Mobile et Desktop) -->
        <ClientOnly>
          <button
            v-if="activeSpace === 'buyer'"
            @click="router.push('/buyer/cart')"
            class="relative p-2 text-gray-700 hover:text-[#10b481] transition-colors flex items-center justify-center"
          >
            <i class="bx bx-cart text-[1.6rem]"></i>
            <!-- Badge -->
            <span 
              v-if="cartItemCount > 0"
              class="absolute top-0 right-0 translate-x-1/4 -translate-y-1/4 bg-red-500 text-white text-[10px] font-bold min-w-[20px] h-5 px-1 flex items-center justify-center rounded-full border-2 border-white"
            >
              {{ cartItemCount }}
            </span>
          </button>
        </ClientOnly>

        <!-- Actions header (desktop uniquement) -->
        <div class="hidden sm:flex items-center gap-6">

        <!-- Sélecteur de langue -->
        <div class="relative" data-lang-dropdown>
          <button
            @click="open = !open"
            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-gray-100 transition-colors duration-150"
          >
            <img v-if="currentLocale" :src="currentLocale.flag" alt="" class="w-5 h-5 rounded-full" />
            <span class="text-sm font-medium text-gray-600">{{ currentLocale?.code?.toUpperCase() }}</span>
            <i class="bx bx-chevron-down text-gray-400 text-sm"></i>
          </button>
          <transition name="fade">
            <ul v-if="open" class="absolute right-0 mt-1.5 w-36 bg-white border border-gray-100 rounded-xl shadow-lg overflow-hidden z-50 p-1">
              <li
                v-for="loc in locales"
                :key="loc.code"
                @click="selectLocale(loc.code)"
                class="flex items-center gap-2.5 px-3 py-2 cursor-pointer hover:bg-gray-50 rounded-lg transition-colors"
              >
                <img :src="loc.flag" alt="" class="w-4 h-4 rounded-full" />
                <span class="text-sm font-medium text-gray-700">{{ loc.name }}</span>
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
              <span class="text-white text-sm font-bold tracking-wide">{{ userInitials }}</span>
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
                <div class="w-9 h-9 rounded-full bg-[#10b481] flex items-center justify-center text-white flex-shrink-0">
                  <span class="text-xs font-bold tracking-wide">{{ userInitials }}</span>
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
          <div class="h-10 w-10 rounded-full bg-[#10b481] flex items-center justify-center">
            <span class="text-white text-sm font-bold tracking-wide">{{ userInitials }}</span>
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
          <label class="text-white text-sm mb-1 block">{{ t("dashboard.language") }}</label>
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
          v-if="activeSpace !== 'agriculture'"
          @click="goTo(`/${rolePath}/assistant`)"
          :class="[
            'flex items-center gap-3 px-3 py-2 rounded-lg w-full text-left transition-all duration-200',
            isActive(`/${rolePath}/assistant`) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
          ]"
        >
          <i class="bx bx-robot text-[1.1rem] flex-shrink-0"></i>
          <span class="text-sm font-medium">Sesily</span>
        </button>

        <template v-for="(item, index) in sidebarMenu" :key="'m_'+index">
          <button
            v-if="item.isHeader"
            @click="toggleGroup(item.group)"
            class="flex items-center justify-between px-3 py-1.5 mt-4 mb-0.5 w-full text-xs font-semibold text-gray-400 tracking-wide hover:text-gray-200 transition-colors duration-150"
          >
            <span>{{ item.label }}</span>
            <i :class="['bx bx-chevron-down text-sm transition-transform duration-200', openGroups[item.group] ? 'rotate-0' : '-rotate-90']"></i>
          </button>
          <button
            v-else
            v-show="!item.group || openGroups[item.group]"
            @click="goTo(item.to)"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg w-full text-left transition-all duration-200',
              isActive(item.to) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
            ]"
          >
            <i :class="[item.icon, 'text-[1.1rem] flex-shrink-0', item.iconColor || '']"></i>
            <span class="text-sm font-medium flex-1">{{ item.label }}</span>
            <span v-if="item.badge" class="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-[#10b481]/20 text-[#10b481]">{{ item.badge }}</span>
          </button>
        </template>

        <button
          @click="logout"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-white/70 hover:bg-red-500/20 hover:text-red-400 transition-all duration-200"
        >
          <i class="bx bx-log-out text-[1.1rem]"></i>
          <span class="text-sm font-medium">{{ t("dashboard.logout") }}</span>
        </button>
      </nav>
    </aside>
    <!-- FIN MENU MOBILE -->


    <!-- ═══════════════════════════════════════════
         LAYOUT PRINCIPAL — Sidebar fixe + Contenu
         ═══════════════════════════════════════════ -->
    <div class="flex flex-1 pt-16">

      <aside class="hidden sm:flex fixed top-16 left-0 h-[calc(100vh-4rem)] flex-col bg-[#112830] shadow-lg w-56 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
        <nav class="flex flex-col space-y-1 py-4">
          <template v-for="(item, index) in sidebarMenu" :key="index">
            <button
              v-if="item.isHeader"
              @click="toggleGroup(item.group)"
              class="flex items-center justify-between px-4 py-1.5 mt-5 mb-1 w-full text-xs font-semibold text-gray-400 tracking-wide hover:text-gray-200 transition-colors duration-150"
            >
              <span>{{ item.label }}</span>
              <i :class="['bx bx-chevron-down text-sm transition-transform duration-200', openGroups[item.group] ? 'rotate-0' : '-rotate-90']"></i>
            </button>
            <button
              v-else
              v-show="!item.group || openGroups[item.group]"
              @click="router.push(item.to)"
              :class="[
                'flex items-center gap-3 mx-2 px-3 py-2 rounded-lg transition-all duration-200 w-[calc(100%-1rem)] text-left',
                isActive(item.to) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
              ]"
            >
              <i :class="[item.icon, 'text-[1.1rem] flex-shrink-0', item.iconColor || '']"></i>
              <span class="font-medium text-sm flex-1">{{ item.label }}</span>
              <span v-if="item.badge" class="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-[#10b481]/20 text-[#10b481]">{{ item.badge }}</span>
            </button>
          </template>
        </nav>

        <!-- Bas de la sidebar -->
        <div class="mt-auto flex flex-col space-y-1 px-2 py-4">
          <button
            v-if="activeSpace !== 'agriculture'"
            @click="router.push(`/${rolePath}/profil`)"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 w-full text-left',
              isActive(`/${rolePath}/profil`) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
            ]"
          >
            <i class="bx bx-user text-[1.1rem] flex-shrink-0"></i>
            <span class="font-medium text-sm">{{ t("dashboard.myProfile") }}</span>
          </button>

          <button
            v-if="['organisation', 'admin'].includes(activeSpace)"
            @click="router.push(`/${rolePath}/assistant`)"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 w-full text-left',
              isActive(`/${rolePath}/assistant`) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
            ]"
          >
            <i class="bx bx-robot text-[1.1rem] flex-shrink-0"></i>
            <span class="font-medium text-sm">{{ t("dashboard.assistantAI") }}</span>
          </button>

          <button
            v-if="activeSpace !== 'agriculture'"
            @click="router.push(`/${rolePath}/help`)"
            :class="[
              'flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 w-full text-left',
              isActive(`/${rolePath}/help`) ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
            ]"
          >
            <i class="bx bx-info-circle text-[1.1rem] flex-shrink-0"></i>
            <span class="font-medium text-sm">{{ t("dashboard.help") }}</span>
          </button>
        </div>
      </aside>

      <main class="flex-1 p-6 sm:ml-56">
        <slot />
      </main>
    </div>
    <!-- FIN LAYOUT PRINCIPAL -->

    <!-- ===== BOUTON FLOTTANT SESILY AI ===== -->
    <ClientOnly>
      <Transition name="fab">
        <button
          v-if="activeSpace === 'agriculture'"
          @click="router.push('/farmer/assistant')"
          class="fixed bottom-6 right-6 z-50 flex items-center gap-3 pl-2 pr-5 py-2 bg-[#112830] text-white rounded-2xl shadow-2xl shadow-[#112830]/40 hover:bg-[#10b481] hover:shadow-[#10b481]/30 transition-all duration-300 group"
          :class="isActive('/farmer/assistant') ? 'bg-[#10b481] shadow-[#10b481]/30' : ''"
          title="Sesily — Assistant IA"
        >
          <div class="w-9 h-9 rounded-xl bg-[#10b481] group-hover:bg-white/20 flex items-center justify-center transition-colors shrink-0"
               :class="isActive('/farmer/assistant') ? 'bg-white/20' : ''">
            <i class="bx bx-robot text-white text-xl"></i>
          </div>
          <div class="flex flex-col items-start">
            <span class="text-[9px] font-black text-white/50 uppercase tracking-widest leading-none">Assistant IA</span>
            <span class="text-sm font-black leading-tight tracking-tight">Sesily</span>
          </div>
          <span class="ml-1 text-[8px] font-black px-1.5 py-0.5 bg-[#10b481] group-hover:bg-white/20 rounded-full uppercase tracking-widest transition-colors"
                :class="isActive('/farmer/assistant') ? 'bg-white/20' : ''">IA</span>
        </button>
      </Transition>
    </ClientOnly>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
import { useMarketplace } from "~/composables/useMarketplace";

// ─── Router & Store & i18n ───────────────────────────────────────────────────
const router      = useRouter();
const route       = useRoute();
const authStore   = useAuthStore();
const { apiFetch } = useApi();
const { t, locale, setLocale } = useI18n();
const { cart, cartItemCount, fetchCart, clearMarketplaceState } = useMarketplace();

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

const openGroups = reactive<Record<string, boolean>>({
  exploitation: true,
  marketplace: true,
  reseau: true,
  support: true,
});

function toggleGroup(group: string) {
  if (group in openGroups) openGroups[group] = !openGroups[group];
}

// ─── Logique de détection de l'espace actif ───────────────────────────
const updateActiveSpace = (p: string) => {
  if (p.startsWith('/organization')) {
    activeSpace.value = 'organisation';
  } else if (p.startsWith('/farmer')) {
    activeSpace.value = 'agriculture';
  } else if (p.startsWith('/buyer')) {
    activeSpace.value = 'buyer';
  } else if (p.startsWith('/seller')) {
    activeSpace.value = 'seller';
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

const userInitials = computed(() => {
  if (!user.value?.first_name) return '?';
  const parts = user.value.first_name.trim().split(' ').filter(Boolean);
  if (parts.length === 0) return '?';
  const a = parts[0]?.charAt(0) ?? '';
  const b = parts[1]?.charAt(0) ?? '';
  return parts.length >= 2 ? (a + b).toUpperCase() : (parts[0] ?? '').slice(0, 2).toUpperCase();
});

const rolePath = computed(() => {
  if (activeSpace.value === 'organisation') return 'organization';
  if (activeSpace.value === 'agriculture') return 'farmer';
  if (activeSpace.value === 'buyer') return 'buyer';
  if (activeSpace.value === 'seller') return 'seller';
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
  clearMarketplaceState(); // Nettoyer les données du panier/commandes de l'utilisateur
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
  const userRole = authStore.user?.role;
  const spaces = authStore.spaces || { agriculture: true };
  const items: any[] = [];

  if (activeSpace.value === 'seller') {
    items.push(
      { to: "/seller/dashboard", icon: "bx bxs-dashboard",   label: t("dashboard.dashboard") },
      { to: "/seller/products",  icon: "bx bx-store",        label: t("dashboard.myProducts") },
      { to: "/seller/orders",    icon: "bx bx-shopping-bag", label: t("dashboard.receivedOrders") },
      { to: "/seller/payments",  icon: "bx bx-wallet",       label: "Mes Revenus" },
      { to: "/seller/history",   icon: "bx bx-history",      label: t("dashboard.history") },
    );
  } else if (activeSpace.value === 'agriculture' && spaces.agriculture) {
    items.push(
      { to: "/farmer/dashboard", icon: "bx bxs-dashboard", label: t("dashboard.dashboard") },

      { isHeader: true, label: "Exploitation", group: "exploitation" },
      { to: "/farmer/crops",   icon: "bx bx-leaf",    label: t("dashboard.crops"),   group: "exploitation" },
      { to: "/farmer/parcels", icon: "bx bx-map-alt", label: t("dashboard.parcels"), group: "exploitation" },

      { isHeader: true, label: "Marketplace", group: "marketplace" },
      { to: "/farmer/marketplace/products", icon: "bx bx-store",        label: "Produits",   group: "marketplace" },
      { to: "/farmer/marketplace/orders",   icon: "bx bx-shopping-bag", label: "Commandes",    group: "marketplace" },
      { to: "/farmer/marketplace/payments", icon: "bx bx-wallet",       label: "Revenus",      group: "marketplace" },
      { to: "/farmer/marketplace/history",  icon: "bx bx-history",      label: "Historique",   group: "marketplace" },

      { isHeader: true, label: "Réseau", group: "reseau" },
      { to: "/farmer/organisations", icon: "bx bx-buildings", label: t("dashboard.organisations"), group: "reseau" },
      { to: "/farmer/invitations",   icon: "bx bx-envelope",  label: t("dashboard.invitations"),   group: "reseau" },
    );
  } else if (activeSpace.value === 'organisation') {
    items.push(
      { to: "/organization/dashboard",   icon: "bx bxs-dashboard",      label: t("dashboard.dashboard") },
      { to: "/organization/groups",      icon: "bx bx-group",           label: t("dashboard.groups") },
      { to: "/organization/recruitment", icon: "bx bx-search-alt",      label: t("dashboard.recruitment") },
      { to: "/organization/requests",    icon: "bx bx-envelope",      label: t("dashboard.invitationBox") },
      { to: "/organization/indicators",  icon: "bx bx-bar-chart-alt-2", label: t("dashboard.indicatorTracking") },
    );
  } else if (activeSpace.value === 'buyer') {
    items.push(
      { to: "/buyer/dashboard",   icon: "bx bxs-dashboard",      label: t("dashboard.dashboard") },
      { to: "/buyer/products",    icon: "bx bx-store",           label: t("dashboard.products") },
      { to: "/buyer/cart",        icon: "bx bx-cart",            label: t("dashboard.cart") },
      { to: "/buyer/orders",      icon: "bx bx-shopping-bag",    label: t("dashboard.orders") },
      { to: "/buyer/payments",    icon: "bx bx-wallet",          label: "Paiements" },
      { to: "/buyer/history",     icon: "bx bx-history",         label: t("dashboard.history") }
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

    authStore.setUserData({
      first_name: data.first_name,
      ...(data.spaces ? { spaces: data.spaces } : {}),
    });
  } catch (err) {
    console.error("Impossible de charger l'utilisateur :", err);
    await navigateTo("/login");
  }

  window.addEventListener("scroll", handleScroll);
  document.addEventListener("click", handleOutsideClick);

  // Load cart if in buyer space
  if (activeSpace.value === 'buyer') {
    fetchCart();
  }
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

.fab-enter-active { transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.fab-leave-active { transition: all 0.2s ease; }
.fab-enter-from, .fab-leave-to { opacity: 0; transform: translateY(1rem) scale(0.8); }

.bx-chevron-down { transition: transform 0.2s ease; }
</style>