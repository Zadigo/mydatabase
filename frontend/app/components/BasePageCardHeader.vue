<template>
  <nuxt-card>
    <div class="flex justify-between">
      <h3 class="font-bold text-2xl">
        {{ title }}
      </h3>

      <nuxt-button variant="outline">
        <icon name="i-lucide-book" />
        Documentation
      </nuxt-button>
    </div>

    <div class="flex justify-between">
      <nuxt-input v-model="search" :placeholder="placeholder" />
      <nuxt-button>
        <icon name="i-lucide-plus" />
        Create function
      </nuxt-button>
    </div>
  </nuxt-card>
</template>

<script setup lang="ts">
const props = defineProps<{ title: string, modelValue: string, placeholder: string }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()
const search = useVModel(props, 'modelValue', emit)
</script>
