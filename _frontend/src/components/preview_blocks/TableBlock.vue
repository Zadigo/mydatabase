<template>
  <base-card>
    <template #header>
      <div class="d-flex justify-content-between align-items-center">
        <div class="w-50">
          <v-text-field v-model="search" type="search" variant="solo" placeholder="Search" hide-details />
        </div>

        <v-btn v-if="details.allow_record_creation" id="cta-create-record" elevation="0" variant="tonal" color="primary" rounded @click="showCreateRecordModal = true">
          <font-awesome-icon :icon="['fas', 'plus']" class="me-2" />
          Create record
        </v-btn>
      </div>
    </template>

    <template #body>
      <v-table>
        <thead>
          <tr>
            <th v-for="column in visibleColumns" :key="column" class="fw-bold">
              {{ column.column }}
            </th>
          </tr>
        </thead>

        <tbody>
          <template v-for="item in searchedBlockData" :key="item.index">
            <tr>
              <td v-for="column in blockData.columns" :key="column">
                {{ item[column] }}
              </td>
            </tr>
          </template>
        </tbody>
      </v-table>

      <div class="mt-5 d-flex justify-content-end">
        <v-pagination v-model="currentPage" :length="4" prev-icon="mdi-menu-left" next-icon="mdi-menu-right"></v-pagination>
      </div>
    </template>

    <!-- Modals -->
    <v-dialog id="data-creation-modal" v-model="showCreateRecordModal" width="300">
      <v-card title="New record">
        <v-card-text>
          <v-text-field v-for="column in details.record_creation_fields" :key="column" v-model="newRecord[column]" :placeholder="column" variant="solo"></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-btn>Validate</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </base-card>
</template>

<script>
import _ from 'lodash'
import { ref } from 'vue'
import { usePublishedPages } from '@/store/published_pages'
import { useUtilities } from '@/composables/utils'

import BaseCard from '../../layouts/bootstrap/cards/BaseCard.vue'

export default {
  name: 'TableBlock',
  components: {
    BaseCard
  },
  props: {
    details: {
      type: Object,
      required: true
    }
  },
  emits: {
    'block-selected' () {
      return true
    }
  },
  setup () {
    const { listManager } = useUtilities()
    const publishedPages = usePublishedPages()
    const search = ref(null)
    const currentPage = ref(1)
    const showCreateRecordModal = ref(false)

    return {
      showCreateRecordModal,
      currentPage,
      search,
      listManager,
      publishedPages
    }
  },
  data () {
    return {
      blockData: {},
      newRecord: {}
    }
  },
  computed: {
    searchedBlockData () {
      if (this.search) {
        return _.filter(this.blockData.results, (item) => {
          const truthArray = this.blockData.columns.map((column) => {
            return item[column].includes(this.search) || item[column].toLowerCase().includes(this.search)
          })
          return truthArray.some(result => result === true)
        })
      } else {
        return this.blockData.results
      }
    },
    visibleColumns () {
      // return this.blockData.columns
      return _.filter(this.details.conditions.columns_visibility, ['visibility', true])
    }
  },
  beforeMount () {
    this.getData()
  },
  methods: {
    async getData () {
      try {
        const response = await this.$http.get(`sheets/${this.details.data_source}`)
        this.blockData = response.data
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
