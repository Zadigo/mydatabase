import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Icon } from '@iconify/vue'

import App from './App.vue'
import router from './router'
import createPlugins from './plugins'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import './style.css'

const app = createApp(App)

const pinia = createPinia()

app.component('IconBase', Icon)
app.use(router)
app.use(pinia)
app.use(createPlugins())
app.mount('#app')
