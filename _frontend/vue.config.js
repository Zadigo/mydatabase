const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      fallback: {
        // https: false,
        // querystring: false,
        // url: false,
        // os: false,
        // stream: false,
        // path: false,
        // util: false,
        // crypto: false,
        // assert: false
      }
    }
  }
})
