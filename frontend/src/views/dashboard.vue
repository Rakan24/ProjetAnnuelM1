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
        <li v-if="isStaff">
          <button @click="goToThresholds" class="hover:bg-gray-700 rounded px-3 py-1">Gérer les seuils</button>
        </li>
        <li>
          <button @click="logout" class="hover:bg-gray-700 rounded px-3 py-1">Se déconnecter</button>
        </li>
      </ul>
    </div>
  </nav>

  <div class="py-6 max-w-7xl mx-auto px-4">
    <header class="flex flex-col items-start md:flex-row md:items-center md:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Air Quality Dashboard</h1>
        <p class="text-gray-600">{{ formattedDate }}</p>
      </div>
    </header>

    <LoadingScreen v-if="store.isLoading" />

    <section v-else-if="store.error" class="flex items-center justify-center h-64">
      <div class="text-center">
        <p class="text-red-500 text-lg">{{ store.error }}</p>
        <button
          @click="store.fetchForecast"
          class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Réessayer
        </button>
      </div>
    </section>

    <section v-else-if="!today" class="flex items-center justify-center h-64">
      <p class="text-gray-500 text-lg">Aucune donnée de prévision disponible</p>
    </section>

    <section v-else>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card :class="`bg-gradient-to-br ${getStatusColor(today.status)}`">
          <CardHeader>
            <CardTitle class="text-white">Qualité de l'air aujourd'hui</CardTitle>
            <CardDescription class="text-white/80">Statut global de la qualité de l'air</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="flex items-end justify-between">
              <div>
                <p class="text-4xl font-bold text-white">{{ today.aqi }}</p>
                <p class="text-white/90 mt-1 text-lg capitalize">{{ today.status }}</p>
              </div>
              <div class="text-right">
                <p class="text-white/90">{{ getStatusMessage(today.status) }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card class="col-span-1 md:col-span-2">
          <CardHeader>
            <CardTitle>Polluants critiques</CardTitle>
            <CardDescription>Niveaux des polluants clés aujourd'hui</CardDescription>
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
        <Card class="col-span-1 lg:col-span-2 pb-14">
          <CardHeader>
            <CardTitle>Prévisions qualité de l'air sur 7 jours</CardTitle>
            <CardDescription>Niveaux de pollution pour la semaine à venir</CardDescription>
          </CardHeader>
          <CardContent>
            <div class="h-80 w-full">
              <AirQualityChart :forecasts="store.forecasts" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recommandations santé</CardTitle>
            <CardDescription>Basées sur la qualité de l'air actuelle</CardDescription>
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
            <CardTitle>Prévisions détaillées</CardTitle>
            <CardDescription>Prévision qualité de l'air jour par jour</CardDescription>
          </CardHeader>
          <CardContent>
            <ForecastCards :forecasts="store.forecasts" />
          </CardContent>
        </Card>
      </div>

      <div>
        <Card>
          <CardHeader>
            <CardTitle>Détails des polluants</CardTitle>
            <CardDescription>Informations détaillées pour chaque polluant</CardDescription>
          </CardHeader>
          <CardContent>
            <PollutantTable :forecasts="store.forecasts" />
          </CardContent>
        </Card>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { format } from 'date-fns';
import { useAirQualityStore } from '../stores/airQualityStore';
import { useRouter } from 'vue-router';

import Card from '../components/ui/Card.vue';
import CardHeader from '../components/ui/CardHeader.vue';
import CardTitle from '../components/ui/CardTitle.vue';
import CardDescription from '../components/ui/CardDescription.vue';
import CardContent from '../components/ui/CardContent.vue';

import AirQualityChart from '../components/dashboard/AirQualityChart.vue';
import ForecastCards from '../components/dashboard/ForecastCards.vue';
import PollutantTable from '../components/dashboard/PollutantTable.vue';
import LoadingScreen from '../components/ui/LoadingScreen.vue';

const router = useRouter();
const store = useAirQualityStore();

const today = computed(() => {
  if (!Array.isArray(store.forecasts) || store.forecasts.length === 0) return null;
  return store.forecasts[0];
});

const formattedDate = computed(() => format(new Date(), 'EEEE, MMMM d, yyyy'));

onMounted(async () => {
  await store.fetchForecast();
});

// Couleurs et styles par statut qualité
const getStatusColor = (status) => {
  switch (status) {
    case 'good':
      return 'from-green-500 to-green-600';
    case 'moderate':
      return 'from-yellow-400 to-yellow-500';
    case 'unhealthy':
      return 'from-orange-500 to-orange-600';
    case 'hazardous':
      return 'from-red-500 to-red-600';
    default:
      return 'from-blue-500 to-blue-600';
  }
};

const getPollutantCardColor = (status) => {
  switch (status) {
    case 'good':
      return 'bg-green-50 text-green-700';
    case 'moderate':
      return 'bg-yellow-50 text-yellow-700';
    case 'unhealthy':
      return 'bg-orange-50 text-orange-700';
    case 'hazardous':
      return 'bg-red-50 text-red-700';
    default:
      return 'bg-gray-50 text-gray-700';
  }
};

const getStatusDotColor = (status) => {
  switch (status) {
    case 'good':
      return 'bg-green-500';
    case 'moderate':
      return 'bg-yellow-500';
    case 'unhealthy':
      return 'bg-orange-500';
    case 'hazardous':
      return 'bg-red-500';
    default:
      return 'bg-gray-500';
  }
};

const getStatusMessage = (status) => {
  switch (status) {
    case 'good':
      return 'Respirez librement !';
    case 'moderate':
      return 'Qualité acceptable';
    case 'unhealthy':
      return 'Peut causer des gênes';
    case 'hazardous':
      return 'Alerte sanitaire !';
    default:
      return '';
  }
};

const getHealthRecommendations = (status) => {
  switch (status) {
    case 'good':
      return [
        "La qualité de l'air est satisfaisante, peu ou pas de risque.",
        "Profitez des activités extérieures normalement.",
        "Gardez les fenêtres ouvertes pour aérer.",
        "Idéal pour les exercices et sports en plein air.",
      ];
    case 'moderate':
      return [
        "Qualité acceptable mais risque pour certaines personnes.",
        "Personnes sensibles : limitez les efforts prolongés dehors.",
        "Fermez les fenêtres aux heures de pointe.",
        "Surveillez les symptômes si problème respiratoire.",
      ];
    case 'unhealthy':
      return [
        "Effets possibles sur la santé pour tous, plus sérieux pour les groupes sensibles.",
        "Réduisez les efforts prolongés ou intenses à l'extérieur.",
        "Gardez fenêtres fermées, utilisez purificateurs si possible.",
        "Personnes à risque : restez à l'intérieur.",
        "Portez un masque adéquat (N95 ou équivalent) à l'extérieur.",
      ];
    case 'hazardous':
      return [
        "Alerte sanitaire d'urgence, toute la population est affectée.",
        "Évitez toute activité physique en extérieur.",
        "Restez à l'intérieur, fenêtres et portes fermées.",
        "Utilisez purificateurs d'air si possible.",
        "Portez un masque approprié si sortie nécessaire.",
        "Suivez les consignes des autorités sanitaires.",
      ];
    default:
      return [
        "Surveillez les bulletins locaux de qualité de l'air.",
        "Suivez les conseils des autorités sanitaires.",
      ];
  }
};

// Navigation sidebar
const goToProfile = () => router.push('/profile');
const goToDashboard = () => router.push('/dashboard');
const goToThresholds = () => router.push('/thresholds');
const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

const isStaff = localStorage.getItem('is_staff') === 'true'

//Debug
//console.log('Role utilisateur:', isStaff);
</script>
