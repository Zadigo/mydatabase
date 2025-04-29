<template>
  <div class="px-4 py-5 my-5 text-center shadow-sm">
    <img class="d-block mx-auto mb-4" src="" alt="" width="72" height="57">
    <h1 class="display-5 fw-bold text-body-emphasis">{{ lead }}</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">{{ leadDescription }}</p>
      <slot name="cta">
        <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
          <base-button class="px-4 gap-3" size="lg">Primary</base-button>
          <base-button class="px-4" size="lg" outline>Secondary</base-button>
        </div>
      </slot>
    </div>
  </div>
</template>

<script>
import BaseButton from '../buttons/BaseButton.vue'

export default {
  name: 'CenteredHero',
  components: {
    BaseButton
  },
  props: {
    lead: {
      type: String,
      default: "Centered hero"
    },
    leadDescription: {
      type: String,
      default: "Quickly design and customize responsive mobile-first sites with Bootstrap, the world's most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins."
    }
  }
}
</script>
