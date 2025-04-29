<template>
  <section id="authentication">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <base-button color="primary" size="lg" @click="handleAuthToken">
            Connect your account
          </base-button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import { useGoogleAuthentication } from '../composables/google'
import { useGoogle } from '../store/google'
import { googleSheetApi } from '../plugins/google_api'

import BaseButton from '../layouts/bootstrap/buttons/BaseButton.vue'

export default {
  name: 'GoogleAuthView',
  components: {
    BaseButton
  },
  beforeRouteEnter (to, from, next) {
    console.log(to)
    next()
  },
  setup () {
    // const { getOAuthToken } = useGoogleAuthentication()
    const googleAuthStore = useGoogle()
    return {
      googleSheetApi,

      googleAuthStore,
      // getOAuthToken
    }
  },
  methods: {
    handleAuthToken () {
      try {
        this.googleSheetApi()
        // this.getOAuthToken()
        // this.$router.push({ name: 'connections_view' })
      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>
