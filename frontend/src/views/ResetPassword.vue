<template>
  <div class="wrapper">
    <div class="login-container">
      <h2>Réinitialisation du mot de passe</h2>

      <p v-if="loading">Vérification du token...</p>
      <p class="error-message" v-if="error">{{ error }}</p>
      <p class="success-message" v-if="success">{{ success }}</p>

      <form v-if="!loading && !error" @submit.prevent="handleReset">
        <div class="form-group">
          <label for="password">Nouveau mot de passe</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
        <button type="submit" class="btn">Réinitialiser</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../utils/api.js'  // ajuste selon ton projet

export default {
  data() {
    return {
      token: null,
      password: '',
      error: null,
      success: null,
      loading: true,
    };
  },
  async mounted() {
    this.token = this.$route.params.token;
    try {
      await api.get(`/auth/check-reset-token/${this.token}/`);
      this.loading = false;  // token valide, on affiche le formulaire
    } catch (err) {
      this.error = err.response?.data?.error || "Token invalide ou expiré.";
      this.loading = false;
    }
  },
  methods: {
    async handleReset() {
      this.error = null;
      this.success = null;
      if (!this.password || this.password.length < 4) {
        this.error = "Le mot de passe est trop court (minimum 4 caractères)";
        return;
      }

      try {
        await api.post(`/auth/reset-password/${this.token}/`, {
          new_password: this.password
        });
        this.success = "Mot de passe réinitialisé avec succès. Vous allez être redirigé vers la page de connexion...";
        this.password = '';

        // Redirection vers la page login après 2 secondes
        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);

      } catch (err) {
        this.error = err.response?.data?.error || "Une erreur est survenue.";
      }
    }
  }
};
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-container {
  max-width: 400px;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: bold;
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
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-bottom: 1rem;
}

.success-message {
  color: green;
  margin-bottom: 1rem;
}
</style>
