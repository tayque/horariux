<template>
  <button
    @click="logout"
    :disabled="isLoading"
    class="flex items-center px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors duration-200 disabled:opacity-50"
  >
    <svg v-if="isLoading" class="animate-spin mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
    <svg v-else class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
    </svg>
    {{ isLoading ? 'Cerrando...' : 'Cerrar Sesión' }}
  </button>
</template>

<script>
import AuthService from '@/services/auth.service';

export default {
  name: 'LogoutButton',
  data() {
    return {
      isLoading: false,
    }
  },
  methods: {
    async logout() {
      this.isLoading = true;
      
      try {
        console.log('🚪 Cerrando sesión con AuthService...');
        
        const result = await AuthService.logout();
        
        if (result.success) {
          console.log('✅ Logout exitoso:', result.message);
          
          // Redirigir al login
          this.$router.push('/login');
          
        } else {
          console.log('⚠️ Logout con advertencia:', result.message);
          // Aunque falle, redirigir al login de todas formas
          this.$router.push('/login');
        }
        
      } catch (error) {
        console.error('💥 Error en logout:', error);
        // Aunque falle, redirigir al login de todas formas
        this.$router.push('/login');
      } finally {
        this.isLoading = false;
      }
    },
  },
}
</script>
