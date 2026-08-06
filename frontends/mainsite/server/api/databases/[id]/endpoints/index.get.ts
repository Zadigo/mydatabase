import { DatabaseEndpoint } from '~/types'
import { createErrorTemplate } from '~/utils'

export default defineEventHandler(async (event) => {
  try {
    const query = getQuery(event) as { databaseId: string }

    return await $fetch<DatabaseEndpoint[]>(`/v1/databases/${ query.databaseId }/endpoints`, {
      baseURL: useRuntimeConfig().public.prodDomain
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
