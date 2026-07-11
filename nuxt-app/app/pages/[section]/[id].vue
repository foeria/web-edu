<template>
  <div v-if="article">
    <div class="section-hero">
      <div class="container">
        <div class="section-hero-title">{{ sectionData.title }}</div>
        <div class="section-hero-subtitle">{{ sectionData.subtitle }}</div>
      </div>
    </div>

    <div class="about-section">
      <div class="container" style="max-width: 960px;">
        <h1 style="color: #c1272d; font-size: 24px; margin-bottom: 16px;">{{ article.title }}</h1>
        <div style="color: #999; font-size: 14px; margin-bottom: 24px;">
          <span v-if="article.date">时间：{{ article.date }}</span>
          <span v-if="article.author" style="margin-left: 20px;">作者：{{ article.author }}</span>
          <span v-if="article.clicks" style="margin-left: 20px;">点击：{{ article.clicks }}</span>
        </div>

        <div v-if="article.body" style="line-height: 1.8; color: #333;">
          <p v-for="(p, idx) in article.body" :key="idx" style="margin-bottom: 16px;">{{ p }}</p>
        </div>

        <div v-if="article.images?.length" style="margin-top: 30px;">
          <img
            v-for="img in article.images"
            :key="img.src"
            :src="img.src"
            :alt="img.alt || article.title"
            style="max-width: 100%; margin-bottom: 16px;"
          >
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
          <div v-if="article.prev">
            上一篇：<NuxtLink :to="`/${sectionKey}/${article.prev.id}`" style="color: #c1272d;">{{ article.prev.title }}</NuxtLink>
          </div>
          <div v-if="article.next" style="margin-top: 8px;">
            下一篇：<NuxtLink :to="`/${sectionKey}/${article.next.id}`" style="color: #c1272d;">{{ article.next.title }}</NuxtLink>
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
