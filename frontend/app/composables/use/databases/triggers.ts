import type { DatabaseFunction } from "~/types"
import type { DatabaseTrigger } from "~/types/api/triggers"

/**
 * Function used to manage and create database triggers
 */
export const useDatabaseTriggers = createGlobalState(() => {
  const dbTriggers = ref<DatabaseTrigger>({
    on: {
      database: 0
    },
    trigger: []
  })

  const [ showFunctionsModal, toggerFunctionsModal ] = useToggle()

  function create() {
    dbTriggers.value.trigger.push({
      name: '',
      event: 'insert',
      when: {
        before: false,
        after: false
      },
      orientation: 'row',
      function: ''
    })
  }

  function deleteTrigger(trigger: DatabaseTrigger['trigger'][number]) {
    dbTriggers.value.trigger = dbTriggers.value.trigger.filter(item => item.name !== trigger.name)
  }

  function selectFunction(trigger: DatabaseTrigger['trigger'][number], dbFunction: DatabaseFunction) {
    trigger.function = dbFunction.function.name
  }

  const triggerNames = computed(() => dbTriggers.value.trigger.map(item => item.name))

  /**
   * Search
   */

  const search = ref<string>('')
  const searched = useArrayFilter(() => dbTriggers.value.trigger, (item) => {
    return item.name.toLocaleLowerCase().includes(search.value.toLocaleLowerCase())
  })

  /**
   * Writeable computed to get the trigger being edited in the modal
   */

  const editableTrigger = reactify(trigger => useArrayFind(dbTriggers.value.trigger, item => item.name === trigger.name).value)

  return {
    showFunctionsModal,
    dbTriggers,
    search,
    searched,
    triggerNames,
    selectFunction,
    editableTrigger,
    toggerFunctionsModal,
    create,
    deleteTrigger
  }
})
