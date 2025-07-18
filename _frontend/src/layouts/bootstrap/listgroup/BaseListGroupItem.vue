<template>
  <li :class="{ disabled }" :aria-disabled="disabled" class="list-group-item p-3">
    <slot></slot>
  </li>
</template>

<script>
export default {
  name: 'BaseListGroupItem',
  props: {
    disabled: {
      type: Boolean
    }
  }
}
</script>
