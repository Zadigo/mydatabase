<template>
  <v-dialog v-model="showCreateRecordModal" width="400">
    <v-card title="Select columns">
      <v-card-text>
        <p>Allow the creation for a new record for the specified columns</p>

        <div class="row">
          <!-- <div v-for="column in blockDetails.record_creation_columns" :key="column" class="col-12">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ column }}</span>
              <v-btn-toggle color="warning" multiple>
                <v-btn value="creation">Create</v-btn>
                <v-btn value="update">Update</v-btn>
              </v-btn-toggle>
            </div>
          </div> -->
        </div>

        <!-- <v-switch v-for="column in blockDetails.record_creation_columns" :key="column" :label="column" inset hide-details></v-switch> -->
      </v-card-text>

      <v-card-actions>
        <v-btn>Cancel</v-btn>
        <v-btn>Validate</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
