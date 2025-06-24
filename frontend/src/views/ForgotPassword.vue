<template>
  <div class="wrapper">
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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../utils/api.js' // adapte ce chemin selon ton projet

const email = ref('')
const error = ref(null)
const success = ref(null)
const loading = ref(false)

async function handleSubmit() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    // Correction ici : l'URL doit avoir un tiret et slash final
    await api.post('/auth/forgot-password/', { email: email.value })
    success.value = "Un email de réinitialisation a été envoyé si l'adresse existe."
  } catch (err) {
    // Lecture du message d'erreur serveur si dispo
    error.value = err.response?.data?.error || 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.login-container {
  max-width: 400px;
  width: 100%;
  padding: 2rem;
  border-radius: 12px;
  background: white;
  box-shadow: 0 0 12px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
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
</style>
