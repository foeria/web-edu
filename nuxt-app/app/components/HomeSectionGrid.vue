<template>
  <section class="home-section-block">
    <div class="container">
      <SectionTitle :title="title" :subtitle="subtitle" />
      <div class="home-section-grid">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
      </div>
    </div>
  </section>
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
  articles: {
    type: Array,
    required: true,
  },
})
</script>
