<template>
  <div class="p-1 rounded shadow-sm bg-primary-subtle">
    <v-btn color="secondary" variant="tonal" class="filter-block p-2" rounded @click="showFilterSettingsModal = true">
      <font-awesome-icon :icon="['fas', 'filter']" />
    </v-btn>
    
    <v-menu v-model="showFilterSettingsModal" :close-on-content-click="false" location="end">
      <v-card min-width="600">
        <div class="container my-3">
          <div class="row px-5">
            <v-select v-model="newFilterData.column" :items="currentConnection.columns" class="mb-1" variant="solo" hide-details></v-select>
            <v-select v-model="newFilterData.operator" :items="defaultFilters" class="mb-1" variant="solo" hide-details></v-select>
            <v-text-field v-model="newFilterData.value" variant="solo" hide-details />
          </div>
        </div>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import { ref } from 'vue'
import { mapState } from 'pinia'
import { useConnections } from '@/store/connections'
import { useColumnFilters } from '../../composables/page'

export default {
  name: 'ActiveFilter',
  props: {
    filterData: {
      type: Object,
      required: true
    }
  },
  setup () {
    const showFilterSettingsModal = ref(false)
    const filterRequestData = ref({})
    const { defaultFilters } = useColumnFilters()
    return {
      filterRequestData,
      showFilterSettingsModal,
      defaultFilters
    }
  },
  computed: {
    ...mapState(useConnections, ['currentConnection'])
  },
  beforeMount () {
    Object.assign(this.filterRequestData, this.filterData)
  }
}
</script>
