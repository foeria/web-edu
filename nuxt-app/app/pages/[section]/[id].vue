<template>
  <div v-if="article">
    <SectionHero
      :title="sectionData.title"
      :subtitle="sectionData.subtitle"
    />

    <div class="about-section article-detail-section">
      <div class="container article-detail-container">
        <h1 class="article-detail-title">{{ article.title }}</h1>
        <div class="article-detail-meta">
          <span v-if="article.date">时间：{{ article.date }}</span>
          <span v-if="article.author">作者：{{ article.author }}</span>
          <span v-if="article.clicks">点击：{{ article.clicks }}</span>
        </div>

        <div v-if="article.body" class="article-detail-body">
          <p v-for="(p, idx) in article.body" :key="idx">{{ p }}</p>
        </div>

        <div v-if="article.images?.length" class="article-detail-images">
          <figure
            v-for="img in article.images"
            :key="img.src"
          >
            <img :src="img.src" :alt="img.alt || article.title">
          </figure>
        </div>

        <div class="article-detail-nav">
          <div v-if="article.prev">
            上一篇：
            <NuxtLink :to="`/${sectionKey}/${article.prev.id}`">{{ article.prev.title }}</NuxtLink>
          </div>
          <div v-if="article.next">
            下一篇：
            <NuxtLink :to="`/${sectionKey}/${article.next.id}`">{{ article.next.title }}</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import sections from '~/public/data/sections.json'

const route = useRoute()
const sectionKey = route.params.section
const articleId = route.params.id

if (!sections[sectionKey]) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found' })
}

const sectionData = await import(`~/public/data/sections/${sectionKey}.json`).then(m => m.default)

const article = await import(`~/public/data/sections/${sectionKey}/${articleId}.json`)
  .then(m => m.default)
  .catch(() => {
    throw createError({ statusCode: 404, statusMessage: 'Article not found' })
  })

useHead({
  title: article.title,
})
</script>
