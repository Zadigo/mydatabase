import { DatabaseEndpoint } from '#shared/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const id = getRouterParam(event, 'id')
    const body = await readBody(event)

    return await $fetch<DatabaseEndpoint[]>(`/v1/endpoints/${id}`, {
      method: 'PUT',
      baseURL: useRuntimeConfig().public.prodDomain,
      body
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
