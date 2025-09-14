export interface TokenApiResponse {
  access: string
  refresh: string
}

export type RefreshApiResponse  = Pick<TokenApiResponse, 'access'>
