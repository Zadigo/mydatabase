<template>
  <v-dialog id="search-records-modal" v-model="showSearchRecordsModal" width="400">
    <v-card title="Select columns">
      <v-card-text>
        <p>Allow search on the specified columns</p>
        <v-switch v-for="column in currentConnection.columns" :key="column" :label="column" inset hide-details></v-switch>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="showSearchRecordsModal = false">Cancel</v-btn>
        <v-btn>Validate</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
