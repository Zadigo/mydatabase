import { createApp, toRaw } from 'vue'
import { createAxios } from './plugins/axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'

import App from './App.vue'

import 'vuetify/styles'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import './plugins/fontawesome'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import router from './router'
import { createVueLocalStorage, createVueSession } from './composables/vue-storages'

const client = createAxios()
const pinia = createPinia()
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  }
})

const session = createVueSession()
const localstorage = createVueLocalStorage()

const app = createApp(App)

pinia.use(({ store }) => {
  store.$session = toRaw(session)
  store.$http = toRaw(client)
})

app.use(client)
app.use(session)
app.use(localstorage)
app.use(router)
app.use(pinia)
app.use(vuetify)
app.component('FontAwesomeIcon', FontAwesomeIcon)

app.mount('#app')
