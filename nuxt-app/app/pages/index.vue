<template>
  <div>
    <!-- Banner -->
    <section class="banner-section">
      <img :src="home.banners[0]?.src" alt="济南德泓教育咨询有限公司">
    </section>

    <!-- About -->
    <section class="about-section">
      <div class="container about-grid">
        <div class="about-content">
          <div class="about-title">{{ home.about.title }}</div>
          <div class="about-text">{{ home.about.text }}</div>
          <NuxtLink :to="home.about.link" class="about-more">+查看更多</NuxtLink>
        </div>
        <div class="about-image">
          <img :src="home.about.image" :alt="home.about.title">
        </div>
      </div>
    </section>

    <!-- Section cards -->
    <section class="home-sections">
      <div class="container">
        <div class="home-sections-grid">
          <NuxtLink
            v-for="sec in home.sections"
            :key="sec.key"
            :to="sec.path"
            class="home-section-card"
          >
            <img :src="sec.image" :alt="sec.title">
            <div class="home-section-card-body">
              <div class="home-section-card-title">{{ sec.title }}</div>
              <div class="home-section-card-subtitle">{{ sec.subtitle }}</div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import home from '~/public/data/home.json'

useHead({
  title: '',
})
</script>
