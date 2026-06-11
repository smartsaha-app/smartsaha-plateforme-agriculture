<template>
  <div
    class="h-screen flex flex-col md:flex-row bg-gradient-to-tr from-[#0f0f0f] to-[#121212] relative overflow-hidden"
  >
    <!-- Colonne gauche : Formulaire -->
    <div
      class="w-full md:w-[42%] flex flex-col justify-center items-center px-6 py-4 md:px-10 md:py-6 bg-[#f9f9f9] relative z-20 h-full overflow-y-auto"
    >
      <div class="absolute top-4 left-5 md:top-5 md:left-6 flex items-center gap-2">
        <img
          src="/logo.png"
          alt="Smartsaha Logo"
          class="w-10 h-10 object-contain"
        />
        <div class="flex flex-col text-left">
          <h1 class="text-md font-bold text-[#112830]">Smartsaha</h1>
          <p class="text-gray-500 text-xs">{{ $t("auth.slogan") }}</p>
        </div>
      </div>

      <div class="w-full max-w-md mt-12 md:mt-2 p-2 md:p-0">
        <AuthForm
          :title="signupTitle"
          :buttonText="$t('auth.signupBtn')"
          :fields="['first_name', 'last_name', 'email', 'password']"
          :passwordLabel="$t('auth.password')"
          @submit="handleSignup"
        >
          <template #under-title>
            <div class="mb-4 p-1 bg-gray-100/50 rounded-2xl grid grid-cols-4 gap-1 border border-gray-200/50 shadow-inner">
              <button
                type="button"
                @click="userType = 'buyer'"
                :class="[
                  'py-2 rounded-xl text-xs font-black uppercase tracking-tighter transition-all flex flex-col items-center justify-center gap-0.5',
                  userType === 'buyer' ? 'bg-white shadow-md shadow-[#10b481]/5 text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-shopping-bag text-base"></i>
                {{ $t("auth.buyer") }}
              </button>
              <button
                type="button"
                @click="userType = 'farmer'"
                :class="[
                  'py-2 rounded-xl text-xs font-black uppercase tracking-tighter transition-all flex flex-col items-center justify-center gap-0.5',
                  userType === 'farmer' ? 'bg-white shadow-md shadow-[#10b481]/5 text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-leaf text-base"></i>
                {{ $t("auth.farmer") }}
              </button>
              <button
                type="button"
                @click="userType = 'seller'"
                :class="[
                  'py-2 rounded-xl text-xs font-black uppercase tracking-tighter transition-all flex flex-col items-center justify-center gap-0.5',
                  userType === 'seller' ? 'bg-white shadow-md shadow-[#10b481]/5 text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-store text-base"></i>
                {{ $t("auth.seller") }}
              </button>
              <button
                type="button"
                @click="userType = 'enterprise'"
                :class="[
                  'py-2 rounded-xl text-xs font-black uppercase tracking-tighter transition-all flex flex-col items-center justify-center gap-0.5',
                  userType === 'enterprise' ? 'bg-white shadow-md shadow-[#10b481]/5 text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-buildings text-base"></i>
                {{ $t("auth.organization") }}
              </button>
            </div>
          </template>

          <template #footer-links>
            <p class="text-sm">
              {{ $t("auth.alreadyAccount") }}
              <NuxtLink :to="localePath('/login')" class="text-[#10b481] hover:underline font-bold">
                {{ $t("auth.loginTitle") }}
              </NuxtLink>
            </p>
          </template>
        </AuthForm>

        <div class="flex items-center w-full my-4">
          <hr class="flex-grow border-gray-200" />
          <span class="mx-3 text-xs font-bold text-gray-400 uppercase tracking-widest">{{ $t("auth.or") }}</span>
          <hr class="flex-grow border-gray-200" />
        </div>

        <div
          id="googleButton"
          class="w-full gap-3 hover:scale-2 cursor-pointer flex items-center justify-center py-2 rounded transition-all duration-300"
        >
          <img
            src="/Google__G__logo.svg.png"
            alt="Google"
            class="w-5 h-5 mr-2"
          />
          <span class="text-gray-900">{{ $t("auth.googleSignIn") }}</span>
        </div>
      </div>
    </div>

    <!-- Colonne droite : Visuel / Slider -->
    <div
      class="hidden md:flex md:w-[58%] flex-col justify-center p-10 relative shadow-xl overflow-hidden bg-gray-900 h-full"
    >
      <canvas ref="aiCanvas" class="absolute inset-0 w-full h-full"></canvas>

      <div class="absolute inset-0 bg-[#10b481]/10 backdrop-blur-xs pointer-events-none"></div>

      <!-- Le CTA Log In a été retiré d'ici pour éviter la redondance avec le lien sous le formulaire -->

      <div class="slider relative flex-1 flex flex-col justify-center items-center">
        <div
          v-for="(slide, index) in slides"
          :key="index"
          v-show="currentIndex === index"
          class="slide absolute left-8 flex flex-col justify-end items-start transition-all duration-1000 text-gray-50 max-w-xl text-left animate-in fade-in"
        >
          <h2 class="text-3xl md:text-4xl font-extrabold mb-3 leading-tight">
            {{ slide.title }}
          </h2>
          <p class="text-lg md:text-xl mb-6 text-gray-200">
            {{ slide.text }}
          </p>
          <NuxtLink
            :to="localePath(slide.link)"
            class="inline-flex items-center gap-3 whitespace-nowrap px-5 py-2.5 bg-[#10b481] hover:bg-white hover:text-[#112830] text-white rounded-xl font-bold text-sm transition-all duration-200 group mt-2"
          >
            <i class="bx bx-robot text-base" aria-hidden="true"></i>
            <span>{{ $t('auth.learnMore') }}</span>
            <i class="bx bx-right-arrow-alt text-lg group-hover:translate-x-1 transition-transform" aria-hidden="true"></i>
          </NuxtLink>
        </div>
      </div>

      <div class="absolute bottom-6 left-16 flex gap-2">
        <span
          v-for="(_, i) in slides"
          :key="i"
          :class="{
            'bg-[#10b481] w-6 h-1 transition-all duration-300': true,
            'opacity-100 scale-125': i === currentIndex,
            'opacity-50 scale-100': i !== currentIndex,
          }"
        ></span>
      </div>
    </div>

    <!-- Overlay Loading & Notification -->
    <div
      v-if="isLoading"
      class="absolute inset-0 bg-black/50 flex items-center justify-center z-[100]"
    >
      <div
        class="w-12 h-12 border-4 border-t-[#10b481] border-white rounded-full animate-spin"
      ></div>
    </div>

    <transition name="fade">
      <div
        v-if="notification.visible"
        class="fixed inset-0 flex items-center justify-center z-[110] bg-black/20 backdrop-blur-sm"
      >
        <div
          :class="[
            'bg-white rounded-2xl shadow-2xl px-8 py-6 flex flex-col items-center gap-4 w-[340px] text-center transition-all duration-300',
            notification.type === 'success'
              ? 'border-t-4 border-[#10b481]'
              : 'border-t-4 border-red-500',
          ]"
        >
          <div
            v-if="notification.type === 'success'"
            class="w-16 h-16 rounded-full bg-[#10b481] flex items-center justify-center"
          >
            <i class="bx bx-check text-4xl font-extrabold text-white"></i>
          </div>
          <div
            v-else
            class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center"
          >
            <i class="bx bx-x text-4xl font-extrabold text-white"></i>
          </div>

          <p
            :class="[
              'text-lg font-semibold',
              notification.type === 'success' ? 'text-[#10b481]' : 'text-red-500',
            ]"
          >
            {{ notification.message }}
          </p>

          <p class="text-gray-500 text-sm">
            {{
              notification.type === "success"
                ? $t("auth.redirecting")
                : $t("auth.tryAgain")
            }}
          </p>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import AuthForm from "~/components/features/auth/AuthForm.vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
import { ref, onMounted, onUnmounted, computed } from "vue";

const { t: nuxtT } = useI18n();
const localePath = useLocalePath();

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const isLoading = ref(false);
const userType = ref<'farmer' | 'enterprise' | 'buyer' | 'seller'>('buyer');

const signupTitle = computed(() => {
  switch (userType.value) {
    case 'buyer': return nuxtT('auth.buyer');
    case 'farmer': return nuxtT('auth.farmer');
    case 'seller': return nuxtT('auth.seller');
    case 'enterprise': return nuxtT('auth.organization');
    default: return nuxtT('auth.signupTitle');
  }
});

const notification = ref({
  visible: false,
  message: "",
  type: "success",
});

const googleLoaded = ref(false);

const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => (notification.value.visible = false), duration);
};

const handleSignup = async (formData: Record<string, string>) => {
  // ── Validation client ────────────────────────────────────────────────────
  if (!formData.email || !formData.password) {
    showNotification(nuxtT("auth.fillFields"), "error");
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(formData.email)) {
    showNotification(nuxtT("auth.invalidEmailFormat"), "error");
    return;
  }

  if (formData.password.length < 8) {
    showNotification(nuxtT("auth.passwordTooShort"), "error");
    return;
  }

  isLoading.value = true;
  try {
    await apiFetch("/api/signup/", {
      method: "POST",
      body: {
        username: formData.email,
        email: formData.email,
        first_name: formData.first_name || "",
        last_name: formData.last_name || "",
        password: formData.password,
        role:
          userType.value === 'buyer'      ? 'BUYER' :
          userType.value === 'seller'     ? 'SELLER_PUR' :
          userType.value === 'farmer'     ? 'AGRICULTEUR' :
          'ORGANISATION',
      },
    });

    showNotification(nuxtT("auth.accountCreated"), "success");

    // ── Auto-login immédiat ────────────────────────────────────────────────
    try {
      const loginData: any = await apiFetch("/api/login/", {
        method: "POST",
        body: { email: formData.email, password: formData.password },
      });

      authStore.setUserData({
        token: loginData.token,
        uuid: loginData.user.uuid,
        username: loginData.user.username,
        spaces: loginData.user.spaces,
      });

      setTimeout(() => {
        navigateTo(userType.value === 'enterprise' ? "/onboarding" : authStore.getWorkspacePath());
      }, 1000);
    } catch {
      setTimeout(() => navigateTo("/login"), 1000);
    }
  } catch (error: any) {
    console.error("Erreur signup:", error);

    // ── Erreur réseau ───────────────────────────────────────────────────────
    const isNetworkError =
      (typeof navigator !== "undefined" && !navigator.onLine) ||
      !error.status ||
      error.name === "TypeError" ||
      error.message?.toLowerCase().includes("failed to fetch");

    if (isNetworkError) {
      showNotification(nuxtT("auth.networkError"), "error", 5000);
      return;
    }

    // ── Erreurs backend lisibles ────────────────────────────────────────────
    let msg = nuxtT("auth.tryAgain");
    if (error.data) {
      // Email déjà utilisé
      if (error.data.email) {
        const emailErr = Array.isArray(error.data.email) ? error.data.email[0] : error.data.email;
        msg = String(emailErr).toLowerCase().includes("already")
          ? nuxtT("auth.emailNotFound").replace("Aucun compte", "Email déjà utilisé")
          : String(emailErr);
      } else {
        const firstVal = Object.values(error.data)[0];
        if (firstVal) {
          msg = Array.isArray(firstVal) ? (firstVal[0] as string) : String(firstVal);
        }
      }
    }
    showNotification(msg, "error");
  } finally {
    isLoading.value = false;
  }
};

const aiCanvas = ref<HTMLCanvasElement | null>(null);

onMounted(() => {
  if (!aiCanvas.value) return;

  const canvas = aiCanvas.value;
  const ctx = canvas.getContext("2d")!;
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  const particles: any[] = [];
  const numParticles = 40;

  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 1,
      vy: (Math.random() - 0.5) * 1,
      size: Math.random() * 2 + 1,
    });
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(16,180,129,0.3)";
      ctx.fill();
    });
    requestAnimationFrame(animate);
  };
  animate();

  // Charger Google Sign-In
  if (!window.google) {
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = () => {
      googleLoaded.value = true;
      renderGoogleButton();
    };
    document.head.appendChild(script);
  } else {
    googleLoaded.value = true;
    renderGoogleButton();
  }
});

const renderGoogleButton = () => {
  if (!googleLoaded.value || !window.google) return;

  window.google.accounts.id.initialize({
    client_id:
      "186820827638-9915pmkfj0s6ch5tdrc73vakoep2vlsd.apps.googleusercontent.com",
    callback: async (response: any) => {
      try {
        isLoading.value = true;
        const data: any = await apiFetch("/api/google-login/", {
          method: "POST",
          body: { 
            token: response.credential,
            role: 
              userType.value === 'buyer' ? 'BUYER' : 
              userType.value === 'seller' ? 'SELLER_PUR' :
              userType.value === 'farmer' ? 'AGRICULTEUR' : 
              'ORGANISATION'
          },
        });

        authStore.setUserData({
          token: data.token,
          uuid: data.user.uuid,
          username: data.user.username,
          spaces: data.user.spaces,
        });

        showNotification(nuxtT("auth.signInSuccess"), "success");
        setTimeout(async () => {
          if (userType.value === 'enterprise') {
            await navigateTo("/onboarding");
          } else {
            await navigateTo(authStore.getWorkspacePath());
          }
        }, 2000);
      } catch (err: any) {
        console.error(err);
        showNotification(nuxtT("auth.googleFailed"), "error");
      } finally {
        isLoading.value = false;
      }
    },
    auto_select: false,
  });

  window.google.accounts.id.renderButton(
    document.getElementById("googleButton"),
    {
      size: "large",
      type: "standard",
      shape: "rectangular",
      width: "100%",
      theme: "outline",
      text: "continue_with",
    }
  );
};

const slides = computed(() => [
  {
    title: nuxtT("auth.slides[0].title"),
    text: nuxtT("auth.slides[0].text"),
    link: "/sesily-ai",
  },
  {
    title: nuxtT("auth.slides[1].title"),
    text: nuxtT("auth.slides[1].text"),
    link: "/sesily-ai",
  },
  {
    title: nuxtT("auth.slides[2].title"),
    text: nuxtT("auth.slides[2].text"),
    link: "/sesily-ai",
  },
]);

const currentIndex = ref(0);
let intervalId: any;

onMounted(() => {
  const nextSlide = () => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length;
  };
  intervalId = setInterval(nextSlide, 8000);
});

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

.animate-in {
  animation-fill-mode: forwards;
}

.fade-in {
  animation: fadeIn 1s ease-out;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
