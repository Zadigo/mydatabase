import { useGoogleSheets } from '@/composables/google'
import { loadLayout, loadView } from '@/composables/utils'
import { useGoogle } from '@/store/google'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: loadLayout('DashboardLayout'),
      children: [
        {
          path: '',
          name: 'home_view',
          component: loadView('HomeView')
        },
        {
          path: 'slide/:id(\\d+)',
          name: 'slide_view',
          component: loadView('SlideView')
        },
        {
          path: 'integrations',
          name: 'integrations_view',
          component: loadView('IntegrationsView')
        },
        {
          path: 'connections',
          name: 'connections_view',
          component: loadView('ConnectionsView')
        },
        {
          path: 'settings',
          name: 'settings_view',
          component: loadView('SettingsView')
        },
        {
          path: 'rest/oauth2-credential/callback',
          name: 'google_oauth_view',
          component: loadView('GoogleAuthView')
        }
      ]
    },
    {
      path: '/page/:id(pg\\_[a-zA-Z0-9]+)/preview',
      name: 'page_preview_view',
      component: loadView('PagePreviewView')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authenticationStore = useGoogle()
  const sheetsStore = useGoogleSheets()
  authenticationStore
  sheetsStore
  next()
})

export default router
