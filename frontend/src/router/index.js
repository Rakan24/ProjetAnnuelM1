import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Register from '../views/Register.vue'  // <-- Import de la page Register
import Profile from '../views/Profile.vue'  // <-- Import de la page Profile

const routes = [
  { path: '/', redirect: '/login' }, // 👈 redirection automatique
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard pour protéger les routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/') // redirige vers login si non connecté
  } else {
    next()
  }
})

export default router
