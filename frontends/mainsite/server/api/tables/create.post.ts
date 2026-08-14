import { SimpleTable } from '~/types'
import { createErrorTemplate } from '~/utils/errors'
import { NewTableSchema } from '~~/shared/types'
import type { NewTable } from '~~/shared/types'

export default defineEventHandler(async (event) => {
  try {
    const postData = await readBody<NewTable>(event)
    const validatedData = NewTableSchema.safeParse(postData)

    if (!validatedData.success) {
      const error = new Error(`Validation error: ${validatedData.error.message}`)
      const template = createErrorTemplate(error)
      throw createError(template)
    }

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
