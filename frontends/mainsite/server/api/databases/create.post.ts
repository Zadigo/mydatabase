import type { Database } from  '~/types'
import type { NewDatabase } from '~/composables/use/databases'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const newDatabase = await readBody<NewDatabase>(event)
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
