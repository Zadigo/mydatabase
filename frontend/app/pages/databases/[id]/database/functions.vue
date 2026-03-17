<template>
  <section id="database-functions" class="mx-auto">
    <!-- Header -->
    <base-page-card-header v-model="search" placeholder="Search functions" title="Database functions" @create="create" />

    <div class="space-y-2">
      <database-functions-card v-for="(item, idx) in searched" :key="idx" :database-function="item" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useDatabaseFunctions } from '~/composables/use/databases/functions'

definePageMeta({
  label: 'Database: Functions',
  layout: 'details'

})

/**
 * Creation
 */

const { search, searched, create } = useDatabaseFunctions()
</script>
