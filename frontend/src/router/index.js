import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import CreateScheduleView from '@/views/CreateScheduleView.vue';
import AuthService from '../services/auth.service'
import RecuperarContrasena from '@/views/RecuperarContrasena.vue';
import ViewProfessors from '@/views/ViewProfessors.vue';
import ViewScheduleView from '../views/ViewScheduleView.vue';
import ExportarHorarioView from '@/views/ExportarHorarioView.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // Ruta principal, redirigirá al login si no está autenticado
      redirect: '/login' // Redirige directamente al login por ahora
    },
    {
      path: '/login', // La URL para tu formulario de login
      name: 'login',
      component: LoginView // El componente que se mostrará en esta URL
    },
    {
      path: '/dashboard', // La URL para la página principal después del login
      name: 'dashboard',
      component: DashboardView, // El componente que se mostrará aquí
      meta: { requiresAuth: true } // esta ruta requiere estar logueado
    },
    {
      path: '/crear-horario', 
      name: 'crear-horario',
      component: CreateScheduleView, // Componente para crear horarios
      meta: { requiresAuth: true } // esta ruta requiere esta logueado
    },
    {
      path: '/recuperar', 
      name: 'recuperarContrasena',
      component: RecuperarContrasena, // Componente para crear horarios

    },
    {
      path: '/disponibilidad',
      name: 'disponibilidad',
      component: ViewProfessors,
      meta: { requiresAuth: true } // también protegida

    },
    {
    path: '/ver-horario',
    name: 'ViewSchedule',
    component: ViewScheduleView,
    meta: { requiresAuth: true }
    },

    {
    path: '/exportar',
    name: 'ExportarHorario',
    component: ExportarHorarioView,
    meta: { requiresAuth: true }
   },
  ]
})

// Guard de navegación - protege rutas que requieren autenticación
router.beforeEach(async (to, from, next) => {
  console.log('Router guard - Verificando acceso a:', to.path);
  
  if (to.meta.requiresAuth) {
    const isAuthenticated = await AuthService.isAuthenticated();
    
    if (!isAuthenticated) {
      console.log('Acceso denegado - Usuario no autenticado, redirigiendo a login');
      next('/login');
      return;
    }
    
    console.log('Acceso permitido - Usuario autenticado');
  }
  
  next(); // Continúa normalmente
});

export default router
