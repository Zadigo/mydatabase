<template>
  <nuxt-card>
    <nuxt-button variant="subtle" color="error" icon="i-lucide-trash" />

    <form class="space-y-2" @submit.prevent>
      <div class="flex justify-around items-center gap-2 my-5">
        <!-- Name -->
        <nuxt-input v-model="editableEndpoint.endpoint" label="Endpoint Name" class="w-full" />

        <!-- UUID -->
        <nuxt-input v-model="editableEndpoint.endpoint_uuid" class="w-full" variant="subtle" :disabled="true" />
  
        <nuxt-tooltip text="Copy to clipboard">
          <nuxt-button color="neutral" variant="subtle" icon="i-lucide-clipboard" @click="proxyCopy(editableEndpoint.endpoint_uuid)" />
        </nuxt-tooltip>
      </div>

      <div class="flex gap-2 my-3">
        <nuxt-button icon="i-lucide-arrow-down" @click="() => { toggleShowMore() }">
          More
        </nuxt-button>
  
        <nuxt-button @click="() => { toggleShowMore() }">
          Disable
        </nuxt-button>
      </div>

      <template v-if="showMore">
        <div v-for="method in editableEndpoint.methods" :key="method" class="p-3 rounded-lg bg-slate-50 border border-slate-100 dark:bg-slate-800 dark:border-slate-700">
          <div class="pb-3 space-x-3">
            <span class="font-bold">{{ method }}</span>
            <span v-if="currentDatabase" class="font-light">{{ endpointString }}</span>
            <nuxt-skeleton v-else class="w-30 h-5" />
          </div>
          
          <nuxt-switch v-model="methodToggles[method]" />
        </div>
      </template>
    </form>
  </nuxt-card>
</template>

<script setup lang="ts">
import type { DatabaseEndpoint } from '#shared/types'

const props = defineProps<{ endpoint: DatabaseEndpoint }>()

const editableEndpoint = ref({ ...props.endpoint })

const { currentDatabase } = _useDatabases() 

/**
 * Toggle
 */

const [showMore, toggleShowMore] = useToggle()

/**
 * Copy
 */

const proxyCopy = (value: string) => {
  const { copy } = useClipboard({ source: value })
  copy()
}

/**
 * Toggles
 */

const methodToggles = ref<{ [K in DatabaseEndpoint['methods'][number]]: boolean }>(
  props.endpoint.methods.reduce((acc, method) => {
    acc[method] = true
    return acc
  }, {} as { [K in DatabaseEndpoint['methods'][number]]: boolean })
)

const selectedMethods = computed(() => {
  return Object.entries(methodToggles.value)
    .filter(([_, isSelected]) => isSelected)
    .map(([method]) => method)
})

/**
 * Utils
 */

const endpointString = computed(() => {
  if (isDefined(currentDatabase)) {
    return `/v1/endpoints/public/${currentDatabase.value.id}/table/{{table id}}/${editableEndpoint.value.endpoint_uuid}`
  } else {
    return undefined
  }
})

watchDebounced([() => editableEndpoint.value.endpoint, selectedMethods], async ([newEndpoint, newSelectedMethods]) => {
  if (currentDatabase.value) {
    await $fetch(`/api/databases/${currentDatabase.value.id}/endpoints`, {
      method: 'PUT',
      body: {
        endpoint: newEndpoint,
        methods: toValue(newSelectedMethods)
      }
    })
  }
}, {
  debounce: 1000
})
</script>
