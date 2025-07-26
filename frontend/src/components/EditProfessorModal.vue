<template>
  <div class="modal-backdrop fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div
      class="modal-box bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl text-gray-800 max-h-[90vh] overflow-y-auto">
      <h2 class="text-2xl font-bold mb-6 text-[#0A1E40]">Editar Profesor</h2>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-semibold mb-1">Nombre:</label>
          <input v-model="prof.first_name"
            class="w-full border border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Nombre" />
        </div>

        <div>
          <label class="block text-sm font-semibold mb-1">Apellido:</label>
          <input v-model="prof.last_name"
            class="w-full border border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Apellido" />
        </div>

        <div>
          <label class="block text-sm font-semibold mb-1">Tipo de Empleo:</label>
          <select v-model="prof.employment_type"
            class="w-full border border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="FT">Nombrado</option>
            <option value="CT">Contratado</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-semibold mb-1">Cursos:</label>

          <div v-if="prof.can_teach_courses.length">
            <label class="block text-sm font-semibold mb-1">Cursos actuales:</label>
            <div class="flex flex-wrap gap-2 mb-3">
              <span v-for="curso in cursosAsignadosDetalle" :key="curso.id"
                class="flex items-center bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-md">
                {{ curso.name }} –
                {{ curso.academic_year_level.year_level }}° año /
                Semestre {{ curso.academic_year_level.semester_number }} /
                Malla {{ curso.curriculum_year }}
                <button @click="removerCurso(curso.id)"
                  class="ml-2 text-red-500 hover:text-red-700 font-bold">×</button>
              </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-semibold mb-1">Filtrar por Año:</label>
              <select v-model="filtroAño" class="w-full border border-gray-300 p-2 rounded-lg shadow-sm">
                <option v-for="año in añosDisponibles" :key="año" :value="año">{{ año }}° año</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-semibold mb-1">Filtrar por Malla:</label>
              <select v-model="filtroMalla" class="w-full border border-gray-300 p-2 rounded-lg shadow-sm">
                <option v-for="malla in mallasDisponibles" :key="malla" :value="malla">Malla {{ malla }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-1">Semestre académico:</label>
            <select v-model="filtroSemestre"
              class="w-full border border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option disabled value="">Selecciona un semestre</option>
              <option :value="1">1.er semestre</option>
              <option :value="2">2.º semestre</option>
            </select>
          </div>

          <div v-if="cursosCargados">
            <div>
              <label class="block text-sm font-semibold mb-1">Agregar nuevos cursos:</label>
              <select v-model="cursoAAgregar"
                class="w-full border border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option disabled value="">Seleccione un curso...</option>
                <option v-for="curso in cursosFiltrados" :key="curso.id" :value="curso.id">
                  {{ curso.name }} – {{ curso.academic_year_level.year_level }}° año / Semestre {{
                    curso.academic_year_level.semester_number }} / Malla {{ curso.curriculum_year }}
                </option>
              </select>
              <button @click="agregarCurso"
                class="mt-2 bg-green-100 text-green-800 text-sm px-3 py-1 rounded-md hover:bg-green-200 transition">
                ➕ Agregar curso
              </button>
            </div>

          </div>
          <div v-else class="text-sm text-gray-500 italic">Cargando cursos...</div>

        </div>

        <div v-if="prof.employment_type === 'CT'">
          <label class="block text-sm font-semibold mb-1">Disponibilidad:</label>
          <div v-for="(disp, index) in prof.availabilities" :key="index"
            class="p-4 mb-3 bg-gray-50 border border-gray-200 rounded-lg">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-medium mb-1">Día:</label>
                <select v-model="disp.day"
                  class="w-full border border-gray-300 p-2 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option disabled value="">Seleccione un día</option>
                  <option v-for="dia in diasDisponibles" :key="dia" :value="dia">{{ dia }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Inicio:</label>
                <input v-model="disp.start_time" type="time"
                  class="w-full border border-gray-300 p-2 rounded-md shadow-sm" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Fin:</label>
                <input v-model="disp.end_time" type="time"
                  class="w-full border border-gray-300 p-2 rounded-md shadow-sm" />
              </div>
            </div>
          </div>

          <button @click="agregarDisponibilidad"
            class="text-sm bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-lg transition duration-150 shadow-sm">
            ➕ Agregar disponibilidad
          </button>
        </div>
      </div>

      <div class="flex justify-end mt-8 gap-4">
        <button @click="guardarCambios"
          class="bg-[#0A1E40] text-white px-5 py-2 rounded-lg hover:bg-[#264782] focus:outline-none focus:ring-2 focus:bg-[#264782] focus:ring-opacity-50 shadow-sm">
          Guardar
        </button>
        <button @click="$emit('cerrar')"
          class="bg-gray-400 text-white px-5 py-2 rounded-lg hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50 shadow-sm">
          Cancelar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
const API_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  props: ['profesor'],
  emits: ['cerrar', 'guardado'],
  data() {
    const copia = JSON.parse(JSON.stringify(this.profesor));
    console.log("Copia del profesor:", copia);
    copia.can_teach_courses = copia.can_teach_courses.map(c => typeof c === 'object' ? c.id : c);
    return {
      prof: copia,
      diasDisponibles: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
      cursosDisponibles: [],
      filtroAño: null,
      filtroMalla: null,
      filtroSemestre: null,
      añosDisponibles: [1, 2, 3, 4, 5],
      mallasDisponibles: [2017, 2025],
      cursosCargados: false,
      cursoAAgregar: '',
    };
  },

  computed: {
    cursosFiltrados() {
      const idsAsignados = new Set(this.prof.can_teach_courses);
      return this.cursosDisponibles.filter(curso => {
        const cumpleAño = this.filtroAño ? curso.academic_year_level.year_level === this.filtroAño : true;
        const cumpleSemestre = this.filtroSemestre ? curso.academic_year_level.semester_number === this.filtroSemestre : true;
        const cumpleMalla = this.filtroMalla ? curso.curriculum_year === this.filtroMalla : true;
        const noEstaAsignado = !idsAsignados.has(curso.id);
        return cumpleAño && cumpleSemestre && cumpleMalla && noEstaAsignado;
      });
    },
    cursosAsignadosDetalle() {
      const cursoMap = new Map(this.cursosDisponibles.map(c => [c.id, c]));
      return this.prof.can_teach_courses
        .map(id => cursoMap.get(id))
        .filter(Boolean);
    }
  },
  methods: {
    async fetchCursos() {
      try {
        const res = await fetch(`${API_URL}/cursos/`);
        const data = await res.json();
        this.cursosDisponibles = data.courses;
        this.cursosCargados = true;
      } catch (e) {
        console.error('Error al cargar cursos:', e);
      }
    },
    removerCurso(id) {
      this.prof.can_teach_courses = this.prof.can_teach_courses.filter(cursoId => cursoId !== id);
    },
    agregarCurso() {
      if (this.cursoAAgregar && !this.prof.can_teach_courses.includes(this.cursoAAgregar)) {
        this.prof.can_teach_courses.push(this.cursoAAgregar);
        this.cursoAAgregar = '';
      }
    },


    agregarDisponibilidad() {
      this.prof.availabilities.push({ day: '', start_time: '', end_time: '' });
    },
    async guardarCambios() {
      if (this.cursoAAgregar) {
        const continuar = confirm("Tienes un curso seleccionado pero no agregado. ¿Deseas continuar de todas formas?");
        if (!continuar) return;
      }
      const datos = {
        first_name: this.prof.first_name,
        last_name: this.prof.last_name,
        employment_type: this.prof.employment_type,
        academic_unit: this.prof.academic_unit,
        can_teach_courses_ids: this.prof.can_teach_courses,
        availabilities: this.prof.availabilities
      };

      if (datos.employment_type === 'FT') {
        datos.availabilities = [];
      }
      
      try {
        const response = await fetch(`${API_URL}/profesores/${this.prof.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(datos)
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error en la respuesta del servidor:", errorData);
          return;
        }

        this.$emit('guardado');
        this.cursoAAgregar = '';
      } catch (error) {
        console.error('Error al guardar:', error);
      }
    }
  },

  mounted() {
    this.fetchCursos();
  }
};
</script>
