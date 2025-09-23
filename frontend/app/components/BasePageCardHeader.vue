<template>
  <nuxt-card>
    <div class="flex justify-between items-center">
      <h3 class="font-bold text-2xl">
        {{ title }}
      </h3>

      <nuxt-button size="sm" color="info" variant="outline">
        <icon name="i-lucide-book" />
        Documentation
      </nuxt-button>
    </div>

    <slot name="actions">
      <div class="flex justify-between mt-3">
        <nuxt-input v-model="search" :placeholder="placeholder" class="w-5/12" />

        <slot name="actionButton">
          <nuxt-button @click="emit('create')">
            <icon name="i-lucide-plus" />
            Create function
          </nuxt-button>
        </slot>
      </div>
    </slot>
  </nuxt-card>
</template>

<script setup lang="ts">
const props = defineProps<{ title: string, modelValue: string, placeholder: string }>()
const emit = defineEmits<{ 'update:modelValue': [string], create: [] }>()
const search = useVModel(props, 'modelValue', emit)
</script>
