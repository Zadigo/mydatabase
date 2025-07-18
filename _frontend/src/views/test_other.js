emits: {
    'block-selected' () {
      return true
    }
  },
  setup () {
    const app = getCurrentInstance()
    
    const { listManager } = useUtilities()
    const { columnTypeChoices, columnSortingChoices } = useBlocksComposable(app)

    const pageStore = usePage()
    
    const tableColumnsRequestData = ref({})
    const tableBlockRequestData = ref({ allow_creation_columns: [] })

    return {
      columnTypeChoices,
      columnSortingChoices,
      tableBlockRequestData,
      tableColumnsRequestData,
      listManager,
      pageStore
    }
  },
  data () {
    return {
      selected: false,
      allowRecordCreation: false,
      showSearchDataModal: false,
      showCreateRecordModal: false,
      showColumnActionModal: false,
      currentUpdatedColumn: {
        name: null,
        column_type: null,
        column_sort: null,
        allow_record_creation: true,
        allow_record_update: true,
        column_visibility: true
      },
      columnMenuItems: [
        'Field type',
        'Hide'
      ]
    }
  },
  computed: {
    ...mapState(usePage, ['hasActiveSheet', 'availableData', 'availableDataColumns']),

    searchedBlockData () {
      return this.availableData.results
    },
    visibleColumns () {
      // Only return the columns that are set to be visible
      return _.filter(this.details.conditions.columns_visibility, (column) => {
        return column.visibility
      })
    }
  },
  created () {
    // For each column create a template that will be used
    // to track configuration updates
    this.pageStore.availableDataColumns.forEach((column) => {
      this.tableColumnsRequestData[column] = {
        name: column,
        column_type: 'Text',
        column_sort: 'No sort',
        column_visibility: true,
        allow_record_creation: this.details.record_creation_fields.includes(column),
        allow_record_update: this.details.record_update_fields.includes(column)
      }
    })
    console.log(this.tableColumnsRequestData)
  },
  beforeMount () {
    // Set a default current updated column to avoid an error
    // when the component mounts since this value would be null
    this.currentUpdatedColumn = this.tableColumnsRequestData[this.pageStore.availableDataColumns[0]]
  },
  methods: {
    async handleUpdateColumn () {
      // Updates the current column conffiguration
      // for the current block
      try {
        const path = `sheets/pages/${this.pageStore.currentPage.page_id}/blocks/${this.pageStore.currentBlock.block_id}/column/update`
        const response = await this.$http.post(path, this.tableColumnsRequestData[this.currentUpdatedColumn.name])
        this.showColumnActionModal = false
        response.data
      } catch (e) {
        console.log(e)
      }
    },
    handleSelection () {
      // Highlights the block when the user
      // has clicked on the card
      this.pageStore.loadFromCache()
      this.selected = !this.selected
      this.$emit('block-selected', this.details)
    },
    handleSearchActionModal () {
      // Shows the modal to allow search on
      // on certain specific fields
      this.showSearchDataModal = true
    },
    handleShowColumnActionModal (columnObject) {
      // Shows the modal to set specific actions
      // on a give column (search, visibility...)
      console.info(this.tableColumnsRequestData, columnObject)
      this.currentUpdatedColumn = this.tableColumnsRequestData[columnObject.column] || {}

      // const condition = this.pageStore.getColumnVisibilityCondition(columnName)
      // this.tableColumnRequestData.column_visibility = condition.visiblity
      
      this.showColumnActionModal = true
    }
  }
