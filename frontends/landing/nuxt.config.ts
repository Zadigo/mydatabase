// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxt/test-utils/module',
    '@vueuse/nuxt',
    '@vueuse/motion',
    '@nuxt/fonts',
    '@nuxt/image',
    '@nuxtjs/seo',
    '@nuxtjs/i18n',
    'nuxt-vuefire',
    'nuxt-skew-protection',
    'nuxt-ai-ready'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/': { prerender: true },
    '/auth/**': { prerender: true }
  },

  compatibilityDate: '2026-06-30',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  fonts: {
    families: [
      {
        name: 'Zain',
      },
      {
        name: 'Nunito',
      }
    ]
  },

  imports: {
    dirs: [
      '~/constants'
    ]
  },

  runtimeConfig: {
    contactSecret: process.env.NUXT_JWT_CONTACT_SECRET,
    contactToken: process.env.NUXT_JWT_CONTACT_TOKEN,

    firebaseClientEmail: process.env.NUXT_FIREBASE_CLIENT_EMAIL,
    firebasePrivateKey: process.env.NUXT_FIREBASE_PRIVATE_KEY,

    public: {
      siteUrl: '',
      siteName: '',
      jwtContactEndpoint: '',

      firebaseProjectId: '',
    }
  },

  i18n: {
    baseUrl: process.env.NUXT_SITE_URL,
    langDir: './locales',
    defaultLocale: 'fr',
    vueI18n: './i18n.config.ts',
    customRoutes: 'config',
    pages: {
      '/auth/waitlist': { fr: '/auth/liste-d-attente', en: '/auth/waitlist' },
    },
    locales: [
      {
        code: 'fr',
        language: 'fr-FR',
        file: 'fr-FR.ts',
        dir: 'ltr',
        name: 'French'
      },
      {
        code: 'en',
        language: 'en-US',
        files: [ 'en.ts', 'en-US.ts' ],
        dir: 'ltr',
        name: 'English'
      }
    ]
  },

  app: {
    pageTransition: {
      name: 'page',
      mode: 'out-in'
    },

    head: {
      titleTemplate: '%s %separator %siteName',
      templateParams: {
        separator: '-',
        siteName: process.env.NUXT_PUBLIC_SITE_NAME || 'John PM Consulting'
      }
    }
  },

  ogImage: {
    componentDirs: [ 'og-image' ]
  },

  vuefire: {
    config: {
      apiKey: process.env.NUXT_FIREBASE_API_KEY,
      authDomain: process.env.NUXT_FIREBASE_AUTH_DOMAIN,
      databaseURL: process.env.NUXT_FIREBASE_DATABASE_URL,
      storageBucket: process.env.NUXT_FIREBASE_STORAGE_BUCKET,
      appId: process.env.NUXT_FIREBASE_APP_ID,
      measurementId: process.env.NUXT_FIREBASE_MEASUREMENT_ID,
      messagingSenderId: process.env.NUXT_FIREBASE_MESSAGING_SENDER_ID,
      projectId: process.env.NUXT_FIREBASE_PROJECT_ID
    }
  },
})
