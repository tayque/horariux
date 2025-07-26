<template>
  <div class="flex min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Sidebar -->
    <Sidebar @logout="logout" />

    <!-- Main Content -->
    <div class="flex-1 px-8 py-6 overflow-auto">
      <header class="mb-6">
        <h2 class="text-3xl font-bold text-gray-800 mb-1">Gestión de horarios</h2>
      </header>
      <div class="max-w-4xl mx-auto bg-[#dce8fd] p-6 rounded-3xl shadow-lg my-auto">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Registrar Docente</h2>
        <form @submit.prevent="guardarDocente">
          <!-- Nombre -->
          <div class="mb-4">
            <label class="block text-gray-700 font-semibold mb-1">Nombres</label>
            <input v-model="form.nombre" type="text"
              class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] text-black">
          </div>

          <!-- Apellido -->
          <div class="mb-4">
            <label class="block text-gray-700 font-semibold mb-1">Apellidos</label>
            <input v-model="form.apellido" type="text"
              class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] text-black">
          </div>

          <!-- Año Académico -->
          <div class="mb-4">
            <label class="block text-gray-700 font-semibold mb-1">Año Académico</label>
            <select v-model="form.semestre"
              class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
              <option disabled value="">Seleccione año académico</option>
              <option value="1">2025 - A</option>
              <option value="2">2025 - B</option>
            </select>
          </div>

          <!-- Tipo de docente -->
          <div class="mb-4">
            <label class="block text-gray-700 font-semibold mb-2">Tipo de docente</label>
            <div class="flex gap-6">
              <label class="inline-flex items-center">
                <input type="radio" value="contratado" v-model="tipoDocente" class="form-radio text-[#0A1E40] mr-2">
                <span class="text-gray-700">Docente Contratado</span>
              </label>
              <label class="inline-flex items-center">
                <input type="radio" value="nombrado" v-model="tipoDocente" class="form-radio text-[#0A1E40] mr-2">
                <span class="text-gray-700">Docente Nombrado</span>
              </label>
            </div>
          </div>

          <!-- Mostrar si eligió tipo -->
          <div v-if="tipoDocente">
            <!-- Filtros de cursos -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label class="block text-gray-700 font-semibold mb-1">Filtrar por Año:</label>
                <select v-model="filtroAño"
                  class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
                  <option v-for="año in añosDisponibles" :key="año" :value="año">{{ año }}° año</option>
                </select>
              </div>
              <div>
                <label class="block text-gray-700 font-semibold mb-1">Filtrar por Malla:</label>
                <select v-model="filtroMalla"
                  class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
                  <option v-for="malla in mallasDisponibles" :key="malla" :value="malla">Malla {{ malla }}</option>
                </select>
              </div>
              <div>
                <label class="block text-gray-700 font-semibold mb-1">Semestre académico:</label>
                <select v-model="filtroSemestre"
                  class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
                  <option disabled value="">Selecciona un semestre</option>
                  <option :value="1">1.er semestre</option>
                  <option :value="2">2.º semestre</option>
                </select>
              </div>
            </div>
            <!-- Botón para agregar curso -->
            <div class="mt-4">
              <button type="button" @click="agregarCurso"
                class="bg-[#0A1E40] text-white px-4 py-2 rounded-full hover:bg-[#143979] font-semibold transition">
                + Agregar curso
              </button>
            </div>

            <!-- Lista de cursos agregados -->
            <div v-if="form.cursos.length > 0" class="mt-4">
              <label class="block text-gray-700 font-semibold mb-2">Cursos asignados:</label>
              <ul class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
                <li v-for="(cursoId, index) in form.cursos" :key="index" class="flex justify-between items-center">
                  <span class="text-gray-800">
                    {{ mostrarNombreCurso(cursoId) }}
                  </span>
                  <button type="button" @click="eliminarCurso(index)"
                    class="text-red-600 hover:text-red-800 hover:underline text-sm">Eliminar</button>
                </li>
              </ul>
            </div>

            <div v-if="cursosCargados">
              <label class="block text-gray-700 font-semibold mb-1">Cursos disponibles</label>
              <select v-model="cursoSeleccionado"
                class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
                <option disabled value="">Seleccione un curso...</option>
                <option v-for="curso in cursosFiltrados" :key="curso.id" :value="curso.id">
                  {{ curso.name }} – {{ curso.academic_year_level.year_level }}° año / Semestre {{
                    curso.academic_year_level.semester_number }} / Malla {{ curso.curriculum_year }}
                </option>
              </select>
            </div>
            <div v-else class="text-sm text-gray-600 italic">Cargando cursos...</div>
          </div>
          <!-- Disponibilidad horaria para contratados -->
          <div v-if="tipoDocente === 'contratado'" class="mt-8">
            <label class="block text-gray-700 font-bold mb-2">Disponibilidad Horaria</label>

            <!-- Agregar nuevo día -->
            <div class="flex items-center gap-4 mb-4">
              <select v-model="diaNuevo"
                class="px-4 py-2 rounded-full border border-gray-300 bg-white text-[#0A1E40] font-semibold focus:ring-2 focus:ring-[#0A1E40]">
                <option disabled value="">Selecciona un día</option>
                <option v-for="dia in diasNoSeleccionados" :key="dia" :value="dia">{{ dia }}</option>
              </select>
              <button type="button" @click="agregarDia"
                class="bg-[#0A1E40] text-white px-4 py-2 rounded-full hover:bg-[#143979] font-semibold transition">Agregar
                día</button>
            </div>

            <!-- Mostrar días agregados -->
            <div v-for="(dia, diaIndex) in form.disponibilidad" :key="dia.dia"
              class="mb-4 p-4 rounded-xl bg-white border border-gray-200">
              <div class="flex justify-between items-center mb-2">
                <strong class="text-[#0A1E40]">{{ dia.dia }}</strong>
              </div>
              <div v-for="(hora, horaIndex) in dia.horas" :key="horaIndex" class="flex gap-4 mb-2">
                <input v-model="hora.inicio" type="time"
                  class="px-4 py-2 rounded-full border border-gray-300 text-[#0A1E40] font-medium focus:ring-2 focus:ring-[#0A1E40]">
                <input v-model="hora.fin" type="time"
                  class="px-4 py-2 rounded-full border border-gray-300 text-[#0A1E40] font-medium focus:ring-2 focus:ring-[#0A1E40]">
                <button @click="eliminarHora(diaIndex, horaIndex)" type="button"
                  class="text-red-500 hover:text-red-700 text-sm font-medium">Eliminar</button>
              </div>
              <button @click="agregarHora(diaIndex)" type="button"
                class="mt-2 text-sm text-[#0A1E40] font-semibold hover:underline">+ Agregar hora</button>
            </div>
          </div>

          <!-- Botón guardar -->
          <div class="mt-6 text-right">
            <button type="submit"
              class="bg-[#0A1E40] text-white px-6 py-2 rounded-full hover:bg-[#143260] focus:outline-none focus:ring-2 focus:ring-[#0A1E40] shadow">
              Guardar Docente
            </button>
          </div>
        </form>
      </div>
      <div class="max-w-4xl mx-auto bg-[#dce8fd] p-6 rounded-3xl shadow-lg mt-7">
        <h2 class="text-2xl font-bold mb-4 text-gray-800 text-center">Importar docentes desde archivo</h2>
        <form @submit.prevent="subirArchivo" class="flex flex-col items-center gap-6">

          <label for="archivoInput"
            class="cursor-pointer bg-white text-[#0A1E40] px-6 py-2 rounded-full font-semibold hover:bg-[#b5d1ff] transition text-center w-full">
            Seleccionar archivo
          </label>

          <input id="archivoInput" type="file"
            accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
            @change="handleArchivo" class="hidden">

          <div v-if="archivoDocentes" class="text-gray-700 text-sm italic">
            Archivo seleccionado: {{ archivoDocentes.name }}
          </div>

          <button type="submit" class="px-6 py-2 bg-[#0A1E40] text-white rounded-full hover:bg-[#143979] font-bold">
            Subir archivo
          </button>
        </form>
      </div>
      <!-- Generar Horario -->
      <div class="max-w-4xl mx-auto bg-[#dce8fd] p-6 rounded-3xl shadow-lg mt-7">
        <h2 class="text-2xl font-bold mb-4 text-gray-800 text-center">Generar Horario</h2>
        <form @submit.prevent="generarHorario" class="space-y-6">

          <!-- Año académico -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Año Académico</label>
            <select v-model="formGenerar.semestre"
              class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
              <option disabled value="">Seleccione año académico</option>
              <option value="1">2025 - A</option>
              <option value="2">2025 - B</option>
            </select>
          </div>

          <!-- Malla por año académico -->
          <div>
            <label class="block text-gray-700 font-semibold mb-2">Seleccione la malla por año académico:</label>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="anio in [1, 2, 3, 4, 5]" :key="anio">
                <label class="block text-gray-600 font-medium mb-1">{{ anio }}° año:</label>
                <select v-model="formGenerar.mallaPorAño[anio]"
                  class="w-full px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-[#0A1E40] bg-white text-[#0A1E40] font-semibold">
                  <option disabled value="">Seleccione malla</option>
                  <option v-for="malla in mallasDisponibles" :key="malla" :value="malla">Malla {{ malla }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Filtros para cursos con sección C -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">¿Desea añadir cursos con sección C?</label>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
              <div>
                <label class="block text-gray-700 text-sm mb-1">Año</label>
                <select v-model="filtroC.año"
                  class="w-full px-4 py-2 border rounded-full bg-white text-[#0A1E40] font-semibold">
                  <option v-for="año in añosDisponibles" :key="año" :value="año">{{ año }}° año</option>
                </select>
              </div>
              <div>
                <label class="block text-gray-700 text-sm mb-1">Semestre</label>
                <select v-model="filtroC.semestre"
                  class="w-full px-4 py-2 border rounded-full bg-white text-[#0A1E40] font-semibold">
                  <option disabled value="">Selecciona un semestre</option>
                  <option :value="1">1.er semestre</option>
                  <option :value="2">2.º semestre</option>
                </select>
              </div>
              <div>
                <label class="block text-gray-700 text-sm mb-1">Malla</label>
                <select v-model="filtroC.malla"
                  class="w-full px-4 py-2 border rounded-full bg-white text-[#0A1E40] font-semibold">
                  <option v-for="m in mallasDisponibles" :key="m" :value="m">Malla {{ m }}</option>
                </select>
              </div>
            </div>

            <div class="mb-3">
              <label class="block text-gray-700 font-semibold mb-1">Cursos filtrados (sección C)</label>

              <div v-if="!cursosCargados" class="italic text-sm text-gray-500">
                Cargando cursos...
              </div>

              <div v-else>
                <select v-model="cursoCSeleccionado"
                  class="w-full px-4 py-2 border rounded-full bg-white text-[#0A1E40] font-semibold">
                  <option disabled value="">Seleccione un curso...</option>
                  <option v-for="curso in cursosFiltradosC" :key="curso.id" :value="curso.id">
                    {{ curso.name }} – {{ curso.academic_year_level.year_level }}° / Semestre {{
                      curso.academic_year_level.semester_number }} / Malla {{ curso.curriculum_year }}
                  </option>
                </select>
                <button type="button" @click="agregarCursoC"
                  class="mt-2 bg-[#0A1E40] text-white px-4 py-2 rounded-full hover:bg-[#143979] font-semibold">
                  Agregar curso
                </button>
              </div>
            </div>

            <div v-if="formGenerar.cursosC.length > 0" class="mb-4">
              <label class="block text-gray-700 font-semibold mb-1">Cursos con sección C agregados:</label>
              <ul class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
                <li v-for="(cursoId, index) in formGenerar.cursosC" :key="index"
                  class="flex justify-between items-center">
                  <span class="text-gray-800">{{ mostrarNombreCurso(cursoId) }}</span>
                  <button type="button" @click="eliminarCursoC(index)"
                    class="text-red-600 hover:text-red-800 text-sm">Eliminar</button>
                </li>
              </ul>
            </div>
          </div>

          <!-- Botón de generación -->
          <div class="text-right">
            <button type="submit"
              class="bg-[#0A1E40] text-white px-6 py-2 rounded-full hover:bg-[#143979] font-semibold transition">
              Generar Horario
            </button>
          </div>

          <!-- Mensaje -->
          <div v-if="mensajeGeneracion" :class="mensajeError ? 'text-red-600' : 'text-green-700'"
            class="mt-4 text-center font-semibold">
            {{ mensajeGeneracion }}
          </div>

        </form>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import authService from '@/services/auth.service';
import Sidebar from '@/components/Sidebar.vue';

const API_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  name: 'CreateScheduleView',
  components: {
    Sidebar
  },
  data() {
    return {
      añosDisponibles: [1, 2, 3, 4, 5],
      diaNuevo: '',
      tipoDocente: '',
      docenteGuardado: false,
      archivoDocentes: null,
      cursos: [],
      cursosDisponibles: [],
      cursoSeleccionado: '',
      filtroAño: null,
      filtroMalla: null,
      filtroSemestre: null,
      cursosCargados: false,
      mallasDisponibles: [2017, 2025],
      form: {
        nombre: '',
        apellido: '',
        semestre: '',
        anios: [],
        cursos: [],
        disponibilidad: []
      },
      diasDisponibles: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],

      // Parte de generación de horarios
      formGenerar: {
        semestre: '',
        mallaPorAño: {
          1: '',
          2: '',
          3: '',
          4: '',
          5: ''
        },
        cursosC: []
      },
      filtroC: {
        año: null,
        semestre: null,
        malla: null
      },
      cursoCSeleccionado: '',
      mensajeGeneracion: '',
      mensajeError: false
    }
  },
  computed: {
    cursosFiltrados() {
      return this.cursosDisponibles.filter(curso => {
        const cumpleAño = this.filtroAño ? curso.academic_year_level.year_level === this.filtroAño : true;
        const cumpleSemestre = this.filtroSemestre ? curso.academic_year_level.semester_number === this.filtroSemestre : true;
        const cumpleMalla = this.filtroMalla ? curso.curriculum_year === this.filtroMalla : true;
        return cumpleAño && cumpleSemestre && cumpleMalla;
      });
    },
    cursosFiltradosC() {
      return this.cursosDisponibles.filter(curso => {
        const cumpleAño = this.filtroC.año ? curso.academic_year_level.year_level === this.filtroC.año : true;
        const cumpleSemestre = this.filtroC.semestre ? curso.academic_year_level.semester_number === this.filtroC.semestre : true;
        const cumpleMalla = this.filtroC.malla ? curso.curriculum_year === this.filtroC.malla : true;
        return cumpleAño && cumpleSemestre && cumpleMalla;
      });
    },
    diasNoSeleccionados() {
      const seleccionados = this.form.disponibilidad.map(d => d.dia);
      return this.diasDisponibles.filter(d => !seleccionados.includes(d));
    }
  },
  methods: {
    async fetchCursos() {
      try {
        const res = await fetch(`${API_URL}/cursos/`);
        const data = await res.json();
        this.cursosDisponibles = data.courses;
        this.cursosCargados = true;
      } catch (error) {
        console.error('Error al cargar cursos:', error);
      }
    },
    agregarCursoC() {
      if (this.cursoCSeleccionado && !this.formGenerar.cursosC.includes(this.cursoCSeleccionado)) {
        this.formGenerar.cursosC.push(this.cursoCSeleccionado);
        this.cursoCSeleccionado = '';
      }
    },
    eliminarCursoC(index) {
      this.formGenerar.cursosC.splice(index, 1);
    },
    async generarHorario() {
      try {
        const añosFaltantes = Object.entries(this.formGenerar.mallaPorAño)
          .filter(([año, malla]) => !malla)
          .map(([año]) => año);
        if (añosFaltantes.length > 0) {
          this.mensajeGeneracion = `Faltan mallas para los años: ${añosFaltantes.join(', ')}`;
          this.mensajeError = true;
          return;
        }

        const payload = {
          term_id: parseInt(this.formGenerar.semestre), 
          mallas_por_año: this.formGenerar.mallaPorAño,
          cursos_c: this.formGenerar.cursosC
        };

        console.log("Enviando payload para generar horario:", payload);

        const res = await axios.post(`${API_URL}/generar-horario/`, payload);

        this.mensajeGeneracion = "¡Horario generado exitosamente! Puedes revisarlo en la sección de Horarios.";
        this.mensajeError = false;
      } catch (error) {
        if (error.response && error.response.data) {
          console.error('Error al generar horario (validación):', error.response.data);
          this.mensajeGeneracion = "Error: " + JSON.stringify(error.response.data, null, 2);
        } else {
          console.error('Error de red o inesperado:', error.message);
          this.mensajeGeneracion = "Error de red o inesperado al generar horario.";
        }
        this.mensajeError = true;
      }
    },

    guardarDocente() {
      const datosParaEnviar = {
        first_name: this.form.nombre.toUpperCase(),
        last_name: this.form.apellido.toUpperCase(),
        academic_unit: 1, // cambiar luego si es necesario
        employment_type: this.tipoDocente === 'nombrado' ? 'FT' : 'CT',
        academic_year_level: this.form.semestre,
        can_teach_courses: this.form.cursos,
        curriculum: this.form.malla,
      };

      if (this.tipoDocente === 'contratado') {
        datosParaEnviar.availabilities = this.form.disponibilidad.flatMap(d =>
          d.horas.map(hora => ({
            day: d.dia,
            start_time: hora.inicio,
            end_time: hora.fin
          }))
        );
      }

      console.log('Datos enviados:', datosParaEnviar);
      axios.post(`${API_URL}/profesores/`, datosParaEnviar)
        .then(response => {
          console.log('Guardado exitosamente:', response.data);
          this.docenteGuardado = true;
        })
        .catch(error => {
          if (error.response) {
            console.error('Error de validación:', error.response.data);
          } else {
            console.error('Error de red u otro:', error.message);
          }
        });
    },
    agregarCurso() {
      if (this.cursoSeleccionado && !this.form.cursos.includes(this.cursoSeleccionado)) {
        this.form.cursos.push(this.cursoSeleccionado);
        this.cursoSeleccionado = '';
      }
    },
    eliminarCurso(index) {
      this.form.cursos.splice(index, 1);
    },
    mostrarNombreCurso(id) {
      const curso = this.cursosDisponibles.find(c => c.id === id);
      return curso ? `${curso.name} – ${curso.academic_year_level.year_level}° / Semestre ${curso.academic_year_level.semester_number} / Malla ${curso.curriculum_year}` : 'Curso desconocido';
    },
    resetearFormulario() {
      this.form = {
        nombre: '',
        apellido: '',
        semestre: '',
        anios: [],
        cursos: [],
        disponibilidad: []
      };
      this.tipoDocente = '';
      this.docenteGuardado = false;
    }
    ,
    agregarDia() {
      if (this.diaNuevo && !this.form.disponibilidad.some(d => d.dia === this.diaNuevo)) {
        this.form.disponibilidad.push({ dia: this.diaNuevo, horas: [{ inicio: '', fin: '' }] });
        this.diaNuevo = '';
      }
    },
    agregarHora(diaIndex) {
      this.form.disponibilidad[diaIndex].horas.push({ inicio: '', fin: '' });
    },
    eliminarHora(diaIndex, horaIndex) {
      const horas = this.form.disponibilidad[diaIndex].horas;
      horas.splice(horaIndex, 1);

      if (horas.length === 0) {
        this.form.disponibilidad.splice(diaIndex, 1);
      }
    },
    handleArchivo(event) {
      this.archivoDocentes = event.target.files[0];
    },
    subirArchivo() {
      if (!this.archivoDocentes) {
        alert('Selecciona un archivo antes de subir.');
        return;
      }

      const formData = new FormData();
      formData.append('archivo', this.archivoDocentes);
      console.log('Archivo listo para subir:', this.archivoDocentes.name);
    },
    async logout() {
      await authService.logout();
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchCursos();
  }

}
</script>
