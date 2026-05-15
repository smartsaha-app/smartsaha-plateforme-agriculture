<template>
  <div
    class="min-h-screen flex flex-col md:flex-row bg-gradient-to-tr from-[#0f0f0f] to-[#121212]"
  >
    <div
      class="w-full md:w-1/3 flex flex-col justify-center items-center p-6 md:p-8 bg-[#f9f9f9] relative min-h-screen md:min-h-0"
    >
      <div class="absolute top-6 left-6 md:top-8 md:left-8 flex items-center gap-3">
        <img
          src="/logo.png"
          alt="Smartsaha Logo"
          class="w-10 h-10 object-contain"
        />
        <div class="flex flex-col">
          <h1 class="text-md font-bold text-[#112830]">Smartsaha</h1>
          <p class="text-gray-500 text-xs">{{ $t("auth.slogan") }}</p>
        </div>
      </div>

      <div class="w-full max-w-sm mt-20 md:mt-4 p-4 md:p-6">
        <AuthForm
          :title="$t('auth.loginTitle')"
          :buttonText="$t('auth.loginBtn')"
          :fields="['email', 'password']"
          :passwordLabel="$t('auth.password')"
          showForgotPassword
          @submit="handleLogin"
        >
          <template #footer-links>
            <p class="text-sm">
              {{ $t("auth.noAccount") }}
              <NuxtLink :to="localePath('/signup')" class="text-[#10b481] font-bold hover:underline">
                {{ $t("auth.signup") }}
              </NuxtLink>
            </p>
          </template>
        </AuthForm>

        <div class="flex items-center w-full my-4">
          <hr class="flex-grow border-gray-200" />
          <span class="mx-3 text-xs font-bold text-gray-400 uppercase tracking-widest">{{ $t("auth.or") }}</span>
          <hr class="flex-grow border-gray-200" />
        </div>

        <!-- <div
          id="googleButton"
          class="w-full bg-gray-100 border border-gray-400 gap-3 hover:scale-2 cursor-pointer flex items-center justify-center py-2 rounded transition-all duration-300"
        > -->
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

    <div
      class="hidden md:flex md:w-2/3 flex-col justify-between p-10 relative shadow-xl overflow-hidden bg-gray-900"
    >
      <canvas ref="aiCanvas" class="absolute inset-0 w-full h-full"></canvas>

      <div
        class="absolute inset-0 bg-[#10b481]/10 backdrop-blur-xs pointer-events-none"
      ></div>

      <!-- Le CTA Sign Up a été retiré d'ici pour éviter la redondance avec le lien sous le formulaire -->

      <div
        class="slider relative flex-1 flex flex-col justify-center items-center left-6"
      >
        <div
          v-for="(slide, index) in slides"
          :key="index"
          v-show="currentIndex === index"
          class="slide absolute left-8 flex flex-col justify-end items-start transition-all duration-700 text-gray-50 max-w-xl animate-in fade-in"
        >
          <h2 class="text-3xl md:text-4xl font-extrabold mb-3 leading-tight">
            {{ slide.title }}
          </h2>
          <p class="text-lg md:text-xl mb-6 text-gray-200">
            {{ slide.text }}
          </p>
          <NuxtLink
            :to="localePath(slide.link)"
            class="inline-flex items-center gap-2 text-white group"
          >
            <span class="underline decoration-1 decoration-white group-hover:decoration-2 transition-all"
              >Learn More</span
            >
            <i class="bx bx-right-arrow-alt text-lg group-hover:translate-x-1 transition-transform"></i>
          </NuxtLink>

          <div class="mb-24"></div>
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
  </div>

  <div
    v-if="isLoading"
    class="absolute inset-0 bg-black/50 flex items-center justify-center"
  >
    <div
      class="w-12 h-12 border-4 border-t-[#10b481] border-white rounded-full animate-spin"
    ></div>
  </div>

  <transition name="fade">
    <div
      v-if="notification.visible"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black/20 backdrop-blur-sm"
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
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AuthForm from "~/components/features/auth/AuthForm.vue";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const { t: nuxtT } = useI18n();
const localePath = useLocalePath();

const authStore = useAuthStore();
const { apiFetch } = useApi();
const router = useRouter();
const route = useRoute();

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
const isLoading = ref(false);
const notification = ref({ visible: false, message: "", type: "success" });
const googleLoaded = ref(false);

const aiCanvas = ref<HTMLCanvasElement | null>(null);

// ── HELPERS ───────────────────────────────────────────────────────────────
const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.value = { visible: true, message, type };
  setTimeout(() => (notification.value.visible = false), duration);
};

// ── HANDLERS ──────────────────────────────────────────────────────────────
const handleLogin = async (formData: Record<string, string>) => {
  if (!formData.email || !formData.password) {
    alert(nuxtT("auth.fillFields"));
    return;
  }
  isLoading.value = true;
  try {
    const data: any = await apiFetch("/api/login/", {
      method: "POST",
      body: formData,
    });

    authStore.setUserData({
      token: data.token,
      uuid: data.user.uuid,
      username: data.user.username,
      spaces: data.user.spaces,
    });

    showNotification(nuxtT("auth.signInSuccess"), "success");
    
    // Capture redirect info before the timeout
    const redirect = route.query.redirect;
    
    setTimeout(async () => {
      if (redirect === 'onboarding') {
        await navigateTo("/onboarding");
      } else {
        await navigateTo(authStore.getWorkspacePath());
      }
    }, 2000);
  } catch (error: any) {
    console.error(error);
    const msg = error.data?.detail || nuxtT("auth.tryAgain");
    showNotification(msg, "error");
  } finally {
    isLoading.value = false;
  }
};

// ── GOOGLE AUTH ───────────────────────────────────────────────────────────
const renderGoogleButton = () => {
  if (!googleLoaded.value || !window.google) return;

  window.google.accounts.id.initialize({
    client_id:
      "186820827638-9915pmkfj0s6ch5tdrc73vakoep2vlsd.apps.googleusercontent.com",
    callback: async (response: any) => {
      try {
        isLoading.value = true;
        const data = await apiFetch("/api/google-login/", {
          method: "POST",
          body: { 
            token: response.credential
          },
        });

        authStore.setUserData({
          token: data.token,
          uuid: data.user.uuid,
          username: data.user.username,
          spaces: data.user.spaces,
        });

        showNotification(nuxtT("auth.signInSuccess"), "success");

        // Capture redirect info before the timeout
        const redirect = route.query.redirect;

        setTimeout(async () => {
          if (redirect === 'onboarding') {
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

// ── SLIDER ────────────────────────────────────────────────────────────────
const initSlider = () => {
  // Le slider est maintenant géré par les classes réactives (currentIndex === index)
  const nextSlide = () => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length;
  };

  window.setInterval(nextSlide, 8000);
};

// ── CANVAS ────────────────────────────────────────────────────────────────
const initCanvas = () => {
  if (!aiCanvas.value) return;

  const canvas = aiCanvas.value;
  const ctx = canvas.getContext("2d")!;
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  const particles: { x: number; y: number; vx: number; vy: number; size: number }[] = [];
  const numParticles = 50;

  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 1.5,
      vy: (Math.random() - 0.5) * 1.5,
      size: Math.random() * 3 + 1,
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
      ctx.fillStyle = "#10b481";
      ctx.fill();
      ctx.closePath();
    });

    for (let i = 0; i < numParticles; i++) {
      for (let j = i + 1; j < numParticles; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(16,180,129,${1 - dist / 100})`;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
          ctx.closePath();
        }
      }
    }
    requestAnimationFrame(animate);
  };

  animate();

  window.addEventListener("resize", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  });
};

// ── SINGLE onMounted ──────────────────────────────────────────────────────
onMounted(() => {
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

  initSlider();
  initCanvas();
});
</script>

<style scoped>
#googleButton .G_idSignIn {
  background: transparent !important;
  border: none !important;
  width: 100% !important;
  box-shadow: none !important;
  padding: 0 !important;
}

#googleButton .G_idSignIn {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.slide {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.animate-pulse {
  animation: pulse 4s infinite;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-bounce {
  animation: bounce 6s infinite;
}

@keyframes ping {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  75%,
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}

.animate-in {
  animation-fill-mode: forwards;
}

.fade-in {
  animation: fadeIn 0.8s ease-out;
}

.swiper-slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.swiper-pagination-bullet {
  background-color: #10b481;
  opacity: 0.8;
}
</style>
