<template>
  <div class="max-w-5xl mx-auto">
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-extrabold text-neutral-900 mb-4 tracking-tight">Welcome to Avana Group Intranet</h1>
      <p class="text-xl text-neutral-500 max-w-2xl mx-auto">
        Your central hub for office resources, directories, and internal applications.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Intercom Directory Card -->
      <router-link 
        to="/intercom" 
        class="group bg-white rounded-2xl shadow-sm border border-neutral-200 p-8 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex flex-col items-center text-center"
      >
        <div class="w-16 h-16 rounded-2xl bg-primary-50 text-primary-600 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <Icon name="phone" size="xl" />
        </div>
        <h3 class="text-xl font-bold text-neutral-900 mb-3 group-hover:text-primary-700 transition-colors">Intercom Directory</h3>
        <p class="text-neutral-500 mb-6">Access internal phone extensions and contact information.</p>
        <span class="text-primary-600 font-medium flex items-center gap-2 group-hover:gap-3 transition-all">
          View Directory <Icon name="arrow-right" size="sm" />
        </span>
      </router-link>

      <!-- Coming Soon Card (Placeholder) -->
      <div class="bg-neutral-50 rounded-2xl border border-neutral-200 p-8 flex flex-col items-center text-center opacity-75">
        <div class="w-16 h-16 rounded-2xl bg-neutral-100 text-neutral-400 flex items-center justify-center mb-6">
          <Icon name="clock" size="xl" />
        </div>
        <h3 class="text-xl font-bold text-neutral-700 mb-3">More Features Coming Soon</h3>
        <p class="text-neutral-500">We are adding more tools and resources to the intranet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from '../components/ui/Icon.vue'
</script>
