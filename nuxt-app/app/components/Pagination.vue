<template>
  <div v-if="totalPages > 1" class="pagination">
    <NuxtLink
      v-if="currentPage > 1"
      :to="basePath + (currentPage - 1 === 1 ? '' : `/page/${currentPage - 1}`)"
    >
      上一页
    </NuxtLink>
    <NuxtLink
      v-for="p in totalPages"
      :key="p"
      :to="basePath + (p === 1 ? '' : `/page/${p}`)"
      :class="{ active: p === currentPage }"
    >
      {{ p }}
    </NuxtLink>
    <NuxtLink
      v-if="currentPage < totalPages"
      :to="`${basePath}/page/${currentPage + 1}`"
    >
      下一页
    </NuxtLink>
  </div>
</template>

<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  basePath: {
    type: String,
    required: true,
  },
})
</script>
