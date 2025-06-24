<template>
  <!-- SIDEBAR -->
  <nav class="w-full bg-gray-800 text-white sticky top-0 z-50">
    <div class="flex items-center justify-between max-w-7xl mx-auto px-4 py-2">
      <h2 class="font-bold text-lg">Menu</h2>
      <ul class="flex space-x-4">
        <li>
          <button @click="goToProfile" class="hover:bg-gray-700 rounded px-3 py-1">Mon Profil</button>
        </li>
        <li>
          <button @click="goToDashboard" class="hover:bg-gray-700 rounded px-3 py-1">Dashboard</button>
        </li>
        <li>
          <button @click="logout" class="hover:bg-gray-700 rounded px-3 py-1">Se déconnecter</button>
        </li>
      </ul>
    </div>
  </nav>


  <div class="py-6">
    <div class="flex flex-col items-start md:flex-row md:items-center md:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Air Quality Dashboard</h1>
        <p class="text-gray-600">
          {{ format(new Date(), 'EEEE, MMMM d, yyyy') }}
        </p>
      </div>
    </div>

    <LoadingScreen v-if="store.isLoading" />

    <div v-else-if="store.error" class="flex items-center justify-center h-64">
      <div class="text-center">
        <p class="text-red-500 text-lg">{{ store.error }}</p>
        <button
          @click="store.fetchForecast"
          class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    </div>

    <div v-else-if="!today" class="flex items-center justify-center h-64">
      <p class="text-gray-500 text-lg">No forecast data available</p>
    </div>

    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card :class="`bg-gradient-to-br ${getStatusColor(today.status)}`">
          <CardHeader>
            <CardTitle class="text-white">Today's Air Quality</CardTitle>
            <CardDescription class="text-white/80">
              Overall air quality status
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div class="flex items-end justify-between">
              <div>
                <p class="text-4xl font-bold text-white">{{ today.aqi }}</p>
                <p class="text-white/90 mt-1 text-lg capitalize">{{ today.status }}</p>
              </div>
              <div class="text-right">
                <p class="text-white/90">
                  {{ getStatusMessage(today.status) }}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle>Critical Pollutants</CardTitle>
            <CardDescription>
              Today's key pollutant levels
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div 
                v-for="pollutant in today.pollutants" 
                :key="pollutant.id"
                :class="`p-3 rounded-lg ${getPollutantCardColor(pollutant.status)}`"
              >
                <p class="text-sm font-medium">{{ pollutant.name }}</p>
                <p class="text-2xl font-bold mt-1">
                  {{ pollutant.value }}
                  <span class="text-sm font-normal ml-1">{{ pollutant.unit }}</span>
                </p>
                <p class="text-xs mt-1 capitalize">{{ pollutant.status }}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card class="col-span-1 lg:col-span-2">
          <CardHeader>
            <CardTitle>7-Day Air Quality Forecast</CardTitle>
            <CardDescription>
              Pollution levels for the upcoming week
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div class="h-80 w-full">
              <AirQualityChart :forecasts="store.forecasts" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Health Recommendations</CardTitle>
            <CardDescription>
              Based on current air quality
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div 
                v-for="(rec, index) in getHealthRecommendations(today.status)" 
                :key="index" 
                class="flex items-start"
              >
                <div :class="`mt-1 h-2 w-2 rounded-full ${getStatusDotColor(today.status)}`" />
                <p class="ml-3 text-sm text-gray-600">{{ rec }}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div class="mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Detailed Forecast</CardTitle>
            <CardDescription>
              Day-by-day air quality forecast
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ForecastCards :forecasts="store.forecasts" />
          </CardContent>
        </Card>
      </div>

      <div>
        <Card>
          <CardHeader>
            <CardTitle>Pollutant Details</CardTitle>
            <CardDescription>
              Detailed information about each pollutant
            </CardDescription>
          </CardHeader>
          <CardContent>
            <PollutantTable :forecasts="store.forecasts" />
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { format } from 'date-fns';
import { useAirQualityStore } from '../stores/airQualityStore';
import Card from '../components/ui/Card.vue';
import CardHeader from '../components/ui/CardHeader.vue';
import CardTitle from '../components/ui/CardTitle.vue';
import CardDescription from '../components/ui/CardDescription.vue';
import CardContent from '../components/ui/CardContent.vue';
import AirQualityChart from '../components/dashboard/AirQualityChart.vue';
import ForecastCards from '../components/dashboard/ForecastCards.vue';
import PollutantTable from '../components/dashboard/PollutantTable.vue';
import LoadingScreen from '../components/ui/LoadingScreen.vue';


import { useRouter } from 'vue-router'
//import api from '../utils/api.js'

const router = useRouter()


const store = useAirQualityStore();

const today = computed(() => {
  if (!Array.isArray(store.forecasts) || store.forecasts.length === 0) return null;
  return store.forecasts[0];
});

// Chargement initial des données
onMounted(async () => {
  await store.fetchForecast();
});

const getStatusColor = (status) => {
  switch (status) {
    case 'good': return 'from-green-500 to-green-600';
    case 'moderate': return 'from-yellow-400 to-yellow-500';
    case 'unhealthy': return 'from-orange-500 to-orange-600';
    case 'hazardous': return 'from-red-500 to-red-600';
    default: return 'from-blue-500 to-blue-600';
  }
};

const getPollutantCardColor = (status) => {
  switch (status) {
    case 'good': return 'bg-green-50 text-green-700';
    case 'moderate': return 'bg-yellow-50 text-yellow-700';
    case 'unhealthy': return 'bg-orange-50 text-orange-700';
    case 'hazardous': return 'bg-red-50 text-red-700';
    default: return 'bg-gray-50 text-gray-700';
  }
};

const getStatusDotColor = (status) => {
  switch (status) {
    case 'good': return 'bg-green-500';
    case 'moderate': return 'bg-yellow-500';
    case 'unhealthy': return 'bg-orange-500';
    case 'hazardous': return 'bg-red-500';
    default: return 'bg-gray-500';
  }
};

const getStatusMessage = (status) => {
  switch (status) {
    case 'good': return 'Breathe freely!';
    case 'moderate': return 'Acceptable quality';
    case 'unhealthy': return 'May cause discomfort';
    case 'hazardous': return 'Health warnings!';
    default: return '';
  }
};

const getHealthRecommendations = (status) => {
  switch (status) {
    case 'good':
      return [
        'Air quality is considered satisfactory, and air pollution poses little or no risk.',
        'Enjoy outdoor activities as normal.',
        'Keep windows open to let in fresh air.',
        'Perfect time for outdoor exercise and sports.'
      ];
    case 'moderate':
      return [
        'Air quality is acceptable; however, there may be a risk for some people.',
        'Unusually sensitive individuals should consider limiting prolonged outdoor exertion.',
        'Keep windows closed during peak traffic hours.',
        'Consider monitoring symptoms if you have respiratory issues.'
      ];
    case 'unhealthy':
      return [
        'Everyone may begin to experience health effects; members of sensitive groups may experience more serious effects.',
        'Reduce prolonged or heavy outdoor exertion.',
        'Keep windows closed and use air purifiers if available.',
        'People with respiratory or heart disease should stay indoors.',
        'Wear masks when outdoors, especially N95 or equivalent.'
      ];
    case 'hazardous':
      return [
        'Health warnings of emergency conditions. The entire population is more likely to be affected.',
        'Avoid all outdoor physical activity.',
        'Stay indoors with windows and doors closed.',
        'Run air purifiers if available.',
        'Wear appropriate masks if you must go outside.',
        'Follow public health announcements and instructions.'
      ];
    default:
      return [
        'Monitor local air quality reports.',
        'Follow any health advice from local authorities.'
      ];
  }
};

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




