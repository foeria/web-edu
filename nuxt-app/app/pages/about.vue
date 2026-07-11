<template>
  <div class="section-hero">
    <div class="container">
      <div class="section-hero-title">{{ about.title }}</div>
      <div class="section-hero-subtitle">{{ about.company }}</div>
    </div>
  </div>

  <div class="about-section">
    <div class="container">
      <div class="about-text" style="max-width: 960px; margin: 0 auto;">
        <p v-for="(p, idx) in about.paragraphs" :key="idx" style="margin-bottom: 20px;">{{ p }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import about from '~/public/data/about.json'

useHead({
  title: about.title,
})
</script>
