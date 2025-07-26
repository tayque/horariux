<template>
  <div class="flex min-h-screen bg-gray-100">
    <Sidebar @logout="logout" />

    <main class="flex-1 p-6 sm:p-8">
      <div class="max-w-7xl mx-auto">

        <header class="mb-8">
          <h1 class="text-4xl font-bold text-gray-800">Listado de Docentes</h1>
          <p class="text-gray-500 mt-1">Gestiona, visualiza y edita la información de los docentes.</p>
        </header>

        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left">

              <thead class="bg-[#0A1E40] text-white">
                <tr>
                  <th class="px-6 py-4 text-sm font-semibold uppercase tracking-wider">Nombre y Apellido</th>
                  <th class="px-6 py-4 text-sm font-semibold uppercase tracking-wider">Tipo Docente</th>
                  <th class="px-6 py-4 text-sm font-semibold uppercase tracking-wider">Cursos Asignados</th>
                  <th class="px-6 py-4 text-sm font-semibold uppercase tracking-wider">Disponibilidad</th>
                  <th class="px-6 py-4 text-sm font-semibold uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>

              <tbody class="text-gray-700">
                <tr v-if="isLoading">
                  <td colspan="5" class="text-center p-8">
                    <div class="text-gray-500">Cargando docentes...</div>
                  </td>
                </tr>

                <tr v-else-if="professorsForDisplay.length === 0">
                  <td colspan="5" class="text-center p-8">
                    <div class="text-gray-500">No se encontraron docentes registrados.</div>
                  </td>
                </tr>

                <tr v-else v-for="prof in professorsForDisplay" :key="prof.id"
                  class="border-b border-gray-200 hover:bg-gray-50 transition-colors duration-200">
                  <td class="px-6 py-4 align-middle whitespace-nowrap">
                    <span class="font-medium">{{ prof.fullName }}</span>
                  </td>

                  <td class="px-6 py-4 align-middle whitespace-nowrap">
                    <span :class="[
                      'px-3 py-1 text-xs font-semibold rounded-full',
                      prof.tipoDocenteDisplay === 'Contratado' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                    ]">
                      {{ prof.tipoDocenteDisplay }}
                    </span>
                  </td>

                  <td class="px-6 py-4 align-middle">
                    <div class="flex flex-wrap gap-2">
                      <span v-if="prof.cursosDisplay.length === 0" class="text-xs text-gray-500">Sin cursos</span>
                      <span v-else v-for="cursoNombre in prof.cursosDisplay" :key="cursoNombre"
                        class="bg-gray-200 text-gray-800 text-xs px-2 py-1 rounded-md">
                        {{ cursoNombre }}
                      </span>

                    </div>
                  </td>

                  <td class="px-6 py-4 align-middle">
                    <div v-if="prof.tipoDocenteDisplay === 'Contratado' && prof.availabilities.length > 0">
                      <div v-for="(dispo, index) in prof.availabilities" :key="index" class="text-sm mb-1">
                        <span class="font-semibold">{{ dispo.day }}:</span> {{ dispo.start_time }} - {{ dispo.end_time
                        }}
                      </div>
                    </div>
                    <div v-else class="text-sm text-gray-400">
                      -
                    </div>
                  </td>
                  <td class="px-6 py-4 align-middle whitespace-nowrap">
                    <div class="flex flex-col space-y-2">
                      <button @click="editarProfesor(prof)"
                        class="bg-[#0A1E40] text-white px-4 py-2 rounded-lg hover:bg-[#264782] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-all duration-200 shadow-sm hover:shadow-md">
                        Editar
                      </button>
                      <button @click="eliminarProfesor(prof)"
                        class="bg-[#5f1717] text-white px-4 py-2 rounded-lg hover:bg-[#871f1f] focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-all duration-200 shadow-sm hover:shadow-md">
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <EditProfessorModal v-if="showModal" :profesor="selectedProfessor" @cerrar="showModal = false"
      @guardado="() => { showModal = false; fetchProfessors(); }" />
  </div>
</template>

<script>
import axios from 'axios'
import Sidebar from '@/components/Sidebar.vue'
import EditProfessorModal from '@/components/EditProfessorModal.vue'
import authService from '@/services/auth.service'

const API_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  name: 'ViewProfessors',
  components: {
    Sidebar,
    EditProfessorModal
  },
  data() {
    return {
      professors: [],
      isLoading: true,
      showModal: false,
      selectedProfessor: null
    }
  },
  computed: {
    professorsForDisplay() {
      if (!this.professors) return [];
      return this.professors.map(prof => {
        const tipoDocente = prof.employment_type === 'CT' ? 'Contratado' : 'Nombrado';
        const cursos = prof.can_teach_courses || [];

        return {
          id: prof.id,
          ...prof,
          fullName: `${prof.first_name} ${prof.last_name}`,
          tipoDocenteDisplay: tipoDocente,
          cursosDisplay: cursos.map(curso => curso.name),
          availabilities: prof.availabilities || [],
        };
      });
    }

  },
  methods: {
    async fetchProfessors() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${API_URL}/listar-profesores/`);
        this.professors = response.data.results;
      } catch (error) {
        console.error('Error al obtener docentes:', error);
        this.professors = [];
      } finally {
        this.isLoading = false;
      }
    },
    editarProfesor(professor) {
      console.log("Profesor seleccionado:", professor);
      this.selectedProfessor = professor;
      this.showModal = true;
    },
    async eliminarProfesor(profesor) {
      const confirmar = confirm(`¿Estás segura de que deseas eliminar al profesor ${profesor.fullName}?`);
      if (!confirmar) return;

      try {
        await fetch(`${API_URL}/profesores/${profesor.id}/`, {
          method: 'DELETE',
        });
        this.fetchProfessors(); // Recargar lista actualizada
      } catch (error) {
        console.error('Error al eliminar:', error);
        alert('Ocurrió un error al intentar eliminar el profesor.');
      }
    },
    async logout() {
      await authService.logout();
      this.$router.push('/login');
    },


  },
  mounted() {
    this.fetchProfessors();
  }
}
</script>

<style scoped></style>