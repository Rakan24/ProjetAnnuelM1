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
