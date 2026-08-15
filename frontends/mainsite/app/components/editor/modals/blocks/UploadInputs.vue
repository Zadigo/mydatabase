<template>
  <div class="space-y-3">
    <editor-modals-blocks-upload-input-block v-for="(_, idx) in newDocument.documents" :key="idx" :idx="idx" />

    <!-- <div v-for="(tableDocument, idx) in newDocument.documents" :key="idx" class="space-x-2 flex justify-between">
      <nuxt-button v-if="newDocument.merge" :variant="tableDocument.primary_key_file ? 'subtle' : 'ghost'" color="error" @click="() => { selectPrimaryKeyFile(tableDocument) }">
        <icon name="i-lucide-key" />
      </nuxt-button>
  
      <nuxt-input v-model="tableDocument.name" :disabled="newDocument.merge"  type="text" placeholder="Document name" class="w-full" />
      <nuxt-input v-if="tableDocument.source_type === 'url'" type="url" placeholder="Url" class="w-full" />
      <nuxt-input v-else-if="tableDocument.source_type === 'file'" type="file" :accept="fileAccept(tableDocument)" placeholder="Url" class="w-full" />
      
      <nuxt-dropdown-menu :items="contentTypeItems(idx, tableDocument)">
        <nuxt-button variant="subtle" @click="() => { selectIndex(idx) }">
          <icon name="i-lucide-ellipsis" />
        </nuxt-button>
      </nuxt-dropdown-menu>

      <nuxt-button variant="subtle" @click="() => { removeDocument(idx) }">
        <icon name="i-lucide-minus" />
      </nuxt-button>
    </div> -->
  </div>
</template>

<script lang="ts" setup>
import type { DocumentParams  } from '~/composables/use'
import type { DropdownMenuItem } from '@nuxt/ui'

const { newDocument, removeDocument, selectPrimaryKeyFile } = useCreateDocument()

/**
 * Dynamicly set the file accept attribute based on the content type of the document
 */

// function fileAccept(tableDocument: DocumentParams) {
//   if (tableDocument.content_type == 'csv' || tableDocument.content_type === 'json') {
//     return `.${tableDocument.content_type}`
//   }
//   return undefined
// }

/**
 * Menu
 */

// const selectedIndex = ref<number | undefined>()
 
// const selectIndex = (index: number) => {
//   selectedIndex.value = index
// }

// const setSourceType = (value: DocumentParams['source_type']) => {
//   if (isDefined(selectedIndex)) {
//     const item = newDocument.value.documents[selectedIndex.value]
//     if (item) {
//       item.source_type = value
//     }
//   }
// }
 
// function contentTypeItems(index: number, tableDocument: DocumentParams): DropdownMenuItem[] {
//   return [
//     {
//       label: 'Url',
//       icon: 'i-lucide-link',
//       active: tableDocument.source_type === 'url',
//       onSelect: (event) => {
//         event.preventDefault()
//         setSourceType('url')
//       }
//     },
//     {
//       label: 'File',
//       icon: 'i-lucide-file',
//       active: tableDocument.source_type === 'file',
//       disabled: tableDocument.content_type === 'google_sheet',
//       onSelect: (event) => {
//         event.preventDefault()
//         setSourceType('file')
//       }
//     }
//   ]
// }
</script>
