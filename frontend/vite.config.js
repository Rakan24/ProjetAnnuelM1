import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // ← rend Vite accessible depuis l’extérieur du conteneur
    port: 3000,
    proxy: {
      '/api': 'http://backend:8000'
    }
  }
})
