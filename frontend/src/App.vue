<template>
  <div v-if="$route.path.startsWith('/admin') && $route.path !== '/'" class="admin-layout">
    <router-view></router-view>
  </div>
  <div v-else id="app-layout">
    
    <!-- Sidebar -->
    <nav class="sidebar" :class="{ open: isSidebarOpen }">
      <div class="brand">
        <img src="./assets/Avana-logo-black.png" alt="Avana Logo" class="logo" />
        <div class="brand-text">
          <span class="company">Avana Group</span>
          <span class="tagline">Intranet Portal</span>
        </div>
      </div>
      
      <div class="nav-links">
        <router-link to="/" @click="isSidebarOpen = false">
          <span class="icon">📊</span> Dashboard
        </router-link>
        <router-link to="/intercom" @click="isSidebarOpen = false">
          <span class="icon">👥</span> Intercom Directory
        </router-link>
        <router-link to="/events" @click="isSidebarOpen = false">
          <span class="icon">🎉</span> Events
        </router-link>
        <router-link to="/bookings" @click="isSidebarOpen = false">
          <span class="icon">📅</span> Bookings
        </router-link>
      </div>

      <div class="nav-footer">
        <router-link to="/admin" @click="isSidebarOpen = false" class="admin-link">
          <span class="icon">⚙️</span> Admin
        </router-link>
      </div>
    </nav>
    
    <!-- Mobile Overlay -->
    <div class="sidebar-overlay" v-if="isSidebarOpen" @click="isSidebarOpen = false"></div>

    <!-- Main Content Area -->
    <div class="content-wrapper">
      <header class="top-bar">
        <button class="mobile-toggle" @click="isSidebarOpen = !isSidebarOpen">☰</button>
        <h2 class="page-title">{{ currentRouteName }}</h2>
        <div class="user-profile">
          <div class="avatar">👤</div>
        </div>
      </header>

      <main class="main-content">
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

<style scoped>
#app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  background-color: #f1f5f9; /* Slate 100 */
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  flex-shrink: 0;
  height: 100vh;
  box-sizing: border-box;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.logo {
  width: 32px;
  height: auto;
  object-fit: contain;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.company {
  font-weight: 700;
  font-size: 1rem;
  color: #1e293b; /* Slate 800 */
}

.tagline {
  font-size: 0.75rem;
  color: #64748b; /* Slate 500 */
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

/* Navigation Links */
.sidebar a {
  text-decoration: none;
  color: #475569; /* Slate 600 - Enforce contrast */
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.sidebar a .icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.sidebar a:hover {
  background-color: #f8fafc;
  color: #0f766e; /* Teal 700 */
  transform: translateX(2px);
}

.sidebar a.router-link-active {
  background-color: #0f766e; /* Teal 700 */
  color: white !important; /* Force white text on active */
  box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.2);
}

.nav-footer {
  margin-top: auto;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}

/* Wrapper and Header */
.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.top-bar {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  flex-shrink: 0;
}

.page-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.user-profile .avatar {
  background: #f1f5f9;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background-color: #f8fafc;
}

/* Mobile Toggle */
.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #334155;
  margin-right: 1rem;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 50;
    transform: translateX(-100%);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 40;
  }
  .mobile-toggle { display: block; }
  .top-bar { padding: 0 1rem; }
  .main-content { padding: 1rem; }
}

.admin-layout {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background: #f1f5f9;
  padding: 4rem 1rem;
  overflow-y: auto;
  box-sizing: border-box;
}
</style>
