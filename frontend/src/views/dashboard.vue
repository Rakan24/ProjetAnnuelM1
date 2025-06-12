<template>
  <div class="dashboard-container">
    <!-- SIDEBAR -->
    <aside class="sidebar">
      <h2>Menu</h2>
      <ul>
        <li><button @click="goToProfile">Mon Profil</button></li>
        <li><button @click="goToDashboard">Dashboard</button></li>
        <li><button @click="logout">Se déconnecter</button></li>
      </ul>
    </aside>

    <!-- CONTENU PRINCIPAL -->
    <main class="main-content py-6">
      <div class="flex flex-col items-start md:flex-row md:items-center md:justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Tableau de bord qualité de l'air</h1>
          <p class="text-gray-600">{{ todayDate }}</p>
        </div>
      </div>

      <div v-if="loading" class="text-center py-8">
        <p>Chargement des données...</p>
      </div>
      <div v-else-if="error" class="text-center text-red-600 py-8">
        <p>{{ error }}</p>
        <button @click="fetchForecast" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Réessayer
        </button>
      </div>
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div :class="['p-6 rounded-lg text-white', getStatusColor(today.status)]">
            <h2 class="text-xl font-semibold mb-2">Qualité de l'air aujourd'hui</h2>
            <p class="text-4xl font-bold">{{ today.aqi }}</p>
            <p class="capitalize mt-1 text-lg">{{ today.status }}</p>
            <p class="text-white/90 mt-2">{{ getStatusMessage(today.status) }}</p>
          </div>

          <div class="col-span-1 md:col-span-2 bg-white p-6 rounded-lg shadow">
            <h2 class="text-lg font-semibold mb-4">Polluants critiques</h2>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div v-for="pollutant in today.pollutants" :key="pollutant.id"
                :class="['p-3 rounded-lg', getPollutantCardColor(pollutant.status)]">
                <p class="text-sm font-medium">{{ pollutant.name }}</p>
                <p class="text-2xl font-bold mt-1">
                  {{ pollutant.value }} <span class="text-sm font-normal">{{ pollutant.unit }}</span>
                </p>
                <p class="text-xs mt-1 capitalize">{{ pollutant.status }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div class="col-span-1 lg:col-span-2 bg-white p-6 rounded-lg shadow">
            <h2 class="text-lg font-semibold mb-2">Prévisions 7 jours</h2>
            <div class="h-64">
              <!-- Graphique ici -->
              <p class="text-center text-gray-500">(Graphique à implémenter)</p>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-lg font-semibold mb-2">Recommandations santé</h2>
            <ul class="space-y-2">
              <li v-for="(rec, i) in getHealthRecommendations(today.status)" :key="i"
                class="flex items-start">
                <div class="mt-1 h-2 w-2 rounded-full" :class="getStatusDotColor(today.status)" />
                <p class="ml-3 text-sm text-gray-600">{{ rec }}</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'

const router = useRouter()

const loading = ref(true)
const error = ref(null)
const forecasts = ref([])
const today = computed(() => forecasts.value[0] || {})
const todayDate = new Date().toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })

const fetchForecast = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('token')
    const res = await api.get('/predict/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    forecasts.value = res.data
  } catch (err) {
    error.value = 'Erreur de chargement des données.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchForecast)

const getStatusColor = (status) => {
  switch (status) {
    case 'good': return 'bg-gradient-to-br from-green-500 to-green-600'
    case 'moderate': return 'bg-gradient-to-br from-yellow-400 to-yellow-500'
    case 'unhealthy': return 'bg-gradient-to-br from-orange-500 to-orange-600'
    case 'hazardous': return 'bg-gradient-to-br from-red-500 to-red-600'
    default: return 'bg-gradient-to-br from-blue-500 to-blue-600'
  }
}

const getPollutantCardColor = (status) => {
  switch (status) {
    case 'good': return 'bg-green-50 text-green-700'
    case 'moderate': return 'bg-yellow-50 text-yellow-700'
    case 'unhealthy': return 'bg-orange-50 text-orange-700'
    case 'hazardous': return 'bg-red-50 text-red-700'
    default: return 'bg-gray-50 text-gray-700'
  }
}

const getStatusDotColor = (status) => {
  switch (status) {
    case 'good': return 'bg-green-500'
    case 'moderate': return 'bg-yellow-500'
    case 'unhealthy': return 'bg-orange-500'
    case 'hazardous': return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

const getStatusMessage = (status) => {
  switch (status) {
    case 'good': return 'Respirez librement!'
    case 'moderate': return 'Qualité acceptable'
    case 'unhealthy': return 'Peut causer de l"inconfort'
    case 'hazardous': return 'Alerte sanitaire!'
    default: return ''
  }
}

const getHealthRecommendations = (status) => {
  switch (status) {
    case 'good': return [
      'La qualité de l"air est satisfaisante.',
      'Profitez des activités extérieures.',
      'Gardez les fenêtres ouvertes.',
      'Bon moment pour faire du sport.'
    ]
    case 'moderate': return [
      'Qualité de l"air acceptable pour la majorité.',
      'Les personnes sensibles doivent faire attention.',
      'Fermez les fenêtres aux heures de pointe.',
      'Surveillez les symptômes respiratoires.'
    ]
    case 'unhealthy': return [
      'Effets possibles pour tout le monde.',
      'Réduisez les activités extérieures.',
      'Restez à l"intérieur et utilisez des purificateurs.',
      'Les personnes sensibles doivent éviter les sorties.'
    ]
    case 'hazardous': return [
      'Conditions dangereuses pour la santé.',
      'Évitez toute activité extérieure.',
      'Restez à l"intérieur et fermez bien les fenêtres.',
      'Utilisez un purificateur d"air si possible.'
    ]
    default: return ['Consultez les rapports locaux de qualité de l"air.']
  }
}

// Navigation sidebar
const goToProfile = () => {
  router.push('/profile') // à adapter selon ta route
}
const goToDashboard = () => {
  router.push('/dashboard')
}
const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* SIDEBAR */
.sidebar {
  width: 220px;
  background-color: #3b82f6;
  color: white;
  padding: 2rem 1rem;
  border-right: 1px solid #e5e7eb;
}

.sidebar h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 1rem;
}

.sidebar button {
  background: none;
  border: none;
  color: white;
  font-size: 1rem;
  width: 100%;
  text-align: left;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: background-color 0.2s;
  cursor: pointer;
}

.sidebar button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* MAIN CONTENT */
.main-content {
  flex: 1;
  padding: 2rem;
}
</style>
