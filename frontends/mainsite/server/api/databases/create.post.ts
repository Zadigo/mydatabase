import type { Database } from  '~/types'
import type { NewDatabase } from '~/composables/use/databases'
import { createErrorTemplate } from '~/utils'

export default defineEventHandler(async (_event) => {
  const newDatabase = await readBody<NewDatabase>(_event)

  try {
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
