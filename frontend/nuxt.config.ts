// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: true,

  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@pinia/nuxt',
    '@vueuse/nuxt'
  ],

  routeRules: {
    '/': { ssr: true },
    '/databases/**': { ssr: false }
  },

  ui: {
    prefix: 'ui'
  },

  css: [
    '~/assets/css/main.css'
  ]
})
