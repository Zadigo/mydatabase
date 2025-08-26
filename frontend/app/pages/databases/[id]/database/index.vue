<template>
  <section id="database-schema" class="bg-slate-50">
    <div class="tables-wrapper w-full h-screen z-50 relative">
      <div id="table" ref="tableEl" class="bg-white shadow-sm w-50 rounde-md rounded-md border-slate-100" :style="style" style="position: fixed">
        <div class="bg-slate-300 p-2 rounded-t-md font-bold">
          <icon name="i-lucide-table" />
          Table name
        </div>

        <ul class="cursor-move">
          <li v-for="i in 5" :key="i" class="p-2 not-last:border-b border-slate-100 text-sm space-y-2 flex justify-between items-center">
            <div class="space-x-2">
              <span>Column {{ i }}</span>
            </div>

            <div class="text-slate-500">
              <icon name="i-lucide-a-large-small text-md" />
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * TODO: Page is in Bêta mode and needs work
 */

definePageMeta({
  title: 'Database: Schema',
  layout: 'details'
})

const tableEl = useTemplateRef('tableEl')

const { style } = useDraggable(tableEl, {
  initialValue: { x: 800, y: 200 },
})

</script>
