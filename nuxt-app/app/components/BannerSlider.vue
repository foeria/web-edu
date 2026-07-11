<template>
  <div class="banner-slider">
    <div
      v-for="(slide, index) in slides"
      :key="index"
      class="banner-slide"
      :class="{ active: index === currentIndex }"
    >
      <NuxtLink v-if="slide.link" :to="slide.link">
        <img :src="slide.src" :alt="slide.alt || ''">
      </NuxtLink>
      <img v-else :src="slide.src" :alt="slide.alt || ''">
    </div>

    <div v-if="slides.length > 1" class="banner-dots">
      <button
        v-for="(_, index) in slides"
        :key="index"
        :class="{ active: index === currentIndex }"
        @click="goTo(index)"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  slides: {
    type: Array,
    required: true,
  },
  interval: {
    type: Number,
    default: 4000,
  },
})

const currentIndex = ref(0)
let timer = null

function goTo(index) {
  currentIndex.value = index
  resetTimer()
}

function next() {
  currentIndex.value = (currentIndex.value + 1) % props.slides.length
}

function resetTimer() {
  if (timer) {
    clearInterval(timer)
  }
  if (props.slides.length > 1 && props.interval > 0) {
    timer = setInterval(next, props.interval)
  }
}

onMounted(() => {
  resetTimer()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>
