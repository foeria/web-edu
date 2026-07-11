<template>
  <div v-if="sectionData">
    <SectionHero
      :title="sectionData.title"
      :subtitle="sectionData.subtitle"
    />

    <div class="article-list">
      <div class="container">
        <div class="article-grid">
          <ArticleCard
            v-for="article in pageArticles"
            :key="article.id"
            :article="article"
          />
        </div>

        <Pagination
          :current-page="1"
          :total-pages="totalPages"
          :base-path="`/${sectionKey}`"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import sections from '~/public/data/sections.json'

const route = useRoute()
const sectionKey = route.params.section

if (!sections[sectionKey]) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found' })
}

const sectionData = await import(`~/public/data/sections/${sectionKey}.json`).then(m => m.default)

const PAGE_SIZE = 12
const totalPages = Math.ceil(sectionData.articles.length / PAGE_SIZE)
const pageArticles = computed(() => sectionData.articles.slice(0, PAGE_SIZE))

useHead({
  title: sectionData.title,
})
</script>
