// import { useGoogleSheets } from '@/composables/googlasync e'
// import { useGoogle } from '@/store/goasync ogle'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: async () => import('../layouts/DashboardLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: async () => import('../pages/HomePage.vue')
        },
        {
          path: 'slide/:id',
          name: 'slide',
          component: async () => import('../pages/SlidePage.vue')
        }
        // {
        //   path: 'integrations',
        //   name: 'integrations',
        //   component: async () => import('../pages/IntegrationsPage.vue')
        // },
        // {
        //   path: 'connections',
        //   name: 'connections',
        //   component: async () => import('../pages/ConnectionsPage.vue')
        // },
        // {
        //   path: 'settings',
        //   name: 'settings',
        //   component: async () => import('../pages/SettingsPage.vue')
        // },
        // {
        //   path: 'rest/oauth2-credential/callback',
        //   name: 'google_oauth',
        //   component: async () => import('../pages/GoogleAuthPage.vue')
        // }
      ]
    },
    {
      path: '/slide/:id(sl\\_[a-zA-Z0-9]+)/preview',
      component: async () => import('../pages/SlidePreviewPage.vue'),
      name: 'page_preview'
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   const authenticationStore = useGoogle()
//   const sheetsStore = useGoogleSheets()
//   authenticationStore
//   sheetsStore
//   next()
// })

export default router
