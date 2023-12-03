<doc>
  Base structure to create a Bootstrap dropdown button
</doc>

<template>
  <div class="dropdown">
    <base-button :id="id" :size="size" :color="color" :shadow="shadow" :aria-expanded="show" class="dropdown-toggle" type="button" @click="show = !show">
      {{ linkName }}
    </base-button>
    
    <!-- <base-drop-menu :show="show" @click:dropdown-item="show = !show" /> -->
    <slot :show="show"></slot>
  </div>
</template>

<script>
import { useClickOutside } from '../composables'

import BaseButton from './BaseButton.vue'

export default {
  name: 'BaseDropdownButton',
  components: {
    BaseButton
  },
  props: {
    id: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: 'primary'
    },
    size: {
      type: String,
      default: 'md'
    },
    linkName: {
      type: String,
      required: true
    },
    shadow: {
      type: Boolean
    }
  },
  setup () {
    const { show } = useClickOutside()
    return {
      show
    }
  }
}
</script>
