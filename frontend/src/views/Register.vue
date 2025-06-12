<template>
  <div class="register-container">
    <h1>Créer un compte BreathWell</h1>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" type="email" v-model="email" required />
      </div>

      <div class="form-group">
        <label for="password">Mot de passe</label>
        <input id="password" type="password" v-model="password" required />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Création...' : 'S’inscrire' }}
      </button>

      <p class="error" v-if="error">{{ error }}</p>
      <p class="success" v-if="success">{{ success }}</p>
    </form>

    <!-- Bouton pour revenir à la connexion -->
    <button class="login-btn" @click="goToLogin" :disabled="loading">
      Déjà inscrit ? Connectez-vous
    </button>
  </div>
</template>

<script>
import api from '../utils/api.js'

export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
      success: null,
      loading: false,
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      this.success = null
      this.loading = true
      try {
        const response = await api.post('/auth/register/', {
          email: this.email,
          password: this.password,
        })
        this.success = response.data.message
        // Tu peux rediriger après inscription si tu préfères
        // this.$router.push('/login')
      } catch (err) {
        this.error = err.response?.data?.error || 'Erreur serveur'
      } finally {
        this.loading = false
      }
    },
    goToLogin() {
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h1 {
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

button {
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

button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.error {
  margin-top: 1rem;
  color: red;
  text-align: center;
}

.success {
  margin-top: 1rem;
  color: green;
  text-align: center;
  font-weight: 600;
}

/* Style du bouton pour revenir à la connexion */
.login-btn {
  margin-top: 1rem;
  background-color: transparent;
  color: #3b82f6;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  font-weight: 600;
  font-size: 1rem;
}

.login-btn:disabled {
  color: #93c5fd;
  cursor: not-allowed;
}
</style>
