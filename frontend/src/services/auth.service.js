/**
 * Auth Service - Servicio de Autenticación
 * Persona 4: Paola
 * Funciones: login(), logout(), isAuthenticated()
 */

const API_URL = import.meta.env.VITE_API_BASE_URL;
const TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_INFO_KEY = 'user_info';

export default {
  // Función de login mejorada
  async login(username, password) {
    try {
      console.log('Iniciando login con:', { username });
      
      const response = await fetch(`${API_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        // Guardar tokens y información del usuario
        localStorage.setItem(TOKEN_KEY, data.access);
        localStorage.setItem(REFRESH_TOKEN_KEY, data.refresh);
        localStorage.setItem(USER_INFO_KEY, JSON.stringify(data.user || { username }));
        localStorage.setItem('username_after_login', username);
        
        console.log('Login exitoso');
        return { 
          success: true, 
          data: data,
          message: 'Login exitoso'
        };
      } else {
        console.log('Login falló:', data.detail);
        
        // Manejar diferentes tipos de errores
        let errorMessage = 'Credenciales inválidas';
        if (data.detail) {
          if (data.detail.includes('cuenta activa')) {
            errorMessage = 'Credenciales inválidas';
          } else if (data.detail.includes('No active account')) {
            errorMessage = 'Credenciales inválidas';
          } else {
            errorMessage = data.detail;
          }
        }
        
        return { 
          success: false, 
          message: errorMessage
        };
      }
    } catch (error) {
      console.error('Error en login:', error);
      return { 
        success: false, 
        message: 'Error de conexión' 
      };
    }
  },

  // Función de logout mejorada
  async logout() {
    try {
      console.log(' Cerrando sesión...');
      
      // Limpiar localStorage
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
      localStorage.removeItem(USER_INFO_KEY);
      localStorage.removeItem('username_after_login');
      
      console.log(' Logout exitoso');
      return { 
        success: true, 
        message: 'Sesión cerrada correctamente' 
      };
    } catch (error) {
      console.error(' Error en logout:', error);
      return { 
        success: false, 
        message: 'Error al cerrar sesión' 
      };
    }
  },

  // Función para verificar autenticación (verificación local robusta)
  async isAuthenticated() {
    try {
      const token = localStorage.getItem(TOKEN_KEY);
      if (!token) {
        console.log(' No hay token');
        return false;
      }

      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const isExpired = payload.exp <= Math.floor(Date.now() / 1000);

        if (isExpired) {
          console.log(' Token expirado - intentando renovar...');
          const refreshResult = await this.refreshToken();
          if (refreshResult.success) {
            console.log(' Token renovado correctamente');
            return true;
          } else {
            console.log(' No se pudo renovar el token, cerrando sesión');
            await this.logout();
            return false;
          }
        }

        if (!payload.user_id && !payload.sub) {
          console.log(' Token sin información de usuario válida');
          await this.logout();
          return false;
        }

        console.log(' Usuario autenticado (token válido)');
        return true;

      } catch (tokenError) {
        console.log(' Token malformado - limpiando sesión');
        await this.logout();
        return false;
      }

    } catch (error) {
      console.error(' Error verificando autenticación:', error);
      return false;
    }
  },

  // Obtener información del usuario
  getUserInfo() {
    try {
      const userInfo = localStorage.getItem(USER_INFO_KEY);
      if (!userInfo) return null;
      return JSON.parse(userInfo);
    } catch (error) {
      console.error('Error obteniendo info del usuario:', error);
      return null;
    }
  },

  // Obtener rol del usuario
  getUserRole() {
    try {
      const userInfo = this.getUserInfo();
      if (!userInfo) return 'guest';
      
      if (userInfo.is_director) return 'director';
      if (userInfo.is_secretary) return 'secretary';
      return 'user';
    } catch (error) {
      console.error('Error obteniendo rol del usuario:', error);
      return 'guest';
    }
  },

  // Verificar si es director
  isDirector() {
    return this.getUserRole() === 'director';
  },

  // Verificar si es secretario
  isSecretary() {
    return this.getUserRole() === 'secretary';
  },

  // Obtener token
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Petición autenticada
  async authenticatedRequest(url, options = {}) {
    try {
      const token = this.getToken();
      
      if (!token) {
        return { 
          success: false, 
          message: 'No hay token de autenticación' 
        };
      }

      const response = await fetch(`${API_URL}${url}`, {
        ...options,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      const data = await response.json();

      if (response.ok) {
        return { 
          success: true, 
          data: data 
        };
      } else {
        return { 
          success: false, 
          message: data.detail || 'Error en la petición' 
        };
      }
    } catch (error) {
      console.error(' Error en petición autenticada:', error);
      return { 
        success: false, 
        message: 'Error de conexión' 
      };
    }
  },

  // Renovar access token usando refresh token
  async refreshToken() {
    const refresh = localStorage.getItem(REFRESH_TOKEN_KEY);
    if (!refresh) return { success: false, message: 'No hay refresh token' };

    try {
      const response = await fetch(`${API_URL}/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
      });
      const data = await response.json();

      if (response.ok && data.access) {
        localStorage.setItem(TOKEN_KEY, data.access);
        return { success: true, access: data.access };
      } else {
        await this.logout();
        return { success: false, message: data.detail || 'No se pudo renovar el token' };
      }
    } catch (error) {
      await this.logout();
      return { success: false, message: 'Error de conexión al renovar token' };
    }
  },
};
