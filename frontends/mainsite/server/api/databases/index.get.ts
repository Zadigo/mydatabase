import { Database } from '~/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async () => {
  try {
    return await $fetch<Database[]>('/v1/databases', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.prodDomain,
      headers: [
        ['Accept', 'application/json'],
        ['Content-Type', 'application/json']
      ]
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
