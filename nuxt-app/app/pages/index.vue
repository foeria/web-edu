<template>
  <div>
    <!-- Banner -->
    <section class="banner-section">
      <BannerSlider :slides="home.banners" :interval="4000" />
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

    <!-- Problem Forum -->
    <HomeSectionGrid
      :title="home.previews.zanding.title"
      :subtitle="home.previews.zanding.subtitle"
      :articles="home.previews.zanding.articles"
    />

    <!-- Comprehensive Education -->
    <HomeSectionGrid
      :title="home.previews.zonghe.title"
      :subtitle="home.previews.zonghe.subtitle"
      :articles="home.previews.zonghe.articles"
    />

    <!-- Expansion Training Gallery -->
    <HomeGallery
      :title="home.previews.xunlian.title"
      :subtitle="home.previews.xunlian.subtitle"
      :items="home.previews.xunlian.images"
    />

    <!-- Psychological Counseling News -->
    <HomeNewsList
      :title="home.previews.zixun.title"
      :subtitle="home.previews.zixun.subtitle"
      :items="home.previews.zixun.items"
    />

    <!-- Student Style -->
    <HomeSectionGrid
      :title="home.previews.fengcai.title"
      :subtitle="home.previews.fengcai.subtitle"
      :articles="home.previews.fengcai.articles"
    />
  </div>
</template>

<script setup>
import home from '~/public/data/home.json'

useHead({
  title: '',
})
</script>
