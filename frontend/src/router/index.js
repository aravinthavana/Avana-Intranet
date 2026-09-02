import { createRouter, createWebHashHistory } from 'vue-router'
import Intercom from '../views/Intercom.vue'
import AdminLogin from '../views/AdminLogin.vue'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/intercom', component: Intercom },
  { path: '/admin', component: AdminLogin }
]

const router = createRouter({
  history: createWebHashHistory(), // Hash history for simpler file-based routing
  routes
})

router.beforeEach((to, from, next) => {
  // Use dynamic import or grab store at execution time to avoid Pinia init issues
  import('../stores/data').then(({ useDataStore }) => {
    const store = useDataStore()
    const isAuthenticated = store.isAuthenticated()
    
    if (to.meta?.requiresAuth && !isAuthenticated) {
      next('/admin')
    } else {
      next()
    }
  })
})

export default router
