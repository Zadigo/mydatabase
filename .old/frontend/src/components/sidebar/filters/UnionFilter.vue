<template>
  <div :id="`filter-${position}`" :class="{ 'mt-2': position > 0 }" class="row">
    <div class="col-12">
      <div v-if="isDataFilter" class="row">
        <div class="col-3">
          <v-select v-model="dataFilterRequestData.union" :items="defaultUnions" variant="outlined" placeholder="Union" clearable hide-details />
        </div>

        <div class="col-3">
          <v-autocomplete v-model="dataFilterRequestData.column" :items="currentConnection.columns" variant="outlined" placeholder="Column name" clearable hide-details />
        </div>

        <div class="col-3">
          <v-autocomplete v-model="dataFilterRequestData.operator" :items="defaultOperators" variant="outlined" placeholder="Operator" clearable hide-details />
        </div>

        <div class="col-3">
          <v-text-field v-model="dataFilterRequestData.value" variant="outlined" placeholder="Value" clearable hide-details />
        </div>
      </div>

      <div v-else class="row">
        <div class="col-3">
          <v-select v-model="userFilterRequestData.union" :items="defaultUnions" variant="outlined" placeholder="Union" clearable hide-details />
        </div>

        <div class="col-4">
          <v-autocomplete v-model="userFilterRequestData.column" :items="currentConnection.columns" variant="outlined" placeholder="Column name" clearable hide-details />
        </div>

        <div class="col-4">
          <v-autocomplete v-model="userFilterRequestData.operator" :items="defaultOperators" variant="outlined" placeholder="Operator" clearable hide-details />
        </div>userFilterRequestData

        <div class="col-4">
          <v-autocomplete v-model="userFilterRequestData.input_type" :items="defaultColumnInputs" variant="outlined" placeholder="Input type" clearable hide-details />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useConnections } from '@/store/connections'
import { useColumnFilters } from '@/composables/page'

export default {
  name: 'UnionFilter',
  props: {
    filterDetails: {
      type: Object,
      required: true
    },
    position: {
      type: Number,
      required: true
    },
    isDataFilter: {
      type: Boolean,
      default: false
    }
  },
  setup () {
    const { currentConnection } = useConnections()
    const { defaultOperators, defaultColumnInputs, defaultUnions } = useColumnFilters()
    const dataFilterRequestData = ref({
      column: null,
      operator: 'equals',
      value: null
    })
    const userFilterRequestData = ref({
      column: null,
      operator: 'equals',
      input_type: 'Input'
    })

    return {
      defaultOperators,
      defaultColumnInputs,
      dataFilterRequestData,
      userFilterRequestData,
      defaultUnions,
      currentConnection
    }
  },
  beforeMount () {
    if (this.isDataFilter) {
      Object.assign(this.dataFilterRequestData, this.filterDetails)
    } else {
      Object.assign(this.userFilterRequestData, this.filterDetails)
    }
  }
}
</script>
