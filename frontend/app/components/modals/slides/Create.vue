<template>
  <NuxtModal v-model:open="show" modal>
    <template #title>
      <h2>New Slide</h2>
    </template>
    
    <template #body>
      <NuxtInput id="new-slide" v-model="slideName" type="text" class="w-full" placeholder="Name" @keypress.enter="create" />
      <NuxtSwitch v-model="isPrivate" class="my-2" label="Private slide" />
    </template>

    <template #footer>
      <NuxtButton @click="show=false">
        Cancel
      </NuxtButton>
      
      <NuxtButton @click="create">
        Validate
      </NuxtButton>
    </template>
  </NuxtModal>
</template>

<script setup lang="ts">
import { useCreateSlide } from '~/composables/slides'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [boolean] }>()
const show = useVModel(props, 'modelValue', emit)

const { slideName, isPrivate, create  } = useCreateSlide()
</script>
