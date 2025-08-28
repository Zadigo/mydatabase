<template>
  <section id="presentation" class="text-blue-900">
    <div class="grid grid-cols-12">
      <div class="col-span-12 p-8 bg-blue-200 rounded-b-4xl">
        <h2 class="font-bold text-3xl text-blue-900">Presentation</h2>
        <p class="mt-5">Lorem ipsum dolor sit amet consectetur adipisicing elit. Quibusdam natus nisi nemo ullam pariatur numquam ex esse ratione, soluta obcaecati quo. Iusto nisi aliquam soluta magni nemo, sit rem vero?</p>
      </div>
    </div>

    <grid class="col-span-12">
      <div class="py-5">
        <nuxt-button @click="() => { prev() }">Previous Table</nuxt-button>
        <nuxt-button @click="() => { next() }">Next Table</nuxt-button>
  
        {{ state }}
      </div>
    </grid>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Home page',
  layout: 'presentation'
})

const { css } = useStyleTag('body { background-color: var(--color-blue-50); }')

const tables = [1, 2 , 3]
const { next, prev, state } = useCycleList(tables)


// const someRef = ref<Record<string, string>>({ a: 'google' })

// function usePresentation<T>(passedRef: Ref<T>) {
//   const passedRefTwo = reactivePick(passedRef.value, ['a'])

//   return {
//     passedRef,
//     passedRefTwo
//   }
// }

// const { passedRefTwo  } = usePresentation(someRef)
</script>
