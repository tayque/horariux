<template>
  <div class="flex flex-col min-h-screen">
    
    <!-- Cuerpo dividido en dos columnas -->
    <div class="flex flex-1 flex-col md:flex-row">

      <!-- Lado izquierdo: logo -->
      <div class="w-full md:w-1/2 flex items-center justify-center bg-[#071A33] p-8 max-h-screen">
        <img :src="iconoSoftware" alt="Logo del sistema" class="max-w-full h-auto object-fit" />
      </div>

      <!-- Lado derecho: login -->
      <div class="w-full md:w-1/2 flex items-center justify-center bg-gray-50 p-8 py-16">
        <div class="w-full max-w-md">
          <!-- Título -->
          <div class="mb-10 text-center">
            <h2 class="text-4xl font-extrabold text-gray-800 mb-3 font-['Kdam_Thmor_Pro']">Login</h2>
            <p class="text-gray-600 text-lg font-['Jost']">Ingrese sus datos:</p>
          </div>

          <!-- Formulario -->
          <form @submit.prevent="login" class="space-y-8">
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Usuario:</label>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Ingrese su usuario"
                :class="[
                  'block w-full px-4 py-3 border rounded-lg bg-white text-black placeholder-gray-400',
                  'focus:outline-none focus:ring-2 focus:ring-slate-500 transition duration-200',
                  usernameError ? 'border-red-300 bg-red-50' : 'border-gray-300 hover:border-gray-400'
                ]"
              />
              <p v-if="usernameError" class="text-red-500 text-sm mt-1">Usuario no puede estar vacío</p>
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña:</label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••••"
                  :class="[
                    'block w-full px-4 py-3 pr-12 border rounded-lg bg-white text-black placeholder-gray-400',
                    'focus:outline-none focus:ring-2 focus:ring-slate-500 transition duration-200',
                    passwordError ? 'border-red-300 bg-red-50' : 'border-gray-300 hover:border-gray-400'
                  ]"
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 focus:outline-none"
                >
                  <svg v-if="showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                  <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
              <p v-if="passwordError" class="text-red-500 text-sm mt-1">Contraseña no puede estar vacía</p>
            </div>

            <div class="text-right">
              <a @click="goToRecuperarContrasena" class="text-sm text-slate-600 hover:text-slate-800 hover:underline cursor-pointer">¿Olvidaste la contraseña?</a>
            </div>

            <button
              type="submit"
              :disabled="isLoading"
              class="w-full flex items-center justify-center py-3 px-6 bg-slate-800 text-white text-base rounded-lg font-['Kdam_Thmor_Pro'] hover:bg-slate-700"
            >
              <svg v-if="isLoading" class="animate-spin mr-3 h-5 w-5" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ isLoading ? 'Iniciando...' : 'Iniciar Sesión' }}
            </button>

            <div v-if="apiError" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <p class="text-sm text-red-800">{{ apiError }}</p>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Espaciadores para empujar el footer mucho más abajo con división de colores -->
    <div class="flex flex-grow">
      <div class="w-1/2 bg-[#071A33]"></div>
      <div class="w-1/2 bg-gray-50"></div>
    </div>
    <div class="flex h-32">
      <div class="w-1/2 bg-[#071A33]"></div>
      <div class="w-1/2 bg-gray-50"></div>
    </div>
    <div class="flex flex-grow">
      <div class="w-1/2 bg-[#071A33]"></div>
      <div class="w-1/2 bg-gray-50"></div>
    </div>

    <!-- Footer fijo abajo -->
    <footer class="bg-[#071A33] text-white py-8 px-8">
    <p class="text-center text-xl md:text-2xl mb-6 font-['Kdam_Thmor_Pro']">Facilitamos la gestión de horarios universitarios</p>
    <div class="flex flex-col md:flex-row justify-between text-sm max-w-5xl mx-auto font-['Jost']">
      <div class="mb-4 md:mb-0">
        <p class="font-bold mb-2">Email:</p>
        <p class="font-normal">saliagac@unsa.edu.pe</p>
        <p class="font-normal">tayque@unsa.edu.pe</p>
        <p class="font-normal">rcamargoh@unsa.edu.pe</p>
        <p class="font-normal">pmaytaqu@unsa.edu.pe</p>
      </div>
      <div>
        <p class="font-bold mb-2">Nombres:</p>
        <p class="font-normal">Aliaga Chaina Sandra Gabriela</p>
        <p class="font-normal">Ayque Puraca Tania Luz</p>
        <p class="font-normal">Camargo Hilachoque Romina Giuliana</p>
        <p class="font-normal">Mayta Quispe Paola Adamari</p>
      </div>
    </div>
  </footer>

  </div>
</template>

<script>
import iconoSoftware from '@/assets/icono-software.png';
import AuthService from '@/services/auth.service';
export default {
  name: 'LoginView',
  data() {
    return {
      iconoSoftware,
      username: '',
      password: '',
      showPassword: false,
      usernameError: false,
      passwordError: false,
      apiError: '',
      isLoading: false,
    }
  },
  methods: {
    goToRecuperarContrasena() {
    this.$router.push('/recuperar');
  },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      // Validar campos vacíos
      this.usernameError = this.username.trim() === '';
      this.passwordError = this.password.trim() === '';
      this.apiError = '';
      
      if (this.usernameError || this.passwordError) {
        return;
      }

      this.isLoading = true;
      
      try {
        console.log('Iniciando login con AuthService...');
        
        // Usar el servicio de autenticación en lugar de fetch manual
        const result = await AuthService.login(this.username.trim(), this.password.trim());
        
        if (result.success) {
          console.log('Login exitoso');
          
          // Mostrar mensaje de éxito
          this.apiError = '';
          
          // Redirigir al dashboard después de un breve delay
          setTimeout(() => {
            this.$router.push('/dashboard');
          }, 500);
          
        } else {
          console.log('Login falló:', result.message);
          this.apiError = result.message || 'Credenciales inválidas.';
        }
        
      } catch (error) {
        console.error('Error en login:', error);
        this.apiError = 'Error de conexión. Intenta nuevamente.';
      } finally {
        this.isLoading = false;
      }
    },
  },
}
</script>

<style scoped>
/* Asegúrate de tener importada la fuente Jost si la estás usando */
body {
  font-family: 'Jost', sans-serif;
}
</style>
