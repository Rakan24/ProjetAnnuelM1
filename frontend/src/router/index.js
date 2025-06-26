import { createRouter, createWebHistory } from 'vue-router'
import jwt_decode from 'jwt-decode'

import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Register from '../views/Register.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import Profile from '../views/Profile.vue'
import NotFoundPage from '../views/NotFoundPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/register', component: Register },
  { path: '/forgot-password', component: ForgotPassword },
  { path: '/reset-password/:token', component: ResetPassword },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { 
    path: '/thresholds', 
    name: 'Thresholds', 
    component: () => import('../views/Thresholds.vue'), 
    meta: { requiresAuth: true, requiresAdmin: true } 
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth) {
    if (!token) {
      console.warn('🔒 Aucun token trouvé → redirection login')
      return next('/login')
    }

    let decoded
    try {
      decoded = jwt_decode(token)
      console.log('🔑 Token décodé :', decoded)
      //console.log('📝 is_admin:', decoded.is_admin)
      console.log('📝 is_staff:', decoded.is_staff)
      //console.log('📝 role:', decoded.role)
    } catch (e) {
      console.error('❌ Token invalide :', e)
      return next('/login')
    }

      if (to.meta.requiresAdmin) {
        const isAdmin = decoded.is_staff;
        console.log('👑 isAdmin calculé :', isAdmin);
        if (!isAdmin) {
          console.warn('⛔ Accès admin refusé → redirection dashboard');
          return next('/dashboard');
        }
      }
  }

  next()
})

export default router
