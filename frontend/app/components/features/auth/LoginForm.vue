<template>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full max-w-7xl">

<!-- LEFT : Login + Google -->
<div class="flex flex-col items-center justify-center bg-[#1E1E1E] p-8 rounded-3xl shadow-2xl relative border border-white/10">
  <AuthForm
    class="w-full max-w-md"
    title="Login"
    buttonText="Login"
    :fields="['username', 'password']"
    passwordLabel="Password"
    @submit="handleLogin"
  >
    <template #footer-links>
      <NuxtLink to="/signup" class="text-gray-400 hover:text-white hover:underline mr-4">
        Sign Up
      </NuxtLink>
    </template>
  </AuthForm>

  <div class="flex items-center w-full max-w-md my-6">
    <hr class="flex-grow border-gray-700" />
    <span class="mx-2 text-gray-400">ou</span>
    <hr class="flex-grow border-gray-700" />
  </div>

  <div
    id="googleButton"
    class="w-full max-w-md bg-[#0f0f0f] hover:bg-[#1a1a1a] cursor-pointer flex items-center justify-center py-3 rounded-lg shadow-md transition-all duration-300 border border-gray-700"
  ></div>

  <div v-if="isLoading" class="absolute inset-0 bg-black/50 flex items-center justify-center rounded-3xl z-50">
    <div class="w-12 h-12 border-4 border-t-[#10b481] border-white rounded-full animate-spin"></div>
  </div>
</div>

<!-- RIGHT : Assistant IA Chat -->
<div class="col-span-2 bg-[#1E1E1E] backdrop-blur-xl shadow-2xl rounded-3xl p-6 flex flex-col border border-white/10" style="height: 600px;">
        <h1 class="text-4xl font-bold text-white mb-4">Sesily AI</h1>
        <p class="text-gray-400 mb-6 text-base">
          Posez une question avant même de vous connecter.
        </p>

        <div class="flex-1 flex flex-col overflow-hidden rounded-2xl bg-white/5 border border-white/10 shadow-inner">
          <AssistantIa class="flex-1 flex flex-col"/>
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
            <!-- Icône -->
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
                notification.type === 'success'
                  ? 'text-[#10b481]'
                  : 'text-red-500',
              ]"
            >
              {{ notification.message }}
            </p>
  
            <p class="text-gray-500 text-sm">
              {{
                notification.type === "success"
                  ? "Redirecting to your dashboard..."
                  : "Please try again."
              }}
            </p>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from "vue";
  import AuthForm from "~/components/features/auth/AuthForm.vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "~/stores/auth";
  import { useApi } from "~/composables/useApi";
  import AssistantIa from "~/components/features/ai/AssistantIA.vue";
  
  const router = useRouter();
  const authStore = useAuthStore();
  const { apiFetch } = useApi();
  const isLoading = ref(false);
  const notification = ref({ visible: false, message: "", type: "success" });
  const googleLoaded = ref(false);
  
  const showNotification = (
    message: string,
    type: "success" | "error" = "success",
    duration = 3000
  ) => {
    notification.value = { visible: true, message, type };
    setTimeout(() => (notification.value.visible = false), duration);
  };
  
  const handleLogin = async (formData: {
    username: string;
    password: string;
  }) => {
    if (!formData.username || !formData.password) {
      alert("Veuillez remplir tous les champs");
      return;
    }
    isLoading.value = true;
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
      });

      showNotification("You're signed in successfully.", "success");
      setTimeout(() => {
        router.push("/farmer/dashboard");
      }, 2000);
    } catch (error: any) {
      console.error(error);
      const msg = error.data?.detail || "Network error";
      showNotification(msg, "error");
    } finally {
      isLoading.value = false;
    }
  };
  
  onMounted(() => {
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
        "972113542805-n0fujnh22t4jkejhvda051oml965limf.apps.googleusercontent.com",
      callback: async (response: any) => {
        try {
          isLoading.value = true;
          const data: any = await apiFetch("/api/google-login/", {
            method: "POST",
            body: { token: response.credential },
          });

          authStore.setUserData({
            token: data.token,
            uuid: data.user.uuid,
            username: data.user.username,
          });

          showNotification("You're signed in successfully.", "success");
          setTimeout(() => {
            router.push("/farmer/dashboard");
          }, 2000);
        } catch (err) {
          console.error(err);
          showNotification("Google login failed", "error");
          setTimeout(() => {}, 3000);
        } finally {
          isLoading.value = false;
        }
      },
      auto_select: false,
    });
  
    window.google.accounts.id.renderButton(
      document.getElementById("googleButton"),
      {
        theme: "outline",
        size: "large",
        type: "standard",
        shape: "rectangular",
        width: "100%",
      }
    );
  };
  </script>
  
  <style>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  </style>
  