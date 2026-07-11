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
          :current-page="currentPage"
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
const currentPage = parseInt(route.params.page, 10)

if (!sections[sectionKey]) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found' })
}

const sectionData = await import(`~/public/data/sections/${sectionKey}.json`).then(m => m.default)

const PAGE_SIZE = 12
const totalPages = Math.ceil(sectionData.articles.length / PAGE_SIZE)

if (isNaN(currentPage) || currentPage < 2 || currentPage > totalPages) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found' })
}

const pageArticles = computed(() => {
  const start = (currentPage - 1) * PAGE_SIZE
  return sectionData.articles.slice(start, start + PAGE_SIZE)
})

useHead({
  title: `${sectionData.title} - 第${currentPage}页`,
})
</script>
