import { defineProps, defineEmits } from 'vue'

export function useModal() {
  const props = defineProps<{ modelValue: boolean }>()
  const emit = defineEmits<{ 'update:modelValue': [boolean] }>()

  const show = useVModel(props, 'modelValue', emit)

  return {
    show
  }
}
