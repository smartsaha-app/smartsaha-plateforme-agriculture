<template>
  <div class="policy-page">
    <div class="bg-mesh"></div>

    <div class="content-wrapper p-4 sm:p-6">
      <!-- ===== HEADER ===== -->
      <div class="mb-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl sm:text-3xl font-bold mb-6 text-[#212121] flex items-center gap-2">
            Politique de Confidentialité
          </h2>
          <nav class="flex items-center gap-2 text-sm text-gray-500 mb-4" aria-label="Breadcrumb">
            <NuxtLink :to="`/${role}/dashboard`" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
              <i class="bx bx-home text-base"></i>
              <span>Accueil</span>
            </NuxtLink>
            <i class="bx bx-chevron-right text-gray-400 text-base"></i>
            <NuxtLink :to="`/${role}/help`" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
              <span>Aide</span>
            </NuxtLink>
            <i class="bx bx-chevron-right text-gray-400 text-base"></i>
            <span class="text-[#10b481] font-medium">Confidentialité</span>
          </nav>
        </div>
      </div>

      <!-- ===== HERO BANNER ===== -->
      <div class="hero-banner">
        <div class="hero-icon-wrap">
          <i class="bx bx-shield-quarter"></i>
        </div>
        <div class="hero-text">
          <h1 class="hero-title">{{ t("policy") }}</h1>
          <p class="hero-date">
            <i class="bx bx-calendar"></i>
            {{ t("policyDate") }}
          </p>
        </div>
        <div class="hero-deco" aria-hidden="true">
          <svg width="160" height="160" viewBox="0 0 160 160" fill="none">
            <circle cx="80" cy="80" r="72" stroke="rgba(255,255,255,0.15)" stroke-width="1.5" stroke-dasharray="10 5"/>
            <circle cx="80" cy="80" r="48" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
            <circle cx="80" cy="80" r="20" fill="rgba(255,255,255,0.08)"/>
          </svg>
        </div>
      </div>

      <!-- ===== MAIN LAYOUT ===== -->
      <div class="main-layout">
        <!-- ===== SIDEBAR TOC ===== -->
        <aside class="toc-sidebar">
          <div class="toc-card">
            <div class="toc-header">
              <i class="bx bx-list-ul"></i>
              <span>Sommaire</span>
            </div>
            <nav class="toc-list">
              <a
                v-for="i in 7"
                :key="i"
                :href="`#section-${i}`"
                class="toc-item"
                :class="{ active: activeSection === i }"
                @click="activeSection = i"
              >
                <span class="toc-num">{{ String(i).padStart(2, '0') }}</span>
                <span class="toc-label" v-html="t(`policy${i}Title`)"></span>
                <i class="bx bx-chevron-right toc-arrow"></i>
              </a>
            </nav>
          </div>
        </aside>

        <!-- ===== SECTIONS ===== -->
        <div class="sections-wrapper">
          <section
            v-for="i in 7"
            :key="i"
            :id="`section-${i}`"
            class="policy-section"
            :style="`--delay: ${(i - 1) * 60}ms`"
          >
            <div class="section-header">
              <div class="section-badge">
                <span>{{ String(i).padStart(2, '0') }}</span>
              </div>
              <h2 class="section-title" v-html="t(`policy${i}Title`)"></h2>
            </div>
            <div class="section-divider"></div>
            <p class="section-text" v-html="t(`policy${i}Text`)"></p>
          </section>

          <!-- ===== FOOTER NOTE ===== -->
          <div class="footer-note">
            <i class="bx bx-info-circle"></i>
            <p>
              Pour toute question concernant cette politique de confidentialité, veuillez nous contacter à
              <a href="mailto:contact@smart-saha.com" class="footer-link">contact@smart-saha.com</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const props = defineProps<{
  role: string;
}>();

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const activeSection = ref(1);

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          const num = parseInt(id.replace("section-", ""));
          if (!isNaN(num)) activeSection.value = num;
        }
      });
    },
    { threshold: 0.4 }
  );
  for (let i = 1; i <= 7; i++) {
    const el = document.getElementById(`section-${i}`);
    if (el) observer.observe(el);
  }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

.policy-page {
  font-family: 'Plus Jakarta Sans', sans-serif;
  min-height: 100%;
  position: relative;
}

.content-wrapper {
  position: relative;
  max-width: 1060px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero-banner {
  background: linear-gradient(135deg, #0a8a5c 0%, #10b481 55%, #34d399 100%);
  border-radius: 20px;
  padding: 2.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(16, 180, 129, 0.2);
}

.hero-icon-wrap {
  width: 56px; height: 56px;
  background: rgba(255,255,255,0.2);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(8px);
}
.hero-icon-wrap i { font-size: 1.7rem; color: white; }

.hero-title { font-size: 1.75rem; font-weight: 800; color: white; margin-bottom: 0.4rem; }
.hero-date { font-size: 0.85rem; color: rgba(255, 255, 255, 0.8); display: flex; align-items: center; gap: 6px; }

.main-layout {
  display: grid; grid-template-columns: 220px 1fr; gap: 2rem; align-items: start;
}

.toc-sidebar { position: sticky; top: 2rem; }
.toc-card { background: white; border-radius: 16px; border: 1px solid #f1f5f9; overflow: hidden; }
.toc-header { padding: 1rem; background: #f8fafc; border-bottom: 1px solid #f1f5f9; font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; font-family: 'DM Mono', monospace; }

.toc-item {
  display: flex; align-items: center; gap: 8px; padding: 0.8rem 1rem; text-decoration: none; border-bottom: 1px solid #f8fafc; transition: all 0.2s; color: #64748b;
}
.toc-item.active { background: #f0fdf4; color: #10b481; font-weight: 700; border-left: 3px solid #10b481; }

.toc-label { font-size: 0.85rem; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.sections-wrapper { display: flex; flex-direction: column; gap: 1.5rem; }
.policy-section { background: white; border-radius: 20px; border: 1px solid #f1f5f9; padding: 2rem; scroll-margin-top: 100px; }
.policy-section:hover { border-color: #10b481; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }

.section-badge { width: 32px; height: 32px; background: #f0fdf4; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; }
.section-badge span { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #10b481; font-weight: 700; }

.section-title { font-size: 1.15rem; font-weight: 800; color: #111827; margin-bottom: 1rem; }
.section-text { font-size: 0.95rem; color: #4b5563; line-height: 1.8; }

.footer-note { background: #f0fdf4; border: 1px solid #dcfce7; border-radius: 16px; padding: 1.25rem; display: flex; gap: 12px; }
.footer-note i { color: #10b481; font-size: 1.25rem; }
.footer-note p { font-size: 0.9rem; color: #166534; line-height: 1.6; }

@media (max-width: 768px) {
  .main-layout { grid-template-columns: 1fr; }
  .toc-sidebar { position: static; }
}
</style>
