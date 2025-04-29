import { defineStore } from 'pinia';

const useGoogle = defineStore('google', {
  state: () => ({
    oAuthToken: {
      access_token: null,
      id_token: null,
      expires_in: null,
      refresh_token: null,
      token_type: null,
      scope: null
    },
    user: {
      id: null,
      email: null,
      verified_email: null,
      name: null,
      given_name: null,
      family_name: null,
      picture: null,
      locale: null,
    }
  }),
  actions: {
    setOAuthToken (data) {
      Object.keys(this.oAuthToken).forEach((key) => {
        this.oAuthToken[key] = data[key]
      })
    }
  },
  getters: {
    isAuthenticated () {
      // const truthArray = Object.keys(this.oAuthToken).map((key) => {
      //   return this.oAuthToken[key] !== null
      // })
      // return truthArray.every(x => x === true)
      return false
    }
  }
})

export {
  useGoogle
}
