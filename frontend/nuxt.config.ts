import tailwind from '@tailwindcss/vite'

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
    '@vueuse/nuxt',
    '@nuxt/test-utils/module',
    'pinia-plugin-persistedstate/nuxt'
  ],

  routeRules: {
    '/': { ssr: true },
    '/databases/**': { ssr: false }
  },

  ui: {
    prefix: 'Nuxt'
  },

  css: [
    '~/assets/css/tailwind.css'
  ],

  vite: {
    plugins: [
      tailwind()
    ]
  }
})
