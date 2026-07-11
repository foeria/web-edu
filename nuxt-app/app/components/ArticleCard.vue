<template>
  <NuxtLink :to="article.path" class="article-card">
    <div class="article-card-image">
      <img :src="article.image || '/images/common/002_nyban.jpg'" :alt="article.title">
    </div>
    <div class="article-card-body">
      <div class="article-card-title">{{ article.title }}</div>
      <div class="article-card-excerpt">{{ article.excerpt }}</div>
    </div>
  </NuxtLink>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true,
  },
})
</script>
