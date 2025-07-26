<template>
  <div class="flex min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <SidebarMenu />
    <div class="flex flex-col items-center justify-center flex-1">
      <div class="bg-white p-8 rounded shadow-lg w-full max-w-md">
        <h2 class="text-2xl font-bold text-[#0A1E40] mb-4 text-center">Exportar horarios a PDF</h2>
        <label class="block mb-2 text-[#0A1E40] font-semibold">Nombre del archivo</label>
        <input
          v-model="nombreArchivo"
          type="text"
          placeholder="horarios.pdf"
          class="border border-gray-300 rounded px-3 py-2 w-full mb-4 text-black focus:outline-none focus:ring-2 focus:ring-blue-200"
        />
        <div class="flex justify-end gap-2 mt-4">
          <router-link
            to="/dashboard"
            class="bg-gray-300 hover:bg-gray-400 text-blue-900 font-semibold py-2 px-6 rounded-full transition duration-300 text-center flex items-center justify-center shadow"
          >
            Cancelar
          </router-link>
          <button
            @click="exportarPDF"
            :disabled="exportando"
            class="bg-[#0A1E40] text-white font-semibold py-2 px-6 rounded-full transition duration-300 shadow hover:bg-[#143979] focus:outline-none focus:ring-2 focus:ring-[#0A1E40] disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {{ exportando ? 'Exportando...' : 'Exportar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SidebarMenu from '@/components/Sidebar.vue'; 
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  name: 'ExportarHorarioView',
  components: { SidebarMenu },
  data() {
    return {
      nombreArchivo: 'horarios.pdf',
      exportando: false
    };
  },
  methods: {
    async exportarPDF() {
      if (!this.nombreArchivo.endsWith('.pdf')) {
        this.nombreArchivo += '.pdf';
      }
      this.exportando = true;
      try {
        const response = await axios.get(`${API_URL}/exportar-horarios/`, {
          params: { nombre: this.nombreArchivo },
          responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.nombreArchivo);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
        this.$router.push('/dashboard');
      } catch (error) {
        alert('Error al exportar el PDF.');
      } finally {
        this.exportando = false;
      }
    }
  }
};
</script>

<style scoped>
.bg-gradient-to-br {
  min-height: 100vh;
}
</style>
