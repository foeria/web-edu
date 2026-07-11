<template>
  <div class="section-hero" :style="heroStyle">
    <div class="container">
      <div class="section-hero-title">{{ title }}</div>
      <div v-if="subtitle" class="section-hero-subtitle">{{ subtitle }}</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  image: {
    type: String,
    default: '/images/common/002_nyban.jpg',
  },
})

const heroStyle = computed(() => ({
  backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('${props.image}')`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
}))
</script>
