<template>
  <div class="login-container">
    <h2>Mot de passe oublié</h2>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="success" class="success-message">{{ success }}</div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Adresse e-mail</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
        />
      </div>
      <button type="submit" class="btn" :disabled="loading">
        {{ loading ? 'Envoi en cours...' : 'Envoyer le lien' }}
      </button>
    </form>


    <button class="back-login-btn" @click="goToLogin" :disabled="loading">
      Je me rappelle de mon mot de passe
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'

const email = ref('')
const error = ref(null)
const success = ref(null)
const loading = ref(false)
const router = useRouter()

async function handleSubmit() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    await api.post('/auth/forgot-password/', { email: email.value })
    success.value = "Un email de réinitialisation a été envoyé si l'adresse existe."
  } catch (err) {
    error.value = err.response?.data?.error || 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push('/login')
}
function goToRegister() {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #3b82f6;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
  text-align: center;
}

.success-message {
  color: green;
  margin-bottom: 1rem;
  text-align: center;
}

.register-btn {
  margin-top: 1rem;
  background-color: transparent;
  color: #3b82f6;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  font-weight: 600;
  font-size: 1rem;
}

.register-btn:disabled {
  color: #93c5fd;
  cursor: not-allowed;
}

.back-login-btn {
  margin-top: 0.5rem;
  background-color: transparent;
  color: #3b82f6;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  font-weight: 600;
  font-size: 1rem;
  width: 100%;
}
.back-login-btn:disabled {
  color: #93c5fd;
  cursor: not-allowed;
}
</style>
