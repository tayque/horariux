<template>
  <div class="min-h-screen flex items-center justify-center bg-[#071A33] from-blue-900 via-blue-800 to-blue-700">
    <div class="bg-white rounded-2xl shadow-2xl p-10 w-full max-w-md">
      <h2 class="text-2xl font-bold text-blue-900 mb-6 text-center">Recuperar Contraseña</h2>

      <label class="block text-sm font-medium text-blue-900 mb-1">Motivo</label>
      <textarea
        v-model="reason"
        rows="3"
        placeholder="Escribe aquí tu motivo"
        class="w-full px-4 py-2 mb-4 border border-blue-300 text-black rounded-md focus:outline-none text-blackfocus:ring-2 focus:ring-blue-500 resize-none"
      ></textarea>

      <div class="flex gap-2">
        <button
          @click="sendRequest"
          class="w-full bg-[#071A33] hover:bg-blue-800 text-white font-semibold py-2 px-4 rounded-md transition duration-300"
        >
          Enviar Solicitud
        </button>
        <router-link
          to="/login"
          class="w-full bg-gray-300 hover:bg-gray-400 text-blue-900 font-semibold py-2 px-4 rounded-md transition duration-300 text-center flex items-center justify-center"
        >
          Cancelar
        </router-link>
      </div>

      <p class="mt-4 text-sm text-center text-green-700" v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  data() {
    return {
      reason: '',
      message: ''
    }
  },
  methods: {
    async sendRequest() {
      try {
        const response = await axios.post(`${API_URL}/recuperarContrasena/`, {
          reason: this.reason
        })
        this.message = response.data.message
      } catch (error) {
        this.message = "Hubo un error al enviar tu solicitud."
      }
    }
  }
}
</script>
