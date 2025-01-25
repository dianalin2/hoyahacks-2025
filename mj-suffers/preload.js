const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
    queryAll: () => {
        ipcRenderer.send('queryAll');

        return new Promise((resolve, reject) => {
            ipcRenderer.once('queryAll-success', (event, data) => {
                resolve({ event, data })
            })
            ipcRenderer.once('queryAll-error', (event, error) => {
                reject({ event, error })
            })
        })
    },
    queryDB: (query) => {
        ipcRenderer.send('queryDB', { query });

        return new Promise((resolve, reject) => {
            ipcRenderer.once('queryDB-success', (event, data) => {
                resolve({ event, data })
            })
            ipcRenderer.once('queryDB-error', (event, error) => {
                reject({ event, error })
            })
        })
    },
    openFile: (path) => {
        ipcRenderer.send('openFile', { path });

        return new Promise((resolve, reject) => {
            ipcRenderer.once('openFile-success', (event, data) => {
                resolve({ event, data })
            })
            ipcRenderer.once('openFile-error', (event, error) => {
                reject({ event, error })
            })
        })
    },
    searchDirectory: () => {
        ipcRenderer.send('searchDirectory');

        return new Promise((resolve, reject) => {
            ipcRenderer.once('searchDirectory-success', (event, data) => {
                resolve({ event, data })
            })
            ipcRenderer.once('searchDirectory-error', (event, error) => {
                reject({ event, error })
            })
        })
    },
    indexDirectory: (path) => {
        ipcRenderer.send('indexDirectory', { path });

        return new Promise((resolve, reject) => {
            ipcRenderer.once('indexDirectory-success', (event, data) => {
                resolve({ event, data })
            })
            ipcRenderer.once('indexDirectory-error', (event, error) => {
                reject({ event, error })
            })
        })
    }
})
