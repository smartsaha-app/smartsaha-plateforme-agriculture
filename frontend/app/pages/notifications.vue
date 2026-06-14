<script setup lang="ts">
// Redirect vers la page notifications de l'espace actif de l'utilisateur
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const roleToSpace: Record<string, string> = {
  farmer:       'farmer',
  seller:       'seller',
  buyer:        'buyer',
  organization: 'organization',
  admin:        'admin',
}
const space = roleToSpace[authStore.user?.role ?? ''] ?? 'farmer'
await navigateTo(`/${space}/notifications`, { replace: true })
</script>
