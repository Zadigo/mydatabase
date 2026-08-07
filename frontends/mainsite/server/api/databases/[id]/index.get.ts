import { Database } from '~/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const config = useRuntimeConfig()
    const id = getRouterParam(event, 'id')

    return await $fetch<Database>(`/v1/databases/${id}`, {
      baseURL: config.public.prodDomain,
      method: 'GET'
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    return createError(template)
  }
})
