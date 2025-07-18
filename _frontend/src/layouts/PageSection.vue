<template>
  <section :id="sectionId">
    <div class="container">
      <div class="row">
        <div class="col-md-10 col-sm-12 offset-md-1">
          <h1 class="h2 mb-4">{{ pageTitle }}</h1>
          <slot></slot>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    sectionId: {
      type: String,
      required: true
    },
    pageTitle: {
      type: String,
      required: true
    }
  }
}
</script>
