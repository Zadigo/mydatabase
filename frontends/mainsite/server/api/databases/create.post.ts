import type { Database } from  '~/types'
import { createErrorTemplate } from '~/utils/errors'
import { NewDatabaseSchema, NewDatabase  } from '~~/shared/types'

export default defineEventHandler(async (event) => {
  try {
    const newDatabase = await readBody<NewDatabase>(event)

    const validatedData = NewDatabaseSchema.safeParse(newDatabase)
    if (!validatedData.success) {
      const error = new Error(`Validation error: ${validatedData.error.message}`)
      const template = createErrorTemplate(error)
      throw createError(template)
    }

    return await $fetch<Database>('/v1/databases/create', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: newDatabase
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
