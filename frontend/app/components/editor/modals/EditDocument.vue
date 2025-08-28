<template>
  <nuxt-drawer v-model:open="show" class="min-w-100" direction="right" :handle="false" hande-only>
    <template #title>
      Edit document
    </template>

    <template #body>
      <div v-for="tableDocument in tableDocuments" :key="tableDocument.id" class="p-5 rounded-md bg-info-50">
        <div class="flex justify-between items-center">
          <p class="font-bold">
            <icon name="i-solid-csv" /> Document
          </p>

          <nuxt-button-group>
            <nuxt-button color="neutral" variant="subtle" @click="() => { remove(tableDocument) }">
              <icon name="i-lucide-trash" />
            </nuxt-button>

            <nuxt-dropdown-menu :items="dropdownItems">
              <nuxt-button color="neutral" variant="outline" icon="i-lucide-chevron-down" />
            </nuxt-dropdown-menu>
          </nuxt-button-group>
        </div>

        <p class="font-light text-sm">{{ tableDocument.name || tableDocument.document_uuid }}</p>

        <div class="p-1 bg-gray-100 my-5">
          <div class="flex justify-center gap-3 items-center cursor-pointer rounded-md border border-gray-200 hover:bg-gray-100 p-2">
            <icon name="i-lucide-key" />
            <nuxt-select placeholder="Primary key" />
            <icon name="i-lucide-arrow-right" />
            <nuxt-select placeholder="Foreign key" />
          </div>
        </div>
      </div>
    </template>
  </nuxt-drawer>
</template>

<script setup lang="ts">
import { table } from '#build/ui';
import type { DropdownMenuItem } from '@nuxt/ui'
import type { TableDocument } from '~/types'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'udpate:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

const tableEditionStore = useTableEditionStore()
const { tableDocuments } = storeToRefs(tableEditionStore)

const dropdownItems: DropdownMenuItem[] = [
  {
    label: 'Merge versions',
    icon: 'i-lucide-git-merge',
    onSelect (e) {
      // Handle merge versions
      console.log(e)
    }
  },
  {
    label: 'Versions',
    icon: 'i-lucide-user-plus',
    children: [
      {
        label: 'New version',
        icon: 'i-lucide-git-pull-request-create'
      },
      {
        label: 'Compare version',
        icon: 'i-lucide-git-compare-arrows'
      },
      {
        label: 'Delete version',
        icon: 'i-lucide-git-pull-request-closed'
      }
    ]
  },
  {
    label: 'Transfer ownership',
    icon: 'i-lucide-hard-drive-upload'
  },
  {
    label: 'Lock file',
    icon: 'i-lucide-file-lock'
  }
]

/**
 * Edit document
 */
 
/**
 * Composable used to edit a document
 */
function useDocumentEditionStore() {
  const config = useRuntimeConfig()

  const tableEditionStore = useTableEditionStore()
  const { tableDocuments } = storeToRefs(tableEditionStore)

  async function remove (tableDocument: TableDocument) {
    const { status } = await useFetch(`/v1/documents/${tableDocument.document_uuid}`, { 
      baseURL: config.public.prodDomain,
      method: 'DELETE'
    })

    if (status.value === 'success') {
      tableDocuments.value = tableDocuments.value.filter(doc => doc.id !== tableDocument.id)
    }
  }

  return {
    /**
     * Remove a document from a table
     */
    remove
  }
}

const { remove } = useDocumentEditionStore()
</script>
