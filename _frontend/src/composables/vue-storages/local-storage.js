// import vue from 'vue'

const { setupDevtoolsPlugin } = require('@vue/devtools-api')

// const DEBUG = (process.env.NODE_ENV !== 'production')

// const storageSymbol = (DEBUG ? Symbol('vue-local-storage') : Symbol())

// const storageSymbol = /*#__PURE__*/ Symbol('local')

function setupDevtools (app, storage) {
    let devtoolsApi = null
    const devtools = {}

    setupDevtoolsPlugin({
        id: 'vue-local-storage',
        label: 'Vue Local Storage',
        packageName: 'vue-local-storage',
        homepage: 'http://example.com',
        componentStateTypes: ['vue-local-storage'],
        enableEarlyProxy: true,
        app
    }, api => {
        devtoolsApi = api
        devtoolsApi
        api.addInspector({
            id: 'vue-local-storage',
            label: 'Vue Local Storage',
            icon: 'storage'
        })

        api.on.getInspectorState((payload) => {
            if (payload.inspectorId === 'vue-local-storage') {
                payload.state = {
                    state: {
                        key: 'vue-local-storage',
                        value: storage.data
                    }
                }
            }
        })

        api.on.getInspectorTree((payload) => {
            if (payload.inspectorId === 'vue-local-storage') {
                payload.rootNodes = [
                    {
                        id: 'storage',
                        label: 'Storage'
                    }
                ]
            }
        })

        // api.notifyComponentUpdate('vue-local-storage')
        // api.sendInspectorTree('vue-local-storage')
        // api.sendInspectorState('vue-local-storage')
    })

    return devtools
}

class VueLocalStorage {
    constructor() {
        this.DEFAULT_KEY_NAME = 'vue_local'
        this.storage = localStorage
    }

    get data () {
        var result = JSON.parse(this.storage.getItem(this.DEFAULT_KEY_NAME))

        if (!result) {
            this._save({})
            return {}
        } else {
            return result
        }
    }

    _save (data) {
        // Saves an element under the global session key
        this.storage.setItem(this.DEFAULT_KEY_NAME, JSON.stringify(data))
    }

    _getValueForOperation (key) {
        // Return the numeric value stored under a key
        // to run a given operation
        // var storedData = this.data
        // let result = storedData[key]
        const result = this.retrieve(key)

        if (typeof result === 'undefined') {
            return 0
        }

        if (typeof result !== 'number') {
            throw new Error('Value for increment or decrement operation should be a number')
        }
        return result
    }

    _getList (key) {
        // Returns the value of the key if the
        // item is Array otherwise raises an error
        var storedData = this.data
        const result = storedData[key]
        if (!Array.isArray(result)) {
            throw new Error('Object is not an array')
        }
        return result
    }

    retrieve (key) {
        return this.data[key]
    }

    create (key, value) {
        var storedData = this.data
        storedData[key] = value
        this._save(storedData)
    }

    exists (key) {
        const storedData = this.data
        return Object.keys(storedData).includes(key)
    }

    getDelete (key) {
        let returnValue = null
        var storedData = this.data

        returnValue = storedData[key]
        delete storedData[key]

        this._save(storedData)
        return returnValue
    }

    increment (key) {
        let result = this._getValueForOperation(key)
        result = result += 1
        this.create(key, result)
    }

    decrement (key) {
        let result = this._getValueForOperation(key)
        result = result -= 1
        this.create(key, result)
    }

    incrementBy (key, k = 1) {
        let result = this._getValueForOperation(key)
        result = result += k
        this.create(key, result)
    }

    decrementBy (key, k = 1) {
        let result = this._getValueForOperation(key)
        result = result -= k
        this.create(key, result)
    }

    getOrCreate (key, value) {
        const result = this.exists(key)
        let returnValue = null
        let returnArray
        if (result) {
            returnValue = this.retrieve(key)
            returnArray = [false, returnValue]
        } else {
            this.create(key, value)
            returnValue = value
            returnArray = [true, returnValue]
        }
        return returnArray
    }

    listPush (key, value) {
        const result = this._getList(key)
        result.push(value)
        this.create(key, result)
    }

    defaultList (key, value) {
        if (this.exists(key)) {
            this.listPush(key, value)
        } else {
            this.create(key, [value])
        }
    }

    listMerge (key, values) {
        var newList = null
        const result = this._getList(key)

        if (!Array.isArray(values)) {
            throw new Error('Is not an array')
        }

        newList = [...result, ...values]
        this.create(key, newList)
    }

    listCount (key) {
        const result = this._getList(key)
        return result.length
    }

    toggle (key) {
        var result = this.retrieve(key)
        if (typeof result === 'boolean') {
            this.create(key, !result)
        } else {
            this.create(key, true)
        }
    }

    remove (key) {
        var result = this.data
        delete result[key]
        this._save(result)
    }

    save (key, value) {
        this.storage.setItem(key, value)
    }

    install (app) {
        setupDevtools(app, this)
        app.config.globalProperties.$localstorage = this
        app.mixin({
            data: () => ({
                localStorage: this.data
            })
        })
        window.VueLocalStorage = this
        // if (DEBUG) {
        // }
    }
}

function createVueLocalStorage () {
    return new VueLocalStorage()
}

export {
    createVueLocalStorage,
    VueLocalStorage
}
