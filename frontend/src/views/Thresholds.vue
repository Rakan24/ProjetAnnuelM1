<template>
  <div class="max-w-3xl mx-auto py-8">
    <button @click="goToDashboard" class="btn-dashboard mb-4">Retour au Dashboard</button>
    <h1 class="text-2xl font-bold mb-4">Gestion des seuils d'alerte</h1>
    <p class="text-gray-600 mb-6">Configurez les seuils pour PM2.5, PM10, O3 et NO2.</p>

    <div class="bg-white shadow rounded p-4">
      <form @submit.prevent="submitThresholds" class="space-y-4">
        <div v-for="(value, key) in thresholds" :key="key">
          <label :for="key" class="block font-medium text-gray-700 mb-1">
            {{ getLabel(key) }}
          </label>
          <input
            type="number"
            :id="key"
            v-model.number="thresholds[key]"
            class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            required
            min="0"
          />
        </div>

        <button
          type="submit"
          class="bg-blue-600 text-white rounded-md px-4 py-2 hover:bg-blue-700 transition-colors"
        >
          Enregistrer les seuils
        </button>
      </form>

      <!-- Message affiché si tous les seuils sont nuls ou 0 -->
      <p v-if="Object.values(thresholds).every(val => !val)" class="text-gray-600 mt-4 italic">
        Aucun seuil défini
      </p>

      <p v-if="successMessage" class="text-green-600 mt-4">{{ successMessage }}</p>
      <p v-if="errorMessage" class="text-red-600 mt-4">{{ errorMessage }}</p>
    </div>
  </div>
</template>


<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api.js'  // ajuste selon ton projet

const router = useRouter()

const thresholds = reactive({
  pm25: null,
  pm10: null,
  o3: null,
  no2: null
})

const successMessage = ref('')
const errorMessage = ref('')

const getLabel = (key) => {
  switch (key) {
    case 'pm25': return 'PM2.5 (µg/m³)'
    case 'pm10': return 'PM10 (µg/m³)'
    case 'o3': return 'O3 (µg/m³)'
    case 'no2': return 'NO2 (µg/m³)'
    default: return key
  }
}

const fetchThresholds = async () => {
  try {
    console.log('fetchThresholds called')
    const response = await api.get('/predictions/get-thresholds/')
    const data = response.data

    Object.keys(thresholds).forEach(key => {
      thresholds[key] = data[key] !== null ? data[key] : 0
    })

    errorMessage.value = ''
  } catch (err) {
    errorMessage.value = 'Impossible de charger les seuils actuels.'
    console.error(err)
  }
}

const submitThresholds = async () => {
  try {
    const response = await api.post('/predictions/save-thresholds/', thresholds)
    successMessage.value = 'Seuils enregistrés avec succès.'
    errorMessage.value = ''
  } catch (err) {
    successMessage.value = ''
    errorMessage.value = 'Erreur lors de l’enregistrement des seuils.'
    console.error(err)
  }
}

const goToDashboard = () => {
  router.push('/dashboard')
}

onMounted(() => {
  fetchThresholds()
})
</script>

<style scoped>
.btn-dashboard {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  margin-bottom: 1.5rem;
}
.btn-dashboard:hover {
  background-color: #2563eb;
}
</style>

