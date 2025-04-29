import { boot } from 'quasar/wrappers'
import { VueSession } from './session-storage'

const session = new VueSession()

export default boot(({ app }) => {
  session.setup(app)
  app.config.globalProperties.$session = session
})

export { session }
