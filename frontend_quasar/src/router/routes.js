
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', redirect: '/app' },
      { path: '/app', component: () => import('pages/HomePage.vue'), name: 'home' },
      { path: '/connections', component: () => import('pages/ConnectionsPage.vue'), name: 'connections' },
      { path: '/slide/:id(sl_[a-zA-Z]+)', component: () => import('pages/SlidePage.vue'), name: 'slide' }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
