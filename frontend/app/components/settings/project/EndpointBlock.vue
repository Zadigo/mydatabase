<template>
  <nuxt-card>
    <nuxt-button variant="subtle" color="error" icon="i-lucide-trash" />

    <div class="space-y-2">
      <nuxt-input v-model="editableEndpoint.endpoint" class="w-full" />

      <nuxt-button-group class="w-full">
        <nuxt-input v-model="editableEndpoint.endpoint_uuid" class="w-full" variant="subtle" :disabled="true" />

        <nuxt-tooltip text="Copy to clipboard">
          <nuxt-button color="neutral" variant="subtle" icon="i-lucide-clipboard" @click="proxyCopy(editableEndpoint.endpoint_uuid)" />
        </nuxt-tooltip>
      </nuxt-button-group>

      <div v-for="method in editableEndpoint.methods" :key="method" class="p-3 rounded-lg bg-slate-50 border border-slate-100">
        <div class="pb-3 space-x-3">
          <span class="font-bold">{{ method }}</span>
          <span v-if="currentDatabase" class="font-light">{{ endpointString }}</span>
          <nuxt-skeleton v-else class="w-30 h-5" />
          <!-- <nuxt-button icon="i-lucide-copy" variant="subtle" size="sm" @click="proxyCopy(`/api/public/{{ editableEndpoint.endpoint }}/{{ currentDatabase.name }}`)" /> -->
        </div>
        <nuxt-switch v-model="selectedMethods[method]" />
      </div>
    </div>
  </nuxt-card>
</template>

<script setup lang="ts">
import type { DatabaseEndpoint } from '~/types'

const props = defineProps<{ endpoint: DatabaseEndpoint }>()

const editableEndpoint = ref({ ...props.endpoint })

const databaseStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(databaseStore)

/**
 * Copy
 */

function proxyCopy(value: string) {
  const { copy } = useClipboard({ source: value })
  copy()
}

/**
 * Toggles
 */

const selectedMethods = ref<{ [K in DatabaseEndpoint['methods'][number]]: boolean }>(
  props.endpoint.methods.reduce((acc, method) => {
    acc[method] = true
    return acc
  }, {} as { [K in DatabaseEndpoint['methods'][number]]: boolean })
)

/**
 * Utils
 */

const endpointString = computed(() => {
  if (isDefined(currentDatabase)) {
    return `/v1/endpoints/public/${currentDatabase.value.id}/table/{{table id}}/${editableEndpoint.value.endpoint}`
  } else {
    return undefined
  }
})
</script>
