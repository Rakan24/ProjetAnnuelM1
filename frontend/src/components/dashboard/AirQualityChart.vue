<template>
  <div class="w-full h-full relative overflow-visible">
    <div class="absolute left-0 ml-[-12%] w-[110%] max-w-none" style="top: -3%;">
      <Line :chart-data="chartData" :chart-options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);

const props = defineProps({
  forecasts: {
    type: Array,
    required: true
  }
});

const chartData = computed(() => ({
  labels: props.forecasts.map(f => f.date || 'Unknown'),
  datasets: [{
    label: 'AQI',
    data: props.forecasts.map(f => f.aqi),
    fill: false,
    borderColor: 'rgb(59, 130, 246)',
    backgroundColor: 'rgb(59, 130, 246)',
    tension: 0.3
  }]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  aspectRatio: 2,  // Ajuste selon largeur/hauteur souhaitée
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: '7-Day Air Quality Forecast',
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: 'AQI' }
    }
  }
};
</script>

<style scoped>
/* Forcer canvas à 100% largeur/hauteur */
canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}
</style>
