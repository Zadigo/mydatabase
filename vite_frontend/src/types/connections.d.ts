import type { User } from './user'

export interface Connection {
  user: User
  id_token: string
  access_token: string
  refresh_token: string
  expires_in: string
  token_type: 'Bearer' | 'Token'
  scope: string
}
