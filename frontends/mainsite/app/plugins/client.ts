
export default defineNuxtPlugin(async (_nuxtApp) => {
  // const access = useCookie('access')
  // const refresh = useCookie('refresh')

  // const client = $fetch.create({
  //   baseURL: useRuntimeConfig().public.prodDomain,
  //   onRequest({ options }) {
  //     options.headers.set('Content-Type', 'application/json')

  //     if (access.value) {
  //       options.headers.set('Authorization', `Token ${access.value}`)
  //     }
  //   },
  //   async onResponseError({ response }) {
  //     if (response.status === 401) {
  //       access.value = null

  //       if (refresh.value) {
  //         const { access: newAccess } = await refreshAccessToken(refresh.value)
  //         access.value = newAccess
  //       } else {
  //         refresh.value = null
  //         await nuxtApp.runWithContext(() => navigateTo('/'))
  //       }
  //     }
  //   }
  // })

  return {
    provide: {
      // client
    }
  }
})
