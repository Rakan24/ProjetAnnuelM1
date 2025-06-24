import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

/**
 * @typedef {Object} Pollutant
 * @property {string} id
 * @property {string} name
 * @property {number} value
 * @property {string} unit
 * @property {'good'|'moderate'|'unhealthy'|'hazardous'} status
 */

/**
 * @typedef {Object} AirQualityForecast
 * @property {string} date
 * @property {number} aqi
 * @property {'good'|'moderate'|'unhealthy'|'hazardous'} status
 * @property {Pollutant[]} pollutants
 */

export const useAirQualityStore = defineStore('airQuality', () => {
  const forecasts = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  /**
   * @returns {AirQualityForecast[]}
   */
  const generateMockData = () => {
    const statuses = ['good', 'moderate', 'unhealthy', 'hazardous'];
    const pollutantNames = ['PM2.5', 'PM10', 'O3', 'NO2'];

    return Array.from({ length: 7 }, (_, index) => {
      const date = new Date();
      date.setDate(date.getDate() + index);

      const status = statuses[Math.floor(Math.random() * statuses.length)];
      const aqi = status === 'good'
        ? Math.floor(Math.random() * 50) + 1
        : status === 'moderate'
        ? Math.floor(Math.random() * 50) + 51
        : status === 'unhealthy'
        ? Math.floor(Math.random() * 100) + 101
        : Math.floor(Math.random() * 200) + 201;

      /** @type {Pollutant[]} */
      const pollutants = pollutantNames.map((name) => ({
        id: `${name.toLowerCase()}-${index}`,
        name,
        value: Math.floor(Math.random() * 100) + 10,
        unit: name.includes('PM') ? 'μg/m³' : 'ppb',
        status: statuses[Math.floor(Math.random() * statuses.length)]
      }));

      return {
        date: date.toISOString(),
        aqi,
        status,
        pollutants
      };
    });
  };

  const fetchForecast = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      forecasts.value = generateMockData();
    } catch (err) {
      error.value = 'Failed to fetch air quality data';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    forecasts: computed(() => forecasts.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    fetchForecast
  };
});
