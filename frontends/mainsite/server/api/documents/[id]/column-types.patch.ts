import { ColumnOptions } from '~/types'
import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const params = getRouterParams(event) as { id: string }
    const columnOptions = await readBody<ColumnOptions[]>(event)

    return await $fetch(`/v1/documents/${params.id}/column-types`, {
      method: 'PATCH',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: {
        column_options: columnOptions
      }
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
