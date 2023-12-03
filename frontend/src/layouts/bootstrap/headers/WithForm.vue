<template>
  <section class="shadow-sm">
    <div class="container col-xl-10 col-xxl-8 px-4 py-5">
      <div class="row align-items-center g-lg-5 py-5">
        <div class="col-lg-7 text-center text-lg-start">
          <h1 class="display-4 fw-bold lh-1 text-body-emphasis mb-3">Vertically centered hero sign-up form</h1>
          <p class="col-lg-10 fs-4">Below is an example form built entirely with Bootstrap’s form controls. Each required form group has a validation state that can be triggered by attempting to submit the form without completing it.</p>
        </div>

        <div class="col-md-10 mx-auto col-lg-5">
          <form class="p-4 p-md-5 border rounded-3 bg-body-tertiary">
            <slot name="inputs">
              <base-input id="name" placeholder="Nom" class="p-3 mb-2" />
              <base-input id="name" input-type="email" placeholder="Email" class="p-3 mb-3" />
            </slot>
            
            <base-checkbox id="remember-me" label="Remember me" class="mb-3" />

            <button class="w-100 btn btn-lg btn-primary" type="submit">Sign up</button>
            <hr class="my-4">
            <small class="text-body-secondary">By clicking Sign up, you agree to the terms of use.</small>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import BaseCheckbox from '../BaseCheckbox.vue'
import BaseInput from '@/layouts/bootstrap/BaseInput.vue'
export default {
  name: 'WithForm',
  components: {
    BaseCheckbox,
    BaseInput
  },
  data () {
    return {
      
    }
  }
}
</script>
