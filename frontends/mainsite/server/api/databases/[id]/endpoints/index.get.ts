import { DatabaseEndpoint } from '~/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')

    return await $fetch<DatabaseEndpoint[]>(`/v1/databases/${id}/endpoints`, {
      method: 'GET',
      baseURL: useRuntimeConfig().public.prodDomain,
      headers: [
        ['Content-Type', 'application/json'],
        ['Accept', 'application/json']
      ]
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
