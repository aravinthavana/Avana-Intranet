import { createRouter, createWebHashHistory } from 'vue-router'
import Intercom from '../views/Intercom.vue'
import AdminLogin from '../views/AdminLogin.vue'
const routes = [
  { path: '/', component: Intercom },
  { path: '/admin', component: AdminLogin }
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
