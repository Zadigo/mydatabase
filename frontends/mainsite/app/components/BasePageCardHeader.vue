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
            {{ actionName }}
          </nuxt-button>
        </slot>
      </div>
    </slot>
  </nuxt-card>
</template>

<script setup lang="ts">
const { title, placeholder, actionName = 'Create function' } = defineProps<{ title: string, placeholder: string, actionName?: string }>()
const emit = defineEmits<{ create: [] }>()

const search = defineModel({ type: String, default: '', required: false })
</script>
