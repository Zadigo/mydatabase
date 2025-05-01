import axios from 'axios'
import type { App, Plugin } from 'vue'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
  timeout: 10000,
  responseType: 'json'
})

export default function createPlugins(): Plugin {
  return {
    install(app: App) {
      console.log(app)
    }
  }
}
