import { createErrorTemplate } from '#server/utils/errors'
import { useFirebaseAdmin } from '#server/utils/server_firebase'
import { type WaitlistData, WaitlistDataSchema } from '~~/shared/types'

export default defineEventHandler(async (event) => {
  try {
    const parsedBody = await readBody<WaitlistData>(event)

    const validatedData = WaitlistDataSchema.safeParse(parsedBody)
    if (!validatedData.success) {
      const err = new Error('Invalid waitlist data')
      const template = createErrorTemplate(err)
      return createError(template)
    }

    const { db } = useFirebaseAdmin()
    const docRef = db.collection('waitlist').doc()
    await docRef.set({
      ...validatedData.data, // TypeScript will now correctly infer the type as WaitlistData
      createdAt: new Date().toISOString()
    })
  } catch(error) {
    const template = createErrorTemplate(error)
    return createError(template)
  }
})
