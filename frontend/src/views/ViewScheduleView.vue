<template>
  <div class="flex min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <Sidebar />

    <div class="flex-1 px-8 py-6 overflow-auto">
      <header class="mb-6">
        <h2 class="text-3xl font-bold text-gray-800 mb-1">Visualización de horarios</h2>
      </header>

      <div class="flex flex-wrap gap-2 justify-center mb-6">
        <button
          v-for="(anio, index) in anios"
          :key="index"
          :class="[
            'px-4 py-2 rounded-full font-semibold transition-all duration-200',
            anioSeleccionado === anio
              ? 'bg-[#0A1E40] text-white shadow-lg'
              : 'bg-white text-[#0A1E40] border hover:bg-gray-50'
          ]"
          @click="cambiarAño(anio)"
        >
          {{ anio }}
        </button>
      </div>

      <h3 class="text-2xl font-bold text-center text-[#0A1E40] mb-4">
        AULA {{ aulaActual }}
      </h3>

      <div class="overflow-x-auto">
        <table class="min-w-full bg-white shadow-xl rounded-xl text-center text-[#0A1E40]">
          <thead class="bg-[#0A1E40] text-white">
            <tr>
              <th class="py-3 px-4 font-semibold">Hora</th>
              <th class="py-3 px-4 font-semibold">Lunes</th>
              <th class="py-3 px-4 font-semibold">Martes</th>
              <th class="py-3 px-4 font-semibold">Miércoles</th>
              <th class="py-3 px-4 font-semibold">Jueves</th>
              <th class="py-3 px-4 font-semibold">Viernes</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(fila, i) in horarios"
              :key="i"
              class="border-b hover:bg-blue-50 transition-colors duration-200"
            >
              <td class="py-3 px-4 font-medium bg-[#0A1E40] text-white">{{ fila.hora }}</td>
              <td 
                v-for="dia in ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']"
                :key="dia"
                v-show="fila[dia].isFirst || !fila[dia].curso"
                :rowspan="fila[dia].curso ? fila[dia].duracion : 1"
                class="py-3 px-4 text-sm"
              >
                {{ fila[dia].curso }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Leyenda -->
      <div class="mt-4 text-sm text-gray-600 text-center">
        <p><strong>Nota:</strong> Cada bloque tiene una duración de 50 minutos. Los cursos pueden ocupar múltiples bloques consecutivos.</p>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import axios from 'axios';
const API_URL = import.meta.env.VITE_API_BASE_URL;
export default {
  name: 'ViewScheduleView',
  components: { Sidebar },
  data() {
    return {
      anios: ['1° año', '2° año', '3° año', '4° año', '5° año', 'Reprogramados'],
      anioSeleccionado: '1° año',
      aulaActual: '301',
      horarios: [
        { hora: '07:00 - 07:50', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '07:50 - 08:40', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '08:50 - 09:40', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '09:40 - 10:30', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '10:40 - 11:30', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '11:30 - 12:20', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '12:20 - 13:10', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '13:10 - 14:00', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '14:00 - 14:50', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '14:50 - 15:40', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '15:50 - 16:40', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '16:40 - 17:30', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '17:30 - 18:20', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '18:30 - 19:20', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
        { hora: '19:20 - 20:10', lunes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, martes: { curso: '', isFirst: false, isLast: false, duracion: 1 }, miercoles: { curso: '', isFirst: false, isLast: false, duracion: 1 }, jueves: { curso: '', isFirst: false, isLast: false, duracion: 1 }, viernes: { curso: '', isFirst: false, isLast: false, duracion: 1 } },
      ]
    };
  },
  methods: {

    horaAMinutos(hora) {
      const [h, m] = hora.split(':').map(Number);
      return h * 60 + m;
    },

    encontrarIndiceHora(horaInicio) {
      const minutosInicio = this.horaAMinutos(horaInicio);
      
      const horariosBase = [
        420,  // 07:00
        470,  // 07:50
        530,  // 08:50
        580,  // 09:40
        640,  // 10:40
        690,  // 11:30
        740,  // 12:20
        790,  // 13:10
        840,  // 14:00
        890,  // 14:50
        950,  // 15:50
        1000, // 16:40
        1050, // 17:30
        1110, // 18:30
        1160  // 19:20
      ];

      return horariosBase.findIndex(h => h === minutosInicio);
    },

    async cambiarAño(anio) {
      this.anioSeleccionado = anio;

      switch (anio) {
        case '1° año': this.aulaActual = '301'; break;
        case '2° año': this.aulaActual = '302'; break;
        case '3° año': this.aulaActual = '306'; break;
        case '4° año': this.aulaActual = '201'; break;
        case '5° año': this.aulaActual = '205'; break;
        default: this.aulaActual = '—'; break;
      }

      this.limpiarHorarios();

      try {
        const response = await axios.get(`${API_URL}/horarios/?anio=${anio}`);
        const datos = response.data;

        console.log('Datos recibidos:', datos);

        datos.forEach(sesion => {
          const { hora, duracion, dia, curso } = sesion;
          const indiceInicio = this.encontrarIndiceHora(hora);
          
          if (indiceInicio === -1) {
            console.warn(`No se encontró índice para la hora: ${hora}`);
            return;
          }

          for (let i = 0; i < duracion; i++) {
            const indice = indiceInicio + i;
            
            if (indice >= this.horarios.length) {
              console.warn(`Índice fuera de rango: ${indice}`);
              break;
            }

            this.horarios[indice][dia].curso = curso;
            this.horarios[indice][dia].isFirst = i === 0;
            this.horarios[indice][dia].isLast = i === duracion - 1;
            this.horarios[indice][dia].duracion = duracion;
          }
        });

      } catch (error) {
        console.error('Error al cargar horarios:', error);
        // Mostrar mensaje de error al usuario
        alert('Error al cargar los horarios. Por favor, intente nuevamente.');
      }
    },

    limpiarHorarios() {
      this.horarios.forEach(fila => {
        ['lunes', 'martes', 'miercoles', 'jueves', 'viernes'].forEach(dia => {
          fila[dia] = { curso: '', isFirst: false, isLast: false, duracion: 1 };
        });
      });
    }
  },
  mounted() {
    this.cambiarAño(this.anioSeleccionado);
  }
};
</script>

<style scoped>
table {
  border-collapse: separate;
  border-spacing: 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(10, 30, 64, 0.1);
}

th, td {
  border: 1px solid #e2e8f0;
  transition: background-color 0.2s ease;
}

tbody tr:hover {
  background-color: #f8fafc;
}

thead {
  background-color: #0A1E40;
  color: white;
}

td {
  font-size: 0.9rem;
  vertical-align: middle;
  padding: 12px 16px;
  width: 180px; 
}

th {
  vertical-align: middle;
  padding: 12px 16px;
  width: 180px; 
}

th:first-child,
td:first-child {
  background-color: #0a1e40;
  font-weight: bold;
  color: white;
  border-right: 2px solid #1e40af;
  width: 120px !important;
  min-width: 120px;
}

/* Efecto hover limpio */
tr:hover td {
  background-color: #f1f5f9;
}

tr:hover td:first-child {
  background-color: #1e40af;
}
</style>