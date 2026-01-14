<template>
  <!-- Admin Layout (Login and Dashboard) -->
  <div v-if="$route.path.startsWith('/admin') && $route.path !== '/'" class="min-h-screen flex items-center justify-center bg-neutral-50 py-12 px-4 sm:px-6 lg:px-8">
    <router-view></router-view>
  </div>
  
  <!-- Main App Layout (User Views) -->
  <div v-else class="flex w-full h-screen bg-neutral-50">
    
    <!-- Sidebar -->
    <nav 
      class="w-64 bg-white border-r border-neutral-200 flex flex-col p-6 flex-shrink-0 h-screen transition-transform duration-300 ease-in-out fixed md:relative z-50"
      :class="{ '-translate-x-full md:translate-x-0': !isSidebarOpen, 'translate-x-0': isSidebarOpen }"
    >
      <!-- Brand -->
      <div class="flex items-center gap-3 mb-8 pb-4 border-b border-neutral-100">
        <img src="./assets/Avana-logo-black.png" alt="Avana Logo" class="w-8 h-auto object-contain" />
        <div class="flex flex-col leading-tight">
          <span class="font-bold text-base text-neutral-800">Avana Group</span>
          <span class="text-xs text-neutral-500 uppercase tracking-wide">Intranet Portal</span>
        </div>
      </div>
      
      <!-- Navigation Links -->
      <div class="flex flex-col gap-2 flex-1">
        <router-link 
          to="/" 
          @click="isSidebarOpen = false"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-neutral-600 hover:bg-neutral-50 hover:text-primary-700 hover:translate-x-0.5 transition-all duration-200"
          active-class="!bg-primary-700 !text-white shadow-md"
        >
          <span class="text-lg w-6 text-center">📊</span>
          <span>Dashboard</span>
        </router-link>
        
        <router-link 
          to="/intercom" 
          @click="isSidebarOpen = false"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-neutral-600 hover:bg-neutral-50 hover:text-primary-700 hover:translate-x-0.5 transition-all duration-200"
          active-class="!bg-primary-700 !text-white shadow-md"
        >
          <span class="text-lg w-6 text-center">👥</span>
          <span>Intercom Directory</span>
        </router-link>
        
        <router-link 
          to="/events" 
          @click="isSidebarOpen = false"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-neutral-600 hover:bg-neutral-50 hover:text-primary-700 hover:translate-x-0.5 transition-all duration-200"
          active-class="!bg-primary-700 !text-white shadow-md"
        >
          <span class="text-lg w-6 text-center">🎉</span>
          <span>Events</span>
        </router-link>
        
        <router-link 
          to="/bookings" 
          @click="isSidebarOpen = false"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-neutral-600 hover:bg-neutral-50 hover:text-primary-700 hover:translate-x-0.5 transition-all duration-200"
          active-class="!bg-primary-700 !text-white shadow-md"
        >
          <span class="text-lg w-6 text-center">📅</span>
          <span>Bookings</span>
        </router-link>
      </div>

      <!-- Admin Link -->
      <div class="mt-auto pt-4 border-t border-neutral-100">
        <router-link 
          to="/admin" 
          @click="isSidebarOpen = false"
          class="flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium text-sm text-neutral-600 hover:bg-neutral-50 hover:text-primary-700 hover:translate-x-0.5 transition-all duration-200 admin-link"
          active-class="!bg-primary-700 !text-white shadow-md"
        >
          <span class="text-lg w-6 text-center">⚙️</span>
          <span>Admin</span>
        </router-link>
      </div>
    </nav>
    
    <!-- Mobile Overlay -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-neutral-900/50 z-40 md:hidden"
    ></div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      <!-- Top Bar -->
      <header class="h-16 bg-white border-b border-neutral-200 flex items-center justify-between px-4 md:px-8 flex-shrink-0">
        <div class="flex items-center gap-4">
          <button 
            @click="isSidebarOpen = !isSidebarOpen"
            class="md:hidden text-neutral-700 hover:text-neutral-900 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg p-2 -ml-2"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          <h2 class="text-xl font-semibold text-neutral-800">{{ currentRouteName }}</h2>
        </div>
        
        <div class="flex items-center gap-4">
          <div class="w-9 h-9 rounded-full bg-neutral-100 border border-neutral-200 flex items-center justify-center text-neutral-500">
            👤
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-8 bg-neutral-50">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const isSidebarOpen = ref(false)
const route = useRoute()

const currentRouteName = computed(() => {
  if (route.path === '/') return 'Dashboard'
  if (route.path === '/intercom') return 'Intercom Directory'
  if (route.path === '/events') return 'Events & Parties'
  if (route.path === '/bookings') return 'Hall Bookings'
  if (route.path.includes('admin')) return 'Admin Area'
  return ''
})
</script>
