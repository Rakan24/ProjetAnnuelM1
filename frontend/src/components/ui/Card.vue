<template>
  <div :class="['bg-white rounded-lg shadow-md border border-gray-200', className]">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: ''
  }
});
</script>
