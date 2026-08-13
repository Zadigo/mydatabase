export type Undefineable<T> = T | undefined

export type Nullable<T> = T | null

export type Emptyable<T> = T | '' | null | undefined

export type Arrayable<T> = T[]

export type StringInterface<T extends string> = { [ K in T ]: string }

export type BaseRoute = StringInterface<'id' | 'title' | 'path'>

export type Locale = 'fr' | 'en'

export type PageTitleOrDescription<T extends string> = Record<T, string>
