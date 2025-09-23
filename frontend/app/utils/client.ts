import { useJwt } from '@vueuse/integrations/useJwt'
import type { Nullable, Refeable, Undefineable } from '~/types'

export interface LoginApiResponse {
  access: string
  refresh: string
}

export type TokenRefreshApiResponse = Omit<LoginApiResponse, 'refresh'>

/**
 * Helper function used to ask for a new access
 * token for the user
 */
export async function refreshAccessToken(refresh: string) {
  const response = await $fetch<TokenRefreshApiResponse>('/v1/auth/token/refresh/', {
    baseURL: useRuntimeConfig().public.prodDomain,
    method: 'POST',
    body: {
      refresh
    }
  })

  return {
    access: response.access
  }
}

/**
 * Composable used to login the user in the frontend 
 * @param email User email
 * @param password User password
 */
export async function useLogin<T extends LoginApiResponse>(email: Refeable<Undefineable<string>>, password: Refeable<Undefineable<string>>) {
  if (import.meta.server) {
    return {
      login: async () => {},
      failureCount: ref(0),
      access: '',
      refresh: '',
      isSuccess: ref(false)
    }
  }

  const { count: failureCount, inc } = useCounter(0)

  const _email = ref(email)
  const _password = ref(password)
  const credentials =  ref<Undefineable<T>>()

  async function login() {
    const data = await $fetch<T>('/v1/auth/token/', {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'POST',
      body: {
        username: _email.value,
        password: _password.value
      },
      onRequestError() {
        inc()
      }
    })

    if (data) {
      credentials.value = data
    }
  }

  const isSuccess = computed(() => isDefined(credentials))

  return {
    login,
    /**
     * Number of failed login attempts
     * @default 0
     */
    failureCount,
    /**
     * Access token used in the Authorization header
     */
    access: credentials.value?.access,
    /**
     * Refresh token used to get a new access token
     */
    refresh: credentials.value?.refresh,
    /**
     * Whether the login was successful
     * @default false
     */
    isSuccess
  }
}

/**
 * Composable that parses the JWT token returned
 * from the backend and contains information on the
 * user's profile
 */
export const useProfile = createSharedComposable(() => {
  if (import.meta.server) {
    return {
      userId: ref<Nullable<number>>(null),
      payload: ref(null)
    }
  }

  const access = refDefault(useCookie('access'), '')
  console.log('Access token:', access.value)

  const { payload } = useJwt(access)
  const userId = computed(() => payload['user_id'])

  return {
    payload,
    /**
     * User ID parsed from the JWT token
     * or null if the user is not logged in
     * @default ""
     */
    userId
  }
})

/**
 * Function that logs out the user by
 * deleting the access and refresh tokens
 * from the cookies
 * @param callback Optional callback to be executed after logout
 */
export async function logout(callback?: () => void) {
  if (import.meta.server) {
    return
  }

  const accessToken = useCookie('access')
  const refreshToken = useCookie('refresh')

  accessToken.value = null
  refreshToken.value = null

  if (callback) {
    callback()
  }
}
