<template>
  <section class="home-section-block home-news-section">
    <div class="container">
      <SectionTitle :title="title" :subtitle="subtitle" />
      <div class="home-news">
        <div class="home-news-image">
          <img src="/images/common/002_nyban.jpg" :alt="title">
        </div>
        <div class="home-news-list">
          <NuxtLink
            v-for="item in items"
            :key="item.id"
            :to="item.path"
            class="home-news-item"
          >
            <div class="home-news-date">
              <div class="home-news-day">{{ item.day }}</div>
              <div class="home-news-year">{{ item.year }}</div>
            </div>
            <div class="home-news-body">
              <div class="home-news-title">{{ item.title }}</div>
              <div class="home-news-excerpt">{{ item.excerpt }}</div>
              <div class="home-news-more">[详细]</div>
            </div>
          </NuxtLink>
        </div>
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
  items: {
    type: Array,
    required: true,
  },
})
</script>
