<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- Left sidebar -->
      <aside class="profile-sidebar" :class="{ loaded: isLoaded }">
        <div class="avatar-wrapper">
          <div class="avatar-ring"></div>
          <div class="avatar">
            <span class="avatar-initial">{{ user?.username?.charAt(0).toUpperCase() || '?' }}</span>
          </div>
        </div>

        <div class="sidebar-name">
          <h1>{{ user?.first_name }} <span>{{ user?.last_name }}</span></h1>
          <p class="sidebar-email">{{ user?.email }}</p>
        </div>

        <div class="sidebar-badge">
          <i class="bx bx-check-shield"></i>
          Compte vérifié
        </div>

        <nav class="sidebar-nav">
          <NuxtLink :to="`/${role}/profil/edit`" class="nav-item nav-item--primary">
            <i class="bx bx-edit-alt"></i>
            <span>{{ t("editProfile") }}</span>
            <i class="bx bx-chevron-right nav-arrow"></i>
          </NuxtLink>
        </nav>

        <button class="logout-btn" @click.prevent="logout">
          <i class="bx bx-log-out"></i>
          {{ t("logout") }}
        </button>

        <div class="sidebar-links">
          <NuxtLink :to="`/${role}/help/conditions/terms-of-service`">{{ t("terms") }}</NuxtLink>
          <span class="dot">·</span>
          <NuxtLink :to="`/${role}/help/conditions/privacy-policy`">{{ t("policy") }}</NuxtLink>
        </div>
      </aside>

      <!-- Main content -->
      <main class="profile-main" :class="{ loaded: isLoaded }">
        <div class="section-header">
          <span class="section-label">INFORMATIONS PERSONNELLES</span>
          <div class="section-line"></div>
        </div>

        <div class="info-grid">
          <div class="info-card" style="--delay: 0.1s">
            <div class="info-icon"><i class="bx bx-user-circle"></i></div>
            <div class="info-content">
              <label>{{ t("firstName") }}</label>
              <p>{{ user?.first_name || '—' }}</p>
            </div>
          </div>

          <div class="info-card" style="--delay: 0.2s">
            <div class="info-icon"><i class="bx bx-id-card"></i></div>
            <div class="info-content">
              <label>{{ t("lastName") }}</label>
              <p>{{ user?.last_name || '—' }}</p>
            </div>
          </div>

          <div class="info-card info-card--wide" style="--delay: 0.3s">
            <div class="info-icon"><i class="bx bx-envelope"></i></div>
            <div class="info-content">
              <label>{{ t("email") }}</label>
              <p>{{ user?.email || '—' }}</p>
            </div>
            <span class="verified-tag"><i class="bx bx-check"></i> Vérifié</span>
          </div>
        </div>

        <div class="section-header" style="margin-top: 2rem;">
          <span class="section-label">SÉCURITÉ</span>
          <div class="section-line"></div>
        </div>

        <div class="security-card" @click="$router.push(`/${role}/profil/edit/reset-password`)">
          <div class="security-left">
            <div class="security-icon"><i class="bx bx-lock-alt"></i></div>
            <div>
              <h3>Mot de passe</h3>
              <p>Dernière modification inconnue</p>
            </div>
          </div>
          <button class="security-btn">Modifier <i class="bx bx-chevron-right"></i></button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
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
    setTimeout(() => (isLoaded.value = true), 100);
  } catch (err) {
    console.error(err);
  }
});

const logout = async () => {
  await authStore.clearUserData();
  router.push("/login");
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:wght@600;700&display=swap');

.profile-page {
  min-height: 100%;
  background: white;
  font-family: 'DM Sans', sans-serif;
  padding: 1.5rem 0;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 850px) {
  .profile-container { grid-template-columns: 1fr; }
}

.profile-sidebar {
  background: white; border-radius: 24px; padding: 2.5rem 1.5rem;
  display: flex; flex-direction: column; align-items: center; gap: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #f1f5f9;
  opacity: 0; transform: translateY(10px); transition: all 0.5s ease;
}
.profile-sidebar.loaded { opacity: 1; transform: translateY(0); }

.avatar-wrapper { position: relative; }
.avatar {
  width: 96px; height: 96px; border-radius: 50%; background: #10b481;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 15px 30px rgba(16, 180, 129, 0.2);
}
.avatar-initial {
  font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 700; color: white;
}

.sidebar-name { text-align: center; }
.sidebar-name h1 { font-family: 'Fraunces', serif; font-size: 1.5rem; color: #111; }
.sidebar-email { font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem; }

.sidebar-badge {
  display: flex; align-items: center; gap: 6px; background: #f0fdf4;
  border: 1px solid #dcfce7; color: #166534; font-size: 0.7rem;
  font-weight: 800; text-transform: uppercase; padding: 0.4rem 0.8rem; border-radius: 100px;
}

.sidebar-nav { width: 100%; display: flex; flex-direction: column; gap: 0.5rem; }
.nav-item {
  display: flex; align-items: center; gap: 1rem; padding: 1rem; border-radius: 16px;
  font-size: 0.9rem; font-weight: 600; color: #4b5563; text-decoration: none;
  transition: all 0.2s; border: 1px solid transparent;
}
.nav-item:hover { background: #f8fafc; border-color: #f1f5f9; color: #10b481; }
.nav-item--primary { background: #f0fdf4; color: #10b481; border-color: #dcfce7; }
.nav-arrow { margin-left: auto; font-size: 1.25rem; opacity: 0.3; }

.logout-btn {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.75rem;
  padding: 1rem; background: #fef2f2; border: 1px solid #fee2e2; border-radius: 16px;
  color: #ef4444; font-weight: 700; font-size: 0.9rem; cursor: pointer; transition: all 0.2s;
}
.logout-btn:hover { background: #fee2e2; transform: scale(0.98); }

.sidebar-links { display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #94a3b8; }
.sidebar-links a { color: #94a3b8; text-decoration: none; font-weight: 600; }
.sidebar-links a:hover { color: #10b481; }

.profile-main {
  display: flex; flex-direction: column; gap: 1.5rem;
  opacity: 0; transform: translateY(10px); transition: all 0.5s ease 0.1s;
}
.profile-main.loaded { opacity: 1; transform: translateY(0); }

.section-header { display: flex; align-items: center; gap: 1rem; }
.section-label { font-size: 0.7rem; font-weight: 800; color: #10b481; letter-spacing: 0.1em; }
.section-line { flex: 1; height: 1px; background: #f1f5f9; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.info-card--wide { grid-column: 1 / -1; }
.info-card {
  background: white; border-radius: 20px; padding: 1.5rem;
  display: flex; align-items: center; gap: 1rem; border: 1px solid #f1f5f9;
  transition: all 0.3s;
}
.info-card:hover { border-color: #10b481; transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.03); }

.info-icon {
  width: 44px; height: 44px; border-radius: 12px; background: #f8fafc;
  display: flex; align-items: center; justify-content: center; color: #10b481; font-size: 1.5rem;
}

.info-content label { display: block; font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.25rem; }
.info-content p { font-size: 1rem; font-weight: 700; color: #111827; }

.verified-tag {
  margin-left: auto; display: flex; align-items: center; gap: 4px;
  background: #f0fdf4; color: #166534; font-size: 0.65rem; font-weight: 800;
  padding: 0.4rem 0.8rem; border-radius: 100px;
}

.security-card {
  background: white; border-radius: 20px; padding: 1.5rem;
  display: flex; align-items: center; justify-content: space-between;
  border: 1px solid #f1f5f9; cursor: pointer; transition: all 0.3s;
}
.security-card:hover { border-color: #10b481; }
.security-left { display: flex; align-items: center; gap: 1rem; }
.security-icon {
  width: 44px; height: 44px; border-radius: 12px; background: #fff7ed;
  display: flex; align-items: center; justify-content: center; color: #f97316; font-size: 1.5rem;
}
.security-left h3 { font-size: 1rem; font-weight: 700; color: #111827; }
.security-left p { font-size: 0.8rem; color: #94a3b8; }

.security-btn {
  padding: 0.6rem 1.25rem; background: #f8fafc; border: 1px solid #e2e8f0;
  border-radius: 12px; font-size: 0.85rem; font-weight: 700; color: #4b5563;
  display: flex; align-items: center; gap: 4px; cursor: pointer;
}

@media (max-width: 600px) {
  .info-grid { grid-template-columns: 1fr; }
  .verified-tag { display: none; }
}
</style>
