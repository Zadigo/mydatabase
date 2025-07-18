<template>
  <section id="blocks">
    <NuxtCard class="ring-0 shadow-sm">
      <template #header>
        <h1 class="text-2xl font-bold">
          Slides
        </h1>
        
        <div class="flex items-center gap-2">
          <NuxtInput v-model="search" placeholder="Search slides..." />

          <NuxtButton @click="() => { toggle() }">
            <Icon name="i-fa-solid:plus" />
            Create slide
          </NuxtButton>
        </div>
      </template>
      
      <div class="space-y-2">
        <div v-for="slide in searched" :key="slide.id" class="py-2 px-5 bg-slate/40 rounded-md flex justify-between items-center">
          <NuxtLink :to="`slides/${slide.id}`">
            {{ slide.name }}
          </NuxtLink>

          <NuxtDropdownMenu arrow :items="actions">
            <NuxtButton icon="i-lucide-menu" color="neutral" variant="outline" />
          </NuxtDropdownMenu>
        </div>
      </div>
    </NuxtCard>

    <!-- Modals -->
    <ModalsSlidesCreate v-model="showCreationModal" />
  </section>
</template>

<script lang="ts" setup>
definePageMeta({
  layout: 'dashboard'
})

const [showCreationModal, toggle] = useToggle()

const actions = ref([
  { label: 'Edit', icon: 'i-lucide-edit-2', action: () => console.log('Edit') },
  { label: 'Delete', icon: 'i-lucide-trash-2', action: () => console.log('Delete') }
])

const { getSlides, searched, search } = useSlideStore()

onBeforeMount(async () => {
  await getSlides()
})
</script>
