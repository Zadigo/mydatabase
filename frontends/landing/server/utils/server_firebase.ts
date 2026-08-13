import { initializeApp, cert, getApps } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'

export function useFirebaseAdmin() {
  const apps = getApps()

  if (!apps.length) {
    const config = useRuntimeConfig()

    initializeApp({
      credential: cert({
        projectId: config.public.firebaseProjectId,
        clientEmail: config.firebaseClientEmail,
        privateKey: config.firebasePrivateKey.replace(/\\n/g, '\n'),
      }),
    })
  }

  const db = getFirestore()
  return { db }
}
