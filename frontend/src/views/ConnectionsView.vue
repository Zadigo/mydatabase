<template>
  <page-section page-title="Connections" section-id="connections">
    <div v-if="!googleStore.isAuthenticated" class="alert alert-warning">
      <div class="p-2">
        <p>Connect to your Google account</p>
        <!-- <v-btn color="info" rounded @click="authenticate">
          <font-awesome-icon :icon="['fas', 'link']" class="me-2" />
          Connect to Google
        </v-btn> -->
      </div>
      
    </div>
    
    <!-- Connections -->
    <base-card class="shadow-sm">
      <template #header>
        <div class="d-flex justify-content-end align-items-center p-2">
          <!-- <v-btn class="me-2" variant="tonal" color="info" rounded @click="handleNewSpreadsheet">
            <font-awesome-icon :icon="['fas', 'plus']" class="me-2" />
            Add Google Sheet
          </v-btn> -->

          <v-btn variant="tonal" color="info" rounded @click="showCsvSettings = true">
            <font-awesome-icon :icon="['fas', 'file-csv']" class="me-2" />
            Upload csv
          </v-btn>
        </div>
      </template>

      <template #body>
        <base-list-group>
          <base-list-group-item v-for="connection in connections" :key="connection.id" class="d-flex justify-content-between align-items-center">
            <span>{{ connection.name }}</span>
            <span class="badge rounded-pill text-light text-bg-success">Public</span>

            <v-btn :id="`btn-connection-${connection.sheet_id}`" variant="text">
              <font-awesome-icon :icon="['fas', 'ellipsis-vertical']" />
            </v-btn>

            <v-menu :activator="`#btn-connection-${connection.sheet_id}`">
              <v-list>
                <v-list-item v-for="action in connectionMenuActions" :key="action" :value="action" @click="handleConnectionMenuAction(action, connection)">
                  <v-list-item-title>{{ action }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </base-list-group-item>
        </base-list-group>
      </template>
    </base-card> 
    
    <!-- Modals -->
    <teleport to="body">
      <v-dialog id="settings-modal" v-model="showSheetSettings" width="300">
        <v-card>
          <v-card-text>
            <div class="row">
              <div class="col-12">
                <h2 v-if="isCreation" class="h4 mb-3">New spreadsheet</h2>
                <h2 v-else class="h4 mb-3">Change spreadsheet</h2>
                <base-input id="new-spreadsheet" placeholder="Spread sheet url" class="p-3" />
              </div>
            </div>
          </v-card-text>
  
          <v-card-actions class="justify-content-end">
            <v-btn @click="showSheetSettings = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleSubmit">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>

    <teleport to="body">
      <v-dialog id="upload-csv-modal" v-model="showCreateConnectionModal" width="600">
        <v-card>
          <v-card-text>
            <div class="row">
              <div class="col-12">
                <h2 class="h4 mb-4">Create a new connection</h2>
              </div>
              
              <div class="col-12">
                <v-text-field v-model="requestData.name" class="mb-1" variant="outlined" label="Your connection's name" hide-details></v-text-field>

                <v-switch v-model="uploadChoice" label="Upload using a csv file" inset hide-details></v-switch>
                <v-file-input v-if="uploadChoice" v-model="requestData.csv_file" label="Choose a csv file" variant="solo" accept=".csv"></v-file-input>

                <div v-else>
                  <v-text-field v-model="requestData.endpoint_url" class="mb-2" type="url" variant="outlined" label="Add an API endpoint url" hide-details></v-text-field>
                  <v-text-field v-model="requestData.endpoint_data_key" variant="outlined" label="Choose the data entrypoint key" hide-details></v-text-field>
                </div>
                

                <!-- <v-switch v-model="cleanCSVFile" label="Clean data" inset></v-switch> -->
                <!-- <v-text-field v-if="cleanCSVFile" label="Columns to clean" variant="solo"></v-text-field> -->
                <!-- <v-switch label="Create Google sheet" inset></v-switch> -->
              </div>
            </div>
          </v-card-text>
  
          <v-card-actions class="justify-content-end">
            <v-btn @click="showCsvSettings = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleCreateConnection">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </page-section>
</template>

<script>
// import { useGoogleAuthentication } from '../composables/google'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useConnections } from '../store/connections'
import { useGoogle } from '../store/google'
import { useSheetsComposable } from '@/composables/page'

import BaseListGroup from '../layouts/bootstrap/listgroup/BaseListGroup.vue'
import BaseListGroupItem from '../layouts/bootstrap/listgroup/BaseListGroupItem.vue'
import BaseCard from '../layouts/bootstrap/cards/BaseCard.vue'
import BaseInput from '../layouts/bootstrap/BaseInput.vue'
import PageSection from '../layouts/PageSection.vue'

export default {
  name: 'ConnectionsView',
  components: {
    BaseCard,
    BaseListGroup,
    BaseListGroupItem,
    BaseInput,
    PageSection
  },
  setup () {
    const googleStore = useGoogle()
    const connectionsStore = useConnections()
    const { connections } = storeToRefs(connectionsStore)
    const { getConnections, getSheetData } = useSheetsComposable()
    const connectionMenuActions = ['Refresh', 'Remove']
    const isCreation = ref(false)
    const showSheetSettings = ref(false)
    const showCreateConnectionModal = ref(false)
    const uploadedFile = ref(null)
    const cleanCSVFile = ref(false)
    const uploadChoice = ref(true)
    const requestData = ref({
      csv_file: null,
      name: null,
      endpoint_url: null,
      endpoint_data_key: null
    })

    return {
      isCreation,
      connections,
      connectionsStore,
      googleStore,
      connectionMenuActions,
      showSheetSettings,
      showCreateConnectionModal,
      uploadedFile,
      cleanCSVFile,
      uploadChoice,
      requestData,
      getConnections,
      getSheetData
    }
  },
  beforeMount () {
    this.getConnections((data) => {
      this.connections = data
      this.$session.create('connections', data)
    })
  },
  methods: {
    async handleCreateConnection () {
      // Creates a new connection/sheet
      try {
        const response = await this.$http.post('sheets/upload', this.requestData)
        this.$session.listPush('connections', response.data)
        this.connections.push(response.data)
        this.showCreateConnectionModal = false
      } catch (e) {
        console.log(e)
      }
    },
    async handleConnectionDataRefresh (sheetId) {
      // Refresh the output data for the
      // selected connection
      try {
        const response = await this.$http.get(`sheets/${sheetId}`)
        this.$session.create(sheetId, response.data)
      } catch (e) {
        console.log(e)
      }
    },
    handleConnectionMenuAction (action, connectionObject) {
      // Actions for connection's dropdown menu
      switch (action) {
        case 'Refresh':
          this.handleConnectionDataRefresh(connectionObject.sheet_id)
          break;
      
        default:
          break;
      }
    } 
  }
}
</script>
