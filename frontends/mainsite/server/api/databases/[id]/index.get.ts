import { Database } from '~/types'
import { createErrorTemplate } from '~/utils'

export default defineEventHandler(async (event) => {
  try {
    const config = useRuntimeConfig()
    const body = await readBody<{ databaseId: string, name: string }>(event)

    return await $fetch<Database>(`/v1/databases/${ body.databaseId }`, {
      baseURL: config.public.prodDomain,
      method: 'POST',
      body: {
        name: body.name
      }
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    return createError(template)
  }
})
