<template>
  <div id="scheduling">
    <nuxt-card>
      <div class="space-y-4">
        <nuxt-select-menu v-model="newSchedule.datasource" :items="allTableDocuments" value-key="document_uuid" label-key="name" placeholder="Select a datasource" variant="subtle" class="w-full" />

        <div class="flex content-evenly gap-2">
          <nuxt-input v-model="newSchedule.interval" class="w-full" />
          <nuxt-select v-model="newSchedule.interval_unit" :items="Array.from(intervalUnits)" class="w-full" />
        </div>

        <nuxt-switch v-model="showCron" label="Use cron" />

        <div v-if="showCron" id="cron" class="space-y-2">
          <div class="flex content-evenly gap-2">
            <nuxt-input v-model="newSchedule.cron.hours" placeholder="hours" class="w-full" />
            <nuxt-input v-model="newSchedule.cron.minutes" placeholder="minutes" class="w-full" />
            <nuxt-input v-model="newSchedule.cron.seconds" placeholder="seconds" class="w-full" />
          </div>

          <div class="flex content-evenly gap-2">
            <nuxt-input v-model="newSchedule.cron.dayOfMonth" placeholder="Days of the month" class="w-full" />
            <nuxt-input v-model="newSchedule.cron.month" placeholder="Months of the year" class="w-full" />
            <nuxt-input v-model="newSchedule.cron.dayOfWeek" placeholder="Days of the week" class="w-full" />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-start">
          <nuxt-button>
            Save
          </nuxt-button>
        </div>
      </template>
    </nuxt-card>
  </div>
</template>

<script setup lang="ts">
const intervalUnits = ['Minute', 'Hour', 'Day', 'Week', 'Month', 'Year'] as const

type IntervalUnit = typeof intervalUnits[number]

interface NewSchedule {
  datasource: string
  interval: string
  interval_unit: IntervalUnit
  cron: {
    seconds: string
    minutes: string
    hours: string
    dayOfMonth: string
    month: string
    dayOfWeek: string
  }
}

const databaseStore = useDatabasesStore()
const { allTableDocuments } = storeToRefs(databaseStore)

const showCron = ref<boolean>(false)

/**
 * Create
 */

const newSchedule = reactive<NewSchedule>({
  datasource: null,
  interval: '',
  interval_unit: 'Day',
  cron: {
    seconds: '',
    minutes: '',
    hours: '',
    dayOfMonth: '',
    month: '',
    dayOfWeek: ''
  }
})
</script>
