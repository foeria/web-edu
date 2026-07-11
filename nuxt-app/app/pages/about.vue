<template>
  <div>
    <SectionHero
      :title="about.title"
      :subtitle="about.company"
    />

    <div class="about-section">
      <div class="container article-detail-container">
        <p
          v-for="(p, idx) in about.paragraphs"
          :key="idx"
          class="about-paragraph"
        >
          {{ p }}
        </p>
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
