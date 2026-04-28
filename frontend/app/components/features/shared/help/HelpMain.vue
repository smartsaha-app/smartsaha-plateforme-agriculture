<template>
  <div class="help-page">
    <div class="content-wrapper p-4 sm:p-6">
      <!-- ===== HEADER ===== -->
      <div class="mb-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl sm:text-3xl font-bold mb-6 text-[#212121] flex items-center gap-2">
            Aide & Guide
          </h2>

          <nav class="flex items-center gap-2 text-sm text-gray-500 mb-4" aria-label="Breadcrumb">
            <NuxtLink
              :to="`/${role}/dashboard`"
              class="flex items-center gap-1 hover:text-[#10b481] transition-colors"
            >
              <i class="bx bx-home text-base"></i>
              <span>Accueil</span>
            </NuxtLink>
            <i class="bx bx-chevron-right text-gray-400 text-base"></i>
            <span class="text-[#10b481] font-medium">Aide</span>
          </nav>
        </div>
      </div>

      <!-- ===== WELCOME BANNER ===== -->
      <div class="welcome-banner">
        <div class="welcome-icon">
          <i class="bx bx-info-circle"></i>
        </div>
        <div class="welcome-text">
          <h3>{{ t("welcomehelp") }}</h3>
          <p>
            {{ t("introhelp") }}
            <a href="https://www.smart-saha.com" target="_blank" class="inline-link">
              www.smart-saha.com
            </a>.
          </p>
        </div>
        <div class="welcome-decoration">
          <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
            <circle cx="60" cy="60" r="55" stroke="rgba(16,180,129,0.15)" stroke-width="2" stroke-dasharray="8 4"/>
            <circle cx="60" cy="60" r="35" stroke="rgba(16,180,129,0.1)" stroke-width="1"/>
            <circle cx="60" cy="60" r="10" fill="rgba(16,180,129,0.2)"/>
          </svg>
        </div>
      </div>

      <!-- ===== HOW IT WORKS ===== -->
      <div class="section">
        <div class="section-header">
          <div class="section-label">
            <div class="label-dot"></div>
            <span>Processus</span>
          </div>
          <h2 class="section-title">{{ t("howitworks") }}</h2>
        </div>

        <div class="steps-grid">
          <div
            v-for="n in 6"
            :key="n"
            class="step-card"
            :style="`--delay: ${(n - 1) * 80}ms`"
          >
            <div class="step-number">{{ String(n).padStart(2, '0') }}</div>
            <div class="step-icon-wrap">
              <i :class="`bx ${stepIcons[n - 1]}`"></i>
            </div>
            <div class="step-body">
              <h4 class="step-title">{{ t(`step${n}title`) }}</h4>
              <p class="step-text">{{ t(`step${n}text`) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== CONTACT ===== -->
      <div class="section">
        <div class="section-header">
          <div class="section-label">
            <div class="label-dot"></div>
            <span>Contact</span>
          </div>
          <h2 class="section-title">{{ t("needhelp") }}</h2>
          <p class="section-desc">{{ t("contactteam") }}</p>
        </div>

        <div class="contact-grid">
          <a href="https://wa.me/261327114865" target="_blank" class="contact-card contact-whatsapp">
            <div class="contact-icon">
              <i class="bx bx-message-circle-plus"></i>
            </div>
            <div class="contact-info">
              <span class="contact-type">WhatsApp</span>
              <span class="contact-value">+261 32 71 148 65</span>
            </div>
            <i class="bx bx-arrow-back contact-arrow"></i>
          </a>

          <a href="mailto:contact@smart-saha.com" class="contact-card contact-email">
            <div class="contact-icon">
              <i class="bx bx-envelope"></i>
            </div>
            <div class="contact-info">
              <span class="contact-type">Email</span>
              <span class="contact-value">contact@smart-saha.com</span>
            </div>
            <i class="bx bx-arrow-back contact-arrow"></i>
          </a>

          <div class="contact-card contact-location">
            <div class="contact-icon">
              <i class="bx bx-map"></i>
            </div>
            <div class="contact-info">
              <span class="contact-type">Localisation</span>
              <span class="contact-value">{{ t("location") }}</span>
            </div>
            <i class="bx bx-map-pin contact-arrow"></i>
          </div>
        </div>
      </div>

      <!-- ===== CONDITIONS ===== -->
      <div class="section">
        <div class="section-header">
          <div class="section-label">
            <div class="label-dot"></div>
            <span>Légal</span>
          </div>
          <h2 class="section-title">Conditions</h2>
        </div>

        <div class="legal-grid">
          <NuxtLink :to="`/${role}/help/conditions/privacy-policy`" class="legal-card">
            <div class="legal-icon">
              <i class="bx bx-shield-quarter"></i>
            </div>
            <div class="legal-content">
              <span class="legal-title">{{ t("policy") }}</span>
              <span class="legal-desc">Comment nous protégeons vos données</span>
            </div>
            <i class="bx bx-chevron-right legal-chevron"></i>
          </NuxtLink>

          <NuxtLink :to="`/${role}/help/conditions/terms-of-service`" class="legal-card">
            <div class="legal-icon">
              <i class="bx bx-file"></i>
            </div>
            <div class="legal-content">
              <span class="legal-title">{{ t("terms") }}</span>
              <span class="legal-desc">Comprenez vos droits et obligations</span>
            </div>
            <i class="bx bx-chevron-right legal-chevron"></i>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  role: string;
}>();

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const stepIcons = [
  "bx-user-plus",
  "bx-cloud-download",
  "bx-bar-chart-alt-2",
  "bx-task",
  "bx-show",
  "bx-file-blank",
];
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

.help-page {
  font-family: 'Plus Jakarta Sans', sans-serif;
  min-height: 100%;
  background: white;
}

.content-wrapper {
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.welcome-banner {
  background: linear-gradient(135deg, #0d9668 0%, #10b481 50%, #34d399 100%);
  border-radius: 24px;
  padding: 2.5rem;
  display: flex;
  gap: 1.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 40px -10px rgba(16, 180, 129, 0.3);
}

.welcome-decoration {
  position: absolute;
  right: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.4;
}

.welcome-icon {
  width: 50px; height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.3);
}
.welcome-icon i { font-size: 1.5rem; color: white; }

.welcome-text h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.5rem;
}
.welcome-text p {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

.section-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.75rem; font-weight: 800; color: #10b481;
  text-transform: uppercase; letter-spacing: 0.1em;
  font-family: 'DM Mono', monospace;
  margin-bottom: 0.5rem;
}

.label-dot { width: 6px; height: 6px; background: #10b481; border-radius: 50%; }

.section-title {
  font-size: 1.75rem; font-weight: 800; color: #111827;
  letter-spacing: -0.02em; margin-bottom: 1.5rem;
}

.steps-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem;
}

.step-card {
  background: #f8fafc; border-radius: 20px; padding: 2rem;
  border: 1px solid #f1f5f9; position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.step-card:hover {
  background: white; border-color: #10b481;
  box-shadow: 0 20px 40px -15px rgba(16, 180, 129, 0.1);
  transform: translateY(-5px);
}

.step-number {
  font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #10b481; font-weight: 700;
  margin-bottom: 1rem;
}

.step-icon-wrap {
  width: 44px; height: 44px; background: white; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 16px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.step-icon-wrap i { font-size: 1.25rem; color: #10b481; }

.step-title { font-size: 1.05rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem; }
.step-text { font-size: 0.9rem; color: #64748b; line-height: 1.6; }

.contact-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem;
}

.contact-card {
  background: white; border-radius: 20px; padding: 1.5rem;
  border: 1px solid #f1f5f9; display: flex; align-items: center; gap: 1.25rem;
  text-decoration: none; transition: all 0.3s;
}
.contact-card:hover {
  border-color: #10b481; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  transform: scale(1.02);
}

.contact-icon {
  width: 48px; height: 48px; background: #10b481; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 10px 20px -5px rgba(16, 180, 129, 0.4);
}
.contact-icon i { font-size: 1.5rem; color: white; }

.contact-type { font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.contact-value { font-size: 0.95rem; font-weight: 700; color: #111827; }

.legal-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1.25rem;
}

.legal-card {
  background: white; border-radius: 20px; padding: 1.5rem;
  border: 1px solid #f1f5f9; display: flex; align-items: center; gap: 1.25rem;
  text-decoration: none; transition: all 0.3s;
}
.legal-card:hover { border-color: #10b481; transform: translateX(5px); }

.legal-icon {
  width: 48px; height: 48px; background: #f8fafc; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}
.legal-icon i { font-size: 1.5rem; color: #10b481; }

.legal-title { font-size: 1rem; font-weight: 700; color: #111827; }
.legal-desc { font-size: 0.85rem; color: #94a3b8; }

@media (max-width: 640px) {
  .welcome-banner { padding: 1.5rem; }
  .welcome-decoration { display: none; }
}
</style>
