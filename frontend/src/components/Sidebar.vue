<template>
  <aside class="bg-[#02162E] text-white w-64 min-h-screen px-6 py-8 flex flex-col items-center gap-5">
    <!-- Logo -->
    <img
      src="@/assets/logo-horariux.png"
      alt="Logo HorariUX"
      class="w-200 h-auto mb-2"
    />

    <!-- Botones -->
    <router-link
      to="/dashboard"
      class="flex items-center justify-start text-left gap-2 bg-white text-[#0A1E40] hover:bg-gray-100 px-4 py-2 rounded-full font-jost shadow-sm transition w-full"
    >
      <i class="fas fa-chart-bar"></i> Inicio
    </router-link>

    <router-link
      to="/crear-horario"
      class="flex items-center justify-start text-left gap-2 bg-white text-[#0A1E40] hover:bg-gray-100 px-4 py-2 rounded-full font-jost shadow-sm transition w-full"
    >
      <i class="fas fa-calendar-plus"></i> Crear nuevo horario
    </router-link>

    <router-link
      to="/ver-horario"
      class="flex items-center justify-start text-left gap-2 bg-white text-[#0A1E40] hover:bg-gray-100 px-4 py-2 rounded-full font-jost shadow-sm transition w-full"
    >
      <i class="fas fa-folder-open"></i> Horario guardado
    </router-link>

    <router-link
      to="/disponibilidad"
      class="flex items-center justify-start text-left gap-2 bg-white text-[#0A1E40] hover:bg-gray-100 px-4 py-2 rounded-full font-jost shadow-sm transition w-full"
    >
      <i class="fas fa-clock"></i> Ver Disponibilidad
    </router-link>

    <router-link
      to="/exportar"
      class="flex items-center justify-start text-left gap-2 bg-white text-[#0A1E40] hover:bg-gray-100 px-4 py-2 rounded-full font-jost shadow-sm transition w-full"
    >
      <i class="fas fa-download"></i> Exportar Horario
    </router-link>

    <button
      @click="$emit('logout')"
      class="flex items-center justify-start text-left gap-2 bg-white hover:bg-gray-100 text-[#0A1E40] font-jost py-2 px-4 rounded-full w-full shadow transition"
    >
      <i class="fas fa-sign-out-alt"></i> Cerrar sesión
    </button>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
};
</script>
