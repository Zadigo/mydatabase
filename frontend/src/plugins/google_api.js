// import { GoogleSpreadsheet } from 'google-spreadsheet'
// import { JWT } from 'google-auth-library'


// async function googleSheetApi () {
//   const serviceAccountAuth = new JWT({
//     email: '818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
//     key: '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',
//     scopes: [
//       'https://www.googleapis.com/auth/spreadsheets',
//     ],
//   })

//   const doc = new GoogleSpreadsheet('<the sheet ID from the url>', serviceAccountAuth);

//   const result = await doc.loadInfo()
//   console.log(result)
// }

import { GoogleSpreadsheet } from 'google-spreadsheet'
// import { JWT } from 'google-auth-library'
// import creds from '../data/secret.json'

async function googleSheetApi () {
  // const auth = new JWT({
  //   email: '"818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
  //   key: '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',
  //   scopes: [
  //     'https://www.googleapis.com/auth/spreadsheets',
  //   ]
  // })
  const instance = new GoogleSpreadsheet('1WZ1lbhipsL7EnSAY-leen_jb8e5BB50T-iDJXqn4z5M', {})
  await instance.loadInfo()
  const c = await instance.sheetCount
  console.log(c)
  // await instance.(creds)
  // const s = instance.sheetsByIndex[0];
  // const rows = await s.getRows({ offset: 1 })
  // this.rows = rows;
}

export {
  googleSheetApi
}
