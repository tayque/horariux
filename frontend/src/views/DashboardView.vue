
<template>
  <div class="flex min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Sidebar -->
    <Sidebar @logout="logout" />

    <!-- Main Content -->
    <div class="flex-1 px-11 py-11 overflow-auto flex flex-col">
      <header class="mb-6">
        <h1 class="text-5xl font-kdam text-[#0A1E40] flex items-center">
          <i class="fas fa-user-circle mr-2 text-5xl text-[#0A1E40]"></i>
          Bienvenida, {{ displayName }}
        </h1>
      </header>

      <!-- Mensaje en etiqueta separada arriba del monitor -->
      <div class="text-center mb-4">
        <div class="bg-[#02162E] rounded-lg shadow-lg px-6 py-3 border border-[#02162E] w-[70vw] mx-auto max-w-full">
          <p class="text-white text-2xl md:text-3xl font-medium">Aquí encontrarás un tutorial de cómo usar nuestro sistema</p>
        </div>
      </div>

      <!-- Videos Section Centered Horizontally and Vertically -->
<section class="flex-1 flex justify-center items-center px-1">
  <!-- Etiqueta con color del sidebar como borde directo del video -->
  <div class="bg-[#02162E] rounded-2xl shadow-2xl p-3 inline-block relative">
    <!-- Video de YouTube embebido -->
    <iframe
      ref="videoPlayer"
      class="w-[70vw] h-[70vh] rounded-xl shadow-2xl"
      :src="videos[0].url"
      title="Tutorial del Sistema"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowfullscreen>
    </iframe>
  </div>
</section>


      
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import AuthService from '@/services/auth.service';
// import tutorialVideo from '@/assets/tu-video-tutorial.mp4'; // Descomenta cuando tengas tu video

export default {
  name: 'DashboardView',
  components: {
    Sidebar
  },
  data() {
    return {
      username: localStorage.getItem("username_after_login") || "Usuario",
      displayName: "Usuario",
      videos: [
      {
        id: 1,
        titulo: "Tutorial del Sistema",
        url: "https://www.youtube.com/embed/CUNMaiAzRcw"
      },
    ]
    };
  },
  async mounted() {
    // Establecer el nombre para mostrar
    this.displayName = this.username;
  },
  methods: {
    async logout() {
      try {

        
        const result = await AuthService.logout();
        
        if (result.success) {
          console.log('Logout exitoso:', result.message);
        } else {
          console.log('Logout con advertencia:', result.message);
        }
        
        // Redirigir al login
        this.$router.push('/login');
        
      } catch (error) {
        console.error('Error en logout:', error);
        // Aunque falle, redirigir al login de todas formas
        this.$router.push('/login');
      }
    }
  }
};
</script>
