import { SimpleTable } from '~/types'
import { createErrorTemplate } from '~/utils/errors'
import type { NewTable } from '~/composables/use'

export default defineEventHandler(async (event) => {
  try {
    const postData = await readBody<NewTable>(event)

    return await $fetch<SimpleTable>(`/v1/tables/create`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: postData
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
