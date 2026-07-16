import { Database } from '~/types'
import { createErrorTemplate } from '~/utils'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody<{ id: string, name: string }>(event)

  try {
    return $fetch<Database>(`/v1/databases/${body.id}`, {
      method: 'POST',
      baseURL: config.public.prodDomain,
      body: {
        name: body.name
      }
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
