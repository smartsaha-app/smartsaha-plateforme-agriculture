<template>
  <div
    class="min-h-screen flex flex-col md:flex-row bg-gradient-to-tr from-[#0f0f0f] to-[#121212] relative overflow-x-hidden"
  >
    <!-- Colonne gauche : Formulaire -->
    <div
      class="md:w-1/3 flex flex-col justify-center items-center p-8 bg-[#f9f9f9] relative z-20"
    >
      <div class="absolute top-8 left-8 flex items-center gap-3">
        <img
          src="/logo.png"
          alt="Smartsaha Logo"
          class="w-10 h-10 object-contain"
        />
        <div class="flex flex-col text-left">
          <h1 class="text-md font-bold text-[#112830]">Smartsaha</h1>
          <p class="text-gray-500 text-xs">Nurture Data, Harvest Impact.</p>
        </div>
      </div>

      <div class="w-full max-w-sm mt-8">
        <AuthForm
          :title="userType === 'farmer' ? 'Inscription Producteur' : 'Inscription Entreprise'"
          buttonText="Créer mon compte"
          :fields="['first_name', 'last_name', 'email', 'password']"
          passwordLabel="Mot de passe"
          @submit="handleSignup"
        >
          <template #under-title>
            <div class="mb-5 p-1 bg-gray-50 rounded-2xl flex gap-1 border border-gray-100 shadow-inner">
              <button 
                type="button"
                @click="userType = 'farmer'"
                :class="[
                  'flex-1 py-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2',
                  userType === 'farmer' ? 'bg-white shadow-sm text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-user-circle text-lg"></i>
                Producteur
              </button>
              <button 
                type="button"
                @click="userType = 'enterprise'"
                :class="[
                  'flex-1 py-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2',
                  userType === 'enterprise' ? 'bg-white shadow-sm text-[#10b481]' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <i class="bx bx-buildings text-lg"></i>
                Entreprise/ONG
              </button>
            </div>
          </template>

          <template #footer-links>
            <!-- Slot vide pour l'instant -->
          </template>
        </AuthForm>

        <div class="flex items-center w-full my-4" v-show="userType === 'farmer'">
          <hr class="flex-grow border-gray-200" />
          <span class="mx-3 text-xs font-bold text-gray-400 uppercase tracking-widest">ou</span>
          <hr class="flex-grow border-gray-200" />
        </div>

        <div
          id="googleButton"
          class="w-full gap-3 hover:scale-2 cursor-pointer flex items-center justify-center py-2 rounded transition-all duration-300"
          v-show="userType === 'farmer'"
        >
          <img
            src="/Google__G__logo.svg.png"
            alt="Google"
            class="w-5 h-5 mr-2"
          />
          <span class="text-gray-900">Sign in with Google</span>
        </div>
      </div>
    </div>

    <!-- Colonne droite : Visuel / Slider -->
    <div
      class="hidden md:flex md:w-2/3 flex-col justify-between p-10 relative shadow-xl overflow-hidden bg-gray-900"
    >
      <canvas ref="aiCanvas" class="absolute inset-0 w-full h-full"></canvas>

      <div class="absolute inset-0 bg-[#10b481]/10 backdrop-blur-xs pointer-events-none"></div>

      <div class="relative flex justify-end items-center mb-10 z-10 gap-4 text-right">
        <p class="text-sm text-gray-300 font-medium">
          Already have an account?
        </p>
        <NuxtLink
          to="/login"
          class="px-6 py-2 bg-transparent border border-white text-gray-50 text-sm rounded hover:scale-105 transition-transform transform hover:-translate-y-0.5 duration-300"
        >
          Log In
        </NuxtLink>
      </div>

      <div class="slider relative flex-1 flex flex-col justify-center items-center">
        <div
          v-for="(slide, index) in slides"
          :key="index"
          class="slide absolute left-8 flex flex-col justify-end items-start transition-opacity duration-1000 opacity-0 text-gray-50 max-w-xl text-left"
        >
          <h2 class="text-3xl md:text-4xl font-extrabold mb-3 leading-tight">
            {{ slide.title }}
          </h2>
          <p class="text-lg md:text-xl mb-6 text-gray-200">
            {{ slide.text }}
          </p>
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
                ? "Redirecting..."
                : "Please try again."
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
import { ref, onMounted, onUnmounted } from "vue";

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const isLoading = ref(false);
const userType = ref<'farmer' | 'enterprise'>('farmer');

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
  if (!formData.email || !formData.password) {
    alert("Veuillez remplir tous les champs obligatoires");
    return;
  }

  isLoading.value = true;
  try {
    const data: any = await apiFetch("/api/signup/", {
      method: "POST",
      body: {
        username: formData.email,
        email: formData.email,
        first_name: formData.first_name || "",
        last_name: formData.last_name || "",
        password: formData.password,
        role: userType.value === 'farmer' ? 'AGRICULTEUR' : 'ORGANISATION',
      },
    });

    showNotification("Compte créé avec succès !", "success");
    
    // Authentification automatique
    try {
      const loginData: any = await apiFetch("/api/login/", {
        method: "POST",
        body: {
          email: formData.email,
          password: formData.password,
        },
      });

      authStore.setUserData({
        uuid: loginData.user.uuid,
        username: loginData.user.username,
        spaces: loginData.user.spaces,
      });

      setTimeout(() => {
        if (userType.value === 'enterprise') {
          navigateTo("/onboarding");
        } else {
          navigateTo("/farmer/dashboard");
        }
      }, 2000);
    } catch (loginError: any) {
      console.error("Erreur auto-login:", loginError);
      // En cas d'erreur de login, on redirige quand même vers login pour que l'utilisateur puisse essayer manuellement
      setTimeout(() => {
        navigateTo("/login");
      }, 2000);
    }
  } catch (error: any) {
    console.error("Erreur signup:", error);
    const msg = error.data ? Object.entries(error.data)
        .map(([key, value]) => `${key}: ${value}`)
        .join("\n") : "Network error";
    alert(msg);
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
            role: userType.value === 'farmer' ? 'AGRICULTEUR' : 'ORGANISATION'
          },
        });

        authStore.setUserData({
          uuid: data.user.uuid,
          username: data.user.username,
          spaces: data.user.spaces,
        });

        showNotification("You're signed in successfully.", "success");
        setTimeout(async () => {
          if (userType.value === 'enterprise') {
            await navigateTo("/onboarding");
          } else {
            await navigateTo(authStore.getWorkspacePath());
          }
        }, 2000);
      } catch (err: any) {
        console.error(err);
        showNotification("Google login failed", "error");
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

const slides = [
  {
    title: "Meet Sesily AI",
    text: "Your smart agronomist assistant, ready to guide you through your data and provide actionable insights.",
  },
  {
    title: "Optimize Your Farm",
    text: "Sesily AI helps you analyze soil, crops, and weather to maximize your harvest efficiently.",
  },
  {
    title: "Lead with Data",
    text: "Make informed decisions with real-time recommendations from your AI assistant.",
  },
];

const currentIndex = ref(0);
let intervalId: any;

onMounted(() => {
  const nextSlide = () => {
    const allSlides = document.querySelectorAll<HTMLDivElement>(".slide");
    allSlides.forEach((slide, idx) => {
      slide.style.opacity = idx === currentIndex.value ? "1" : "0";
    });
    currentIndex.value = (currentIndex.value + 1) % slides.length;
  };
  nextSlide();
  intervalId = setInterval(nextSlide, 8000);
});

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
