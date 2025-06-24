<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm text-left">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3">Pollutant</th>
          <th scope="col" class="px-6 py-3">Current</th>
          <th scope="col" class="px-6 py-3">Status</th>
          <th scope="col" class="px-6 py-3">Unit</th>
          <th scope="col" class="px-6 py-3">Health Impact</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="pollutant in todayPollutants" 
          :key="pollutant.id"
          class="bg-white border-b hover:bg-gray-50"
        >
          <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
            {{ pollutant.name }}
          </th>
          <td class="px-6 py-4">{{ pollutant.value }}</td>
          <td class="px-6 py-4">
            <span :class="['px-2 py-1 rounded-full text-xs font-medium', getPollutantBadgeColor(pollutant.status)]">
              {{ pollutant.status }}
            </span>
          </td>
          <td class="px-6 py-4">{{ pollutant.unit }}</td>
          <td class="px-6 py-4 text-gray-600">
            {{ getHealthImpact(pollutant.name) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  forecasts: {
    type: Array,
    required: true
  }
});

const todayPollutants = computed(() => {
  return props.forecasts[0]?.pollutants || [];
});

const getPollutantBadgeColor = (status) => {
  switch (status) {
    case 'good': return 'bg-green-100 text-green-800';
    case 'moderate': return 'bg-yellow-100 text-yellow-800';
    case 'unhealthy': return 'bg-orange-100 text-orange-800';
    case 'hazardous': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

const getHealthImpact = (pollutantName) => {
  const impacts = {
    'PM2.5': 'Respiratory and cardiovascular effects',
    'PM10': 'Irritation of airways, coughing',
    'O3': 'Lung irritation, breathing difficulties',
    'NO2': 'Respiratory problems, lung damage'
  };
  return impacts[pollutantName] || 'Health effects vary';
};
</script>
