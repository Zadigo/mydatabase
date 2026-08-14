import { SimpleTable } from '~/types'
import { createErrorTemplate } from '~/utils/errors'
import type { EditableTableRef } from '~/types'

export default defineEventHandler(async (event) => {
  try {
    const params = getRouterParams(event) as { id: string }
    const updateData = await readBody<EditableTableRef>(event)

    return await $fetch<SimpleTable>(`/v1/tables/${params.id}`, {
      method: 'PATCH',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: updateData
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
