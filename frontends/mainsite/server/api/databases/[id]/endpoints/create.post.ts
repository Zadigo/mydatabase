import { DatabaseEndpoint } from '~/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody<{ endpointName: string, databaseId: number }>(event)

    return await $fetch<DatabaseEndpoint[]>(`/v1/endpoints/${ body.databaseId }/create`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: { endpoint: body.endpointName }
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
