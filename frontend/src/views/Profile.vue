<template>
  <div class="profile-container">
    <button @click="goToDashboard" class="btn-dashboard">Retour au Dashboard</button>
    <h1>Mon profil</h1>
    
    <div v-if="user">
      <p><strong>Email :</strong> {{ user.email }}</p>
      <p><strong>Statut :</strong> {{ user.is_staff ? 'Admin' : 'Utilisateur' }}</p>
    </div>

    <h2>Changer le mot de passe</h2>
    <form @submit.prevent="changePassword">
      <div class="form-group">
        <label for="old">Ancien mot de passe</label>
        <input type="password" v-model="oldPassword" required />
      </div>
      <div class="form-group">
        <label for="new">Nouveau mot de passe</label>
        <input type="password" v-model="newPassword" required />
      </div>
      <button type="submit" :disabled="loading">Changer</button>
      <p class="success" v-if="success">{{ success }}</p>
      <p class="error" v-if="error">{{ error }}</p>
    </form>

    <button @click="deleteProfile" class="btn-delete">Supprimer profil</button>
  </div>
</template>

<script>
import api from '../utils/api.js'

export default {
  data() {
    return {
      user: null,
      oldPassword: '',
      newPassword: '',
      loading: false,
      error: null,
      success: null,
    }
  },
  async created() {
    try {
      const res = await api.get('/auth/profile/')
      this.user = res.data
    } catch (err) {
      this.error = "Erreur lors du chargement du profil"
      console.error(err)
    }
  },
  methods: {
    async changePassword() {
      this.loading = true
      this.error = null
      this.success = null
      try {
        await api.post('/auth/change-password/', {
          old_password: this.oldPassword,
          new_password: this.newPassword,
        })
        this.success = "Mot de passe changé avec succès."
        this.oldPassword = ''
        this.newPassword = ''
      } catch (err) {
        this.error = err.response?.data?.error || "Erreur serveur"
      } finally {
        this.loading = false
      }
    },
    goToDashboard() {
      this.$router.push('/dashboard')
    },
    async deleteProfile() {
      if (confirm("Êtes-vous sûr de vouloir supprimer votre profil ? Cette action est irréversible.")) {
        try {
          await api.delete('/auth/delete-profile/')
          alert("Profil supprimé avec succès.")
          this.$router.push('/login')
        } catch (err) {
          this.error = err.response?.data?.error || "Erreur lors de la suppression du profil"
        }
      }
    },
  },
}
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 2rem auto;
  background: #f0f4f8;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
h1, h2 {
  margin-bottom: 1rem;
}
.form-group {
  margin-bottom: 1rem;
}
input {
  width: 100%;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 0.75rem;
  background-color: #10b981;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.success {
  color: green;
  margin-top: 1rem;
}
.error {
  color: red;
  margin-top: 1rem;
}
.btn-dashboard {
  margin-bottom: 1.5rem;
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.btn-dashboard:hover {
  background-color: #2563eb;
}
.btn-delete {
  margin-top: 2rem;
  padding: 0.75rem;
  background-color: #dc2626;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease;
}
.btn-delete:hover {
  background-color: #b91c1c;
}
</style>
