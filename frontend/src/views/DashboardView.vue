
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
  <div class="bg-[#02162E] rounded-2xl shadow-2xl p-3 inline-block relative"
      @mouseenter="showControls = true"
      @mouseleave="hideControlsDelayed">
    <!-- Video sin controles -->
    <video
      ref="videoPlayer"
      class="w-[70vw] h-[70vh] rounded-xl shadow-2xl object-cover cursor-pointer"
      @click="togglePlay"
      @ended="onVideoEnded"
      @pause="onVideoPaused"
      @timeupdate="updateProgress"
      @loadedmetadata="onVideoLoaded"
    >
      <source :src="videos[0].url" type="video/mp4" />
      Tu navegador no soporta el video.
    </video>

    <!-- Controles personalizados del video -->
    <div class="absolute bottom-4 left-4 right-4 bg-black bg-opacity-80 rounded-lg p-4 transition-opacity duration-300"
        :class="showControls ? 'opacity-100' : 'opacity-0'"
        @mouseenter="showControls = true"
        @mouseleave="showControls = false">
      
      <!-- Barra de progreso -->
      <div class="mb-3">
        <div class="bg-gray-600 rounded-full h-2 cursor-pointer" @click="seekVideo">
          <div class="bg-[#02162E] h-2 rounded-full transition-all duration-200" 
              :style="`width: ${progress}%`"></div>
        </div>
        <div class="flex justify-between text-white text-sm mt-1">
          <span>{{ formatTime(currentTime) }}</span>
          <span>{{ formatTime(duration) }}</span>
        </div>
      </div>
    </div>

    <!-- Botón de play personalizado en el centro del video -->
    <div 
      v-if="showPlayButton" 
      @click="togglePlay"
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
            bg-[#02162E] 
            hover:bg-[#0A1E40] 
            active:bg-[#001428]
            rounded-full p-8 cursor-pointer 
            transition-all duration-300 ease-in-out
            hover:scale-110 active:scale-95
            shadow-2xl hover:shadow-[#02162E]/50
            ring-4 ring-white/30 hover:ring-white/50
            backdrop-blur-sm
            group z-10"
    >
      <i class="fas fa-play text-white text-6xl ml-2 
              group-hover:text-blue-100 
              transition-colors duration-300 
              drop-shadow-lg"></i>
    </div>
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
      showPlayButton: true,
      showControls: false,
      videoPlaying: false,
      currentTime: 0,
      duration: 0,
      progress: 0,
      volume: 100,
      videos: [
      {
        id: 1,
        titulo: "Bienvenida general",
        url: "" // Cambiar por: tutorialVideo cuando tengas tu video
      },
    ]
    };
  },
  async mounted() {
    // Establecer el nombre para mostrar
    this.displayName = this.username;
  },
  methods: {
    togglePlay() {
      const video = this.$refs.videoPlayer;
      if (video.paused) {
        video.play();
        this.showPlayButton = false;
        this.videoPlaying = true;
        this.showControls = true;
      } else {
        video.pause();
        this.showPlayButton = true;
        this.videoPlaying = false;
      }
    },
    onVideoEnded() {
      this.showPlayButton = true;
      this.videoPlaying = false;
    },
    onVideoPaused() {
      this.showPlayButton = true;
      this.videoPlaying = false;
    },
    onVideoLoaded() {
      const video = this.$refs.videoPlayer;
      this.duration = video.duration;
    },
    updateProgress() {
      const video = this.$refs.videoPlayer;
      this.currentTime = video.currentTime;
      this.progress = (video.currentTime / video.duration) * 100;
    },
    skipVideo(seconds) {
      const video = this.$refs.videoPlayer;
      video.currentTime += seconds;
    },
    seekVideo(event) {
      const video = this.$refs.videoPlayer;
      const progressBar = event.currentTarget;
      const clickPosition = event.offsetX / progressBar.offsetWidth;
      video.currentTime = clickPosition * video.duration;
    },
    changeVolume(event) {
      const video = this.$refs.videoPlayer;
      this.volume = event.target.value;
      video.volume = this.volume / 100;
    },
    formatTime(time) {
      if (!time) return '0:00';
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },
    hideControlsDelayed() {
      setTimeout(() => {
        if (!this.videoPlaying) return;
        this.showControls = false;
      }, 2000);
    },
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
