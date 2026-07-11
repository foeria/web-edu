<template>
  <section class="home-section-block home-gallery-section">
    <div class="container">
      <SectionTitle :title="title" :subtitle="subtitle" />
      <div v-if="items.length" class="home-gallery">
        <div class="home-gallery-large">
          <NuxtLink :to="items[0].path">
            <img :src="items[0].src" :alt="items[0].alt || items[0].title">
            <div v-if="items[0].title" class="home-gallery-caption">{{ items[0].title }}</div>
          </NuxtLink>
        </div>
        <div class="home-gallery-small">
          <NuxtLink
            v-for="item in items.slice(1, 5)"
            :key="item.src"
            :to="item.path"
            class="home-gallery-small-item"
          >
            <img :src="item.src" :alt="item.alt || item.title">
            <div v-if="item.title" class="home-gallery-caption">{{ item.title }}</div>
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
