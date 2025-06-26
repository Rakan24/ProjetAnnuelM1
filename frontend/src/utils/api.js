import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

// Intercepteur pour ajouter le bon Authorization selon la route
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  // Liste des routes publiques qui n'ont PAS besoin du token
  const publicPaths = [
    '/auth/login/',
    '/auth/register/',
    '/auth/forgot-password/',
    '/auth/reset-password/',
    '/auth/check-reset-token/' // <-- Ajout ici
  ]

  // Vérifie si la requête est pour une route publique
  const isPublicPath = publicPaths.some(path => config.url.includes(path))

  console.log(`\n[API] Request to: ${config.url}`)
  console.log(`[API] Token in localStorage: ${token ? 'FOUND' : 'NOT FOUND'}`)
  console.log(`[API] Is public path: ${isPublicPath}`)

  if (token && !isPublicPath) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('[API] Authorization header added')
  } else {
    console.log('[API] Authorization header NOT added')
  }

  return config
}, error => {
  console.error('[API] Request error:', error)
  return Promise.reject(error)
})

export default api
