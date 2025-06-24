<template>
  <div class="notfound-container">
    <h1 class="text-6xl font-bold text-gray-800">404</h1>
    <p class="text-2xl mt-4 text-gray-600">Oops! La page que vous cherchez n'existe pas.</p>
    <button @click="goHome" class="mt-8 px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition">
      Retour à l'accueil
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.notfound-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 1rem;
}
</style>
