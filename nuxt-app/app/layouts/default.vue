<template>
  <div>
    <header>
      <!-- Top bar with logo and hotline -->
      <div class="top-bar">
        <div class="container top-bar-inner">
          <NuxtLink to="/" class="top-logo">
            <img src="/images/common/001_96e14f88ddf0738.png" alt="济南德泓教育咨询有限公司">
          </NuxtLink>
          <div class="top-hotline">
            <h1>{{ site.hotlineLabel }}{{ site.hotline }}</h1>
          </div>
        </div>
      </div>

      <!-- Main navigation -->
      <nav class="top-nav">
        <div class="container">
          <ul>
            <li
              v-for="item in site.nav"
              :key="item.path"
              :class="{ active: route.path === item.path || route.path.startsWith(item.path + '/') }"
            >
              <NuxtLink :to="item.path">{{ item.label }}</NuxtLink>
            </li>
          </ul>
        </div>
      </nav>
    </header>

    <main>
      <slot />
    </main>

    <SiteFooter />
  </div>
</template>

<script setup>
import site from '~/public/data/site.json'

const route = useRoute()

useHead({
  titleTemplate: (title) => title ? `${title}-${site.title}` : site.title,
})
</script>
