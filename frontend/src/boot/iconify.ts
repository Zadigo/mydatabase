import { defineBoot } from '#q-app/wrappers'
import { Icon } from '@iconify/vue'

export default defineBoot(({ app }) => {
  app.component('IconBase', Icon)
})
