// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [],
  devtools: { enabled: true },
  compatibilityDate: '2024-04-03',
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost/api',
    },
  },
  nitro: {
    prerender: {
      crawlLinks: true,
      routes: [
        '/',
        '/about',
        '/contact',
        '/zanding',
        '/zonghe',
        '/xunlian',
        '/zixun',
        '/fengcai',
      ],
    },
  },
})
