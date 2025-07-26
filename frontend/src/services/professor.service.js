// Servicio para manejar operaciones con docentes
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// Configurar interceptor para incluir token de autenticación
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const professorService = {
  
  /**
   * Crear un nuevo docente
   * @param {Object} professorData - Datos del docente
   * @returns {Promise} Response del servidor
   */
  async createProfessor(professorData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/professors/`, professorData)
      return {
        success: true,
        data: response.data,
        message: 'Docente creado exitosamente'
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message,
        message: 'Error al crear el docente'
      }
    }
  },

  /**
   * Obtener todos los docentes
   * @returns {Promise} Lista de docentes
   */
  async getAllProfessors() {
    try {
      const response = await axios.get(`${API_BASE_URL}/professors/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },

  /**
   * Obtener un docente por ID
   * @param {number} id - ID del docente
   * @returns {Promise} Datos del docente
   */
  async getProfessorById(id) {
    try {
      const response = await axios.get(`${API_BASE_URL}/professors/${id}/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },

  /**
   * Actualizar un docente
   * @param {number} id - ID del docente
   * @param {Object} professorData - Datos actualizados
   * @returns {Promise} Response del servidor
   */
  async updateProfessor(id, professorData) {
    try {
      const response = await axios.put(`${API_BASE_URL}/professors/${id}/`, professorData)
      return {
        success: true,
        data: response.data,
        message: 'Docente actualizado exitosamente'
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message,
        message: 'Error al actualizar el docente'
      }
    }
  },

  /**
   * Eliminar un docente
   * @param {number} id - ID del docente
   * @returns {Promise} Response del servidor
   */
  async deleteProfessor(id) {
    try {
      await axios.delete(`${API_BASE_URL}/professors/${id}/`)
      return {
        success: true,
        message: 'Docente eliminado exitosamente'
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message,
        message: 'Error al eliminar el docente'
      }
    }
  },

  /**
   * Agregar disponibilidad a un docente de tiempo parcial
   * @param {number} professorId - ID del docente
   * @param {Object} availabilityData - Datos de disponibilidad
   * @returns {Promise} Response del servidor
   */
  async addAvailability(professorId, availabilityData) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/professors/${professorId}/add_availability/`,
        availabilityData
      )
      return {
        success: true,
        data: response.data,
        message: 'Disponibilidad agregada exitosamente'
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message,
        message: 'Error al agregar disponibilidad'
      }
    }
  },

  /**
   * Obtener disponibilidades de un docente
   * @param {number} professorId - ID del docente
   * @returns {Promise} Lista de disponibilidades
   */
  async getProfessorAvailabilities(professorId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/professors/${professorId}/availabilities/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },

  /**
   * Obtener docentes de tiempo parcial sin disponibilidades
   * @returns {Promise} Lista de docentes
   */
  async getPartTimeWithoutAvailability() {
    try {
      const response = await axios.get(`${API_BASE_URL}/professors/part_time_without_availability/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },

  /**
   * Obtener unidades académicas para el formulario
   * @returns {Promise} Lista de unidades académicas
   */
  async getAcademicUnits() {
    try {
      const response = await axios.get(`${API_BASE_URL}/academic-units/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },

  /**
   * Obtener cursos disponibles para asignar al docente
   * @returns {Promise} Lista de cursos
   */
  async getCourses() {
    try {
      const response = await axios.get(`${API_BASE_URL}/courses/`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || error.message
      }
    }
  },
  /**
   * Validar datos del formulario antes de enviar
   * @param {Object} professorData - Datos a validar
   * @returns {Object} Resultado de validación
   */
  validateProfessorData(professorData) {
    const errors = {}

    // Validar nombre completo
    if (!professorData.full_name || professorData.full_name.trim().length < 2) {
      errors.full_name = 'El nombre completo es requerido y debe tener al menos 2 caracteres'
    }

    // Validar unidad académica
    if (!professorData.academic_unit) {
      errors.academic_unit = 'La unidad académica es requerida'
    }

    // Validar tipo de nombramiento
    if (!professorData.employment_type) {
      errors.employment_type = 'El tipo de nombramiento es requerido'
    }

    // Validar disponibilidades para tiempo parcial
    if (professorData.employment_type === 'PT') {
      if (!professorData.availabilities || professorData.availabilities.length === 0) {
        errors.availabilities = 'Los docentes de tiempo parcial deben tener al menos una disponibilidad'
      } else {
        // Validar cada disponibilidad
        professorData.availabilities.forEach((availability, index) => {
          if (!availability.day && availability.day !== 0) {
            errors[`availability_${index}_day`] = 'El día es requerido'
          }
          if (!availability.start_time) {
            errors[`availability_${index}_start_time`] = 'La hora de inicio es requerida'
          }
          if (!availability.end_time) {
            errors[`availability_${index}_end_time`] = 'La hora de fin es requerida'
          }
          if (availability.start_time && availability.end_time && 
              availability.start_time >= availability.end_time) {
            errors[`availability_${index}_time`] = 'La hora de inicio debe ser menor que la hora de fin'
          }
        })
      }
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    }
  }
}

export default professorService
