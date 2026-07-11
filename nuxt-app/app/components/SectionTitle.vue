<template>
  <div class="section-title">
    <div class="section-title-inner">
      <span class="section-title-line" />
      <span>{{ title }}</span>
      <span class="section-title-line" />
    </div>
    <div v-if="subtitle" class="section-subtitle">{{ subtitle }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})
</script>
