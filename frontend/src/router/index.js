import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Intercom from '../views/Intercom.vue'
import Events from '../views/Events.vue'
import Bookings from '../views/Bookings.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/intercom', component: Intercom },
  { path: '/events', component: Events },
  { path: '/bookings', component: Bookings },
  { path: '/admin', component: AdminLogin },
  { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHashHistory(), // Hash history for simpler file-based routing
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('admin_token')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/admin')
  } else {
    next()
  }
})

export default router
