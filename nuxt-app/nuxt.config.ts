// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
  ],
  devtools: { enabled: true },
  compatibilityDate: '2024-04-03',
  // NUXT_PUBLIC_API_BASE overrides the default at build/runtime time.
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost/api',
    },
  },
})
