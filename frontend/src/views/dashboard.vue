<template>
  <div>
    <h1>Prévisions de pollution</h1>
    <div v-if="loading">Chargement...</div>
    <div v-else>
      <p>PM2.5 demain : {{ prediction.pm25_tomorrow }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const prediction = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await api.get('/predict/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    prediction.value = res.data
  } catch (err) {
    console.error('Erreur lors du chargement des prédictions', err)
  } finally {
    loading.value = false
  }
})
</script>
