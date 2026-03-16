<template>
  <div ref="devContainerEl" class="rounded-3xl fixed top-0 left-0 h-auto w-100 backdrop-blur-3xl bg-primary/50 z-50 overflow-y-scroll p-5 shadow-3xl space-y-2" :style="style">
    <nuxt-button variant="soft" color="neutral" @click="() => { reduceElements = !reduceElements }">
      Reduce
    </nuxt-button>
    
    <div v-show="!reduceElements" class="max-h-150 overflow-y-scroll">
      <p class="font-bold mt-5">
        Selected table
      </p>
  
      <pre class="h-50 w-full overflow-scroll rounded-3xl bg-gray-50/50">
        {{ selectedTable }}
      </pre>
      
      <p class="font-bold mt-5">
        Selected table document
      </p>
  
      <pre class="h-50 w-full overflow-scroll rounded-3xl bg-gray-50/50">
        {{ selectedTableDocument }}
      </pre>

      <p class="font-bold mt-5">
        Table documents
      </p>

      <pre class="h-50 w-full overflow-scroll rounded-3xl bg-gray-50/50">
        {{ tableDocuments }}
      </pre>
    </div>
  </div>
</template>

<script lang="ts" setup>
const devContainerEl = useTemplateRef('devContainerEl')
const { selectedTable, selectedTableDocument, tableDocuments } = storeToRefs(useTableEditionStore())
const { style } = useDraggable(devContainerEl, { initialValue: { x: 40, y: 0 }})

const reduceElements = ref(false)
</script>
