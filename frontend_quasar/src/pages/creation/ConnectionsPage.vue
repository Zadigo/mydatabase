<template>
  <q-page padding>
    <div class="row">
      <h1 class="text-h3">Connections</h1>
    </div>

    <div class="row">
      <!-- <q-banner class="bg-warning text-white q-mb-md" rounded>
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Praesentium nulla vitae laborum nam inventore architecto rem sunt cupiditate dolore, aperiam facilis commodi nesciunt expedita vero consequatur voluptates velit exercitationem amet.
        <template v-slot:action>
          <q-btn flat color="white" label="Dismiss" />
          <q-btn flat color="white" label="Update Credit Card" />
        </template>
      </q-banner> -->

      <q-card style="width: 100%;">
        <q-card-section>
          <div class="flex justify-end">
            <q-btn class="q-mr-md" color="secondary" unelevated rounded @click="showApiModal = true">
              <q-icon name="fas fa-link" class="q-mr-md" size="1em"></q-icon>
              Use an API
            </q-btn>

            <q-btn color="primary" unelevated rounded @click="() => { isFileUpload = true, showApiModal = true }">
              <q-icon name="fas fa-upload" class="q-mr-md" size="1em"></q-icon>
              Upload file
            </q-btn>
          </div>
        </q-card-section>

        <q-card-section>
          <q-list bordered separator>
            <q-item v-for="dataSource in dataSources" :key="dataSource.sheet_id" class="q-pa-md">
              <q-item-section avatar>
                <q-icon v-if="dataSource.csv_base" name="fas fa-file-csv" />
                <q-icon v-else name="fas fa-link" />
              </q-item-section>

              <q-item-section>
                <q-item-label>{{ dataSource.name }}</q-item-label>
                <q-item-label caption lines="1">Label</q-item-label>
              </q-item-section>

              <q-item-section side>
                <q-btn round flat>
                  <q-icon name="fas fa-ellipsis-vertical"></q-icon>

                  <q-menu transition-show="scale" transition-hide="scale">
                    <q-list style="min-width: 150px;">
                      <q-item v-for="item in connectionMenuItems" :key="item" v-close-popup clickable @click="handleMenuActions(item, dataSource)">
                        <q-item-section class="text-center">
                          <q-icon :name="item.icon" size="1em"></q-icon>
                        </q-item-section>

                        <q-item-section>
                          {{ item.name }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <!-- Modals -->
    <q-dialog id="modal-file-upload" v-model="showApiModal" persistent @hide="() => { isFileUpload = false }">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">New data source</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <form @submit.prevent>
            <q-input v-model="requestData.name" class="q-mb-md" placeholder="Name" standout="bg-grey-1" clearable></q-input>

            <q-file v-if="isFileUpload" v-model="requestData.csv_file" accept=".csv" class="q-mb-md" placeholder="Select a csv file" standout="bg-grey-1" counter clearable>
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
            <q-input v-else v-model="requestData.endpoint_url" class="q-mb-md" type="url" placeholder="Url" standout="bg-grey-1" clearable></q-input>

            <q-input v-if="!isFileUpload" v-model="requestData.endpoint_data_key" class="q-mb-md" placeholder="Column name" standout="bg-grey-1" clearable></q-input>
            <q-select v-model="requestData.columns" placeholder="Columns" standout="bg-grey-1" use-input new-value-mode="add" multiple use-chips clearable></q-select>
          </form>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn v-close-popup color="primary" flat label="Cancel" />
          <q-btn color="primary" label="Save" @click="handleDataUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog id="modal-column-settings" v-model="showUpdateColumnTypesModal">
      <q-card style="width: 400px;">
        <q-card-section>
          <div v-for="(column, i) in columnUpdateRequestData" :key="i" class="row">
            <div class="col-12 flex justify-start q-mb-sm">
              <q-input v-model="column.column" class="q-mr-sm" outlined></q-input>
              <q-select v-model="column.type" :options="columnTypes" outlined></q-select>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat>Cancel</q-btn>
          <q-btn color="primary" flat @click="requestUpdateColumnTypes">Save</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import _ from 'lodash'
import columnTypes from '../../data/column_types.json'
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia'
import { useDataSources } from '../../stores/connections'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'ConnectionPage',
  setup () {
    const notifications = useQuasar()

    const showApiModal = ref(false)

    const dataSourcesStore = useDataSources()
    const { dataSources } = storeToRefs(dataSourcesStore)
    const currentUpdatedDataSource = ref({})
    const showUpdateColumnTypesModal = ref(false)

    const requestData = ref({
      name: null,
      endpoint_url: null,
      endpoint_data_key: null,
      columns: [] // TODO: Rename - Columns to keep in the data source
    })

    const columnUpdateRequestData = ref([])

    const isFileUpload = ref(false)

    return {
      notifications,
      isFileUpload,
      showApiModal,
      requestData,
      dataSources,
      columnTypes,
      columnUpdateRequestData,
      currentUpdatedDataSource,
      showUpdateColumnTypesModal,
      dataSourcesStore,
      connectionMenuItems: [
        {
          name: 'Columns',
          icon: 'fas fa-table'
        },
        {
          name: 'Refresh',
          icon: 'fas fa-refresh'
        }, 
        {
          name: 'Delete',
          icon: 'fas fa-trash'
        }
      ]
    }
  },
  created () {
    this.requestConnections()
  },
  methods: {
    async requestConnections () {
      // Returns the list of available data sources
      // for the given user
      try {
        const response = await this.$api.get('/sheets')
        this.dataSourcesStore.$patch((state) => {
          state.dataSources = response.data
          this.$session.create('data_sources', response.data)
        })
      } catch (error) {
        // Pass
      }
    },
    async handleDataUpload () {
      // Use this function to upload a new
      // data source to the backend
      // let response
      try {
        let response

        if (this.isFileUpload) {
          const data = new FormData()
          _.forEach(Object.keys(this.requestData), (key) => {
            data.append(key, this.requestData[key])
          })
          response = await this.$api.post('/sheets/upload', data, {
            headers: {
              'Content-Type': 'multipart/form-data',
            }
          })
        } else {
          response = await this.$api.post('/sheets/upload', this.requestData)
        }
        this.dataSources.push(response.data)
        this.showApiModal = false

        this.requestData = {
          name: null,
          csv_file: null,
          endpoint_url: null,
          endpoint_data_key: null,
          columns: []
        }
        
        this.notifications.notify({
          message: 'Data created',
          color: 'green-4',
          position: 'top',
          timeout: 1000,
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Data source could not be created',
          caption: error,
          color: 'red-4',
          position: 'top',
          timeout: 1000
        })
        this.showApiModal = false
      }
    },
    async handleRemoveConnection (id) {
      // Handles the deleting of a data source
      try {
        const response = await this.$api.post(`sheets/${id}/remove`)
        this.dataSourcesStore.dataSources = response.data

        this.notifications.notify({
          message: 'Connection removed successfully',
          color: 'green-4',
          position: 'top',
          timeout: 1000
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Could not remove data source',
          color: 'red-4',
          position: 'top',
          timeout: 1000
        })
      }
    },
    async handleRefreshConnection (id) {
      // Handles the refreshing of a data source
      try {
        const response = await this.$api.get(`sheets/${id}`)
        this.$session.dictSet('sources', id, response.data)

        this.notifications.notify({
          message: 'Connection refreshed successfully',
          color: 'green-4',
          position: 'top',
          timeout: 1000
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Could not refresh data source',
          color: 'red-4',
          position: 'top',
          timeout: 1000
        })
      }
    },
    async requestUpdateColumnTypes () {},
    handleUpdateColumnTypes (dataSource) {
      // Handles showing the modal for updating
      // the column types for the data source
      this.currentUpdatedDataSource = dataSource
      this.columnUpdateRequestData = dataSource.column_types
      this.showUpdateColumnTypesModal = true
    },
    handleMenuActions (action, dataSource) {
      // Handle actions such as re-updating the
      // data from the source, deletion
      switch (action.name) {
        case 'Delete':
          this.handleRemoveConnection(dataSource.sheet_id)
          break

        case 'Columns':
          this.handleUpdateColumnTypes(dataSource)
          break

        case 'Refresh':
          this.handleRefreshConnection(dataSource.sheet_id)
          break

        default:
          break
      }
    }
  }
})
</script>
