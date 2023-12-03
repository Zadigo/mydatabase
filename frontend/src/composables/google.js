import axios from 'axios'
import qs from 'qs'
import { useGoogle } from '@/store/google'

const authClient = axios.create({
  baseURL: 'https://oauth2.googleapis.com',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  timeout: 10000
  // withCredentials: true
})

export function useGoogleAuthentication () {
  const baseUrl = 'https://accounts.google.com/o/oauth2/v2/auth'

  const scope = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
  ]

  function getOptions () {
    const options = {
      redirect_uri: 'http://localhost:8080/rest/oauth2-credential/callback',
      client_id: '818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
      access_type: 'offline',
      response_type: 'code',
      prompt: 'consent',
      scope: scope.join(' ')
    }
    return new URLSearchParams(options)
  }

  function getAuthenticationUrl () {
    const query = getOptions()
    return `${baseUrl}?${query.toString()}`
  }

  function authenticate () {
    // Opens the OAuth slash screen
    const url = getAuthenticationUrl()
    window.location = url
  }

  function connectionsAPI () {
    const client = axios.create({
      baseURL: 'http://127.0.0.1:8000/connections/api/',
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000
    })
    return client
  }

  async function getOAuthToken () {
    // Gets the Google Authentication Token
    try {
      const response = await connectionsAPI().post('/decode', { url: window.location.href })
      const options = {
        // code: '4/0AfJohXl2WTUThWQY72kxyAR4sjNYMfICOs0ofPXJlcfuSq3oBhg2dV0ypqLg77CtXr6rrw',
        code: response.data.code,
        client_id: '818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
        client_secret: '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',
        redirect_uri: 'http://localhost:8080/rest/oauth2-credential/callback',
        grant_type: 'authorization_code',
      }
      const { data } = await authClient.post('/token', qs.stringify(options))

      const store = useGoogle()
      store.oAuthToken = data
    } catch (e) {
      console.error(e)
    }
  }

  async function getGoogleUser (accessToken, idToken) {
    try {
      const options = {
        alt: 'json',
        access_token: `${accessToken}`
      }
      const query = new URLSearchParams(options)
      const { data } = await axios({
        method: 'post',
        baseURL: `https://www.googleapis.com/oauth2/v1/userinfo?${query.toString()}`,
        timeout: 1000,
        headers: {
          Authorization: `Bearer ${idToken}`,
        }
      })
      data
    } catch (e) {
      console.error(e)
    }
  }

  return {
    scope,
    authenticate,
    getAuthenticationUrl,
    getOAuthToken,
    getGoogleUser
  }
}

export function useGoogleSheets () {
  async function getSheets () {
    return null
  }
  return {
    getSheets
  }
}
