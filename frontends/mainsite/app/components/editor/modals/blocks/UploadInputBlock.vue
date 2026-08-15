<template>
  <div v-if="selectedDocumentParams" class="space-x-2 flex justify-between">
    <nuxt-button v-if="newDocument.merge" :variant="selectedDocumentParams.primary_key_file ? 'subtle' : 'ghost'" color="error" @click="() => { selectPrimaryKeyFile(selectedDocumentParams) }">
      <icon name="i-lucide-key" />
    </nuxt-button>

    <nuxt-input v-model="selectedDocumentParams.name" :disabled="newDocument.merge" type="text" placeholder="Document name" class="w-full" />
    <nuxt-input v-if="selectedDocumentParams.source_type === 'url'" v-model="selectedDocumentParams.url" :loading="true" type="url" placeholder="Url" class="w-full" />
    <nuxt-input v-else-if="selectedDocumentParams.source_type === 'file'" v-model="selectedDocumentParams.file" :loading="true" type="file" :accept="fileAccept(selectedDocumentParams)" placeholder="Url" class="w-full" />
    
    <nuxt-dropdown-menu :items="contentTypeItems(selectedDocumentParams)">
      <nuxt-button variant="subtle" @click="() => { selectIndex(idx) }">
        <icon name="i-lucide-ellipsis" />
      </nuxt-button>
    </nuxt-dropdown-menu>

    <nuxt-button variant="subtle" @click="() => { removeDocument(idx) }">
      <icon name="i-lucide-minus" />
    </nuxt-button>
  </div>
</template>

<script lang="ts" setup>
import type { DocumentParams } from '~/composables/use'
import type { DropdownMenuItem } from '@nuxt/ui'

const props = defineProps<{
  idx: number
}>()


const { newDocument, removeDocument, selectPrimaryKeyFile, getNewDocumentByIndex } = useCreateDocument()

const selectedDocumentParams = getNewDocumentByIndex(props.idx)

/**
 * Prefetch
 * @description Prefetch the headers of the documents to be able to select the columns
 */

const { selectedTable } = useTableEditionComposable()
const { prefetch } = usePrefetchProvider(selectedTable, newDocument)

watch(() => selectedDocumentParams?.url, (newValue) => {
  if (newValue) {
    void prefetch(selectedDocumentParams)
  }
}, { immediate: false })

/**
 * Inputs
 * @description Dynamicly set the file accept attribute based on the content type of the document
 */

function fileAccept(documentParams: DocumentParams) {
  if (documentParams.content_type == 'csv' || documentParams.content_type === 'json') {
    return `.${documentParams.content_type}`
  }
  return undefined
}

/**
 * Menu
 */

const selectedIndex = ref<number | undefined>()

const selectIndex = (index: number) => {
  selectedIndex.value = index
}

const setSourceType = (value: DocumentParams['source_type']) => {
  if (isDefined(selectedIndex)) {
    const item = newDocument.value.documents[selectedIndex.value]
    if (item) {
      item.source_type = value
    }
  }
}

function contentTypeItems(documentParams: DocumentParams): DropdownMenuItem[] {
  return [
    {
      label: 'Url',
      icon: 'i-lucide-link',
      active: documentParams.source_type === 'url',
      onSelect: (event) => {
        event.preventDefault()
        setSourceType('url')
      }
    },
    {
      label: 'File',
      icon: 'i-lucide-file',
      active: documentParams.source_type === 'file',
      disabled: documentParams.content_type === 'google_sheet',
      onSelect: (event) => {
        event.preventDefault()
        setSourceType('file')
      }
    }
  ]
}
</script>
