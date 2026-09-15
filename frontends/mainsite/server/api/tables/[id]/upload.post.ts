import { createErrorTemplate } from '~/utils/errors'

export default defineEventHandler(async (event) => {
  try {
    const tableId = getRouterParam(event, 'id')

    if(!tableId) {
      throw new Error('No table ID provided')
    }

    return await proxyRequest(event, `${useRuntimeConfig().public.prodDomain}/v1/tables/${tableId}/upload`, {
      headers: {
        // inject/override headers here (e.g. internal auth token)
      }
    })
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
