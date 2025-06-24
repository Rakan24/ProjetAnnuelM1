<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
    <div 
      v-for="forecast in forecasts" 
      :key="forecast.date"
      class="p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
    >
      <div class="flex justify-between items-start mb-2">
        <p class="text-sm font-medium text-gray-600">
          {{ formatDate(forecast.date) }}
        </p>
        <div :class="['w-3 h-3 rounded-full', getStatusDotColor(forecast.status)]"></div>
      </div>
      
      <div class="mb-2">
        <p class="text-2xl font-bold text-gray-900">{{ forecast.aqi }}</p>
        <p :class="['text-sm capitalize', getStatusTextColor(forecast.status)]">
          {{ forecast.status }}
        </p>
      </div>
      
      <div class="space-y-1">
        <div 
          v-for="pollutant in forecast.pollutants.slice(0, 2)" 
          :key="pollutant.id"
          class="flex justify-between text-xs text-gray-600"
        >
          <span>{{ pollutant.name }}</span>
          <span>{{ pollutant.value }}{{ pollutant.unit }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { format } from 'date-fns';

defineProps({
  forecasts: {
    type: Array,
    required: true
  }
});

const formatDate = (dateString) => {
  return format(new Date(dateString), 'EEE, MMM d');
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

const getStatusTextColor = (status) => {
  switch (status) {
    case 'good': return 'text-green-600';
    case 'moderate': return 'text-yellow-600';
    case 'unhealthy': return 'text-orange-600';
    case 'hazardous': return 'text-red-600';
    default: return 'text-gray-600';
  }
};
</script>
