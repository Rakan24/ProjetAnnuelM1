<template>
  <p :class="['text-sm text-gray-600 mt-1', className]">
    <slot />
  </p>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: ''
  }
});
</script>
