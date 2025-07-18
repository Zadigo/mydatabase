// import { newSlideSchema } from '~/data'

// import type { NewSlide } from '~/data'

export function useCreateSlide() {
  const slideName = ref<string>('')
  const isPrivate = ref<boolean>(false)

  function create() {}

  return {
    slideName,
    isPrivate,
    create
  }
}
