import { createErrorTemplate } from '#server/utils/errors'
import { useFirebaseAdmin } from '#server/utils/server_firebase'

export default defineEventHandler(async (event) => {
  try {
    const parsedBody = await readBody<WaitllistData>(event)

    const { db } = useFirebaseAdmin()
    const docRef = db.collection('waitlist').doc()
    await docRef.set({
      ...parsedBody,
      createdAt: new Date().toISOString()
    })
  } catch(error) {
    const template = createErrorTemplate(error)
    return createError(template)
  }
})
