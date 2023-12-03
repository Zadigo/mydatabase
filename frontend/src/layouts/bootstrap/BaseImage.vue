<template>
  <figure v-if="isFigure" class="figure">
    <img :src="src" :alt="alt" :class="imageClasses" class="figure-img img-fluid rounded">
    <figcaption class="figure-caption">{{ figCaption }}</figcaption>
  </figure>

  <img v-else :src="src" :class="imageClasses" :alt="alt" class="img-fluid">
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      required: true
    },
    alt: {
      type: String,
      required: false
    },
    rounded: {
      type: Boolean,
      default: false
    },
    floatStart: {
      type: Boolean,
      default: false
    },
    floatEnd: {
      type: Boolean,
      default: false
    },
    circle: {
      type: Boolean,
      default: false
    },
    thumbnail: {
      type: Boolean,
      default: false
    },
    isFigure: {
      type: Boolean,
      default: false
    },
    figCaption: {
      type: String,
      required: false
    },
    figCaptionPosition: {
      type: String,
      default: null
    }
  },
  computed: {
    imageClasses () {
      return [
        {
          rounded: this.rounded,
          'float-start': this.floatStart,
          'float-end': this.floatEnd,
          'img-thumbnail': this.thumbnail,
          'rounded-circle': this.circle,
          [`text-${this.figCaptionPosition}`]: this.figCaptionPosition !== null
        }
      ]
    }
  }
}
</script>
