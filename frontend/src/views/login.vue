<template>
  <div class="login-container">
    <h1>Connexion à BreathWell</h1>

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          type="email"
          v-model="email"
          placeholder="email@example.com"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Mot de passe</label>
        <input
          id="password"
          type="password"
          v-model="password"
          placeholder="********"
          required
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Connexion...' : 'Se connecter' }}
      </button>

      <p class="error" v-if="error">{{ error }}</p>
    </form>

    <!-- Nouveau bouton pour aller à l'inscription -->
    <button class="register-btn" @click="goToRegister" :disabled="loading">
      Pas encore de compte ? Inscrivez-vous
    </button>

    <!-- Nouveau bouton pour réinitialiser le mot de passe -->
    <button class="reset-btn" @click="goToResetPassword" :disabled="loading">
      Mot de passe oublié ?
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
      loading: false,
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      this.loading = true
      try {
        const response = await api.post('/auth/login/', {
          email: this.email,
          password: this.password,
        })

        const token = response.data.token
        const isStaff = response.data.is_staff

        localStorage.setItem('token', token)
        localStorage.setItem('is_staff', isStaff)

        this.$router.push('/dashboard')

      } catch (err) {
        this.error = 'Identifiants incorrects ou erreur serveur.'
      } finally {
        this.loading = false
      }
    },
    goToRegister() {
      this.$router.push('/register')
    },
    goToResetPassword() {
      this.$router.push('/forgot-password')
    }
  },
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

.reset-btn {
  margin-top: 0.5rem;
  background-color: transparent;
  color: #3b82f6;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  font-weight: 600;
  font-size: 1rem;
}

.reset-btn:disabled {
  color: #93c5fd;
  cursor: not-allowed;
}
</style>
