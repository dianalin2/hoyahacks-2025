
const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron')
const path = require('path')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      autoplay: false,
      autofill: false,
      preload: path.join(__dirname, 'preload.js'),
    }
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()

  ipcMain.on('queryAll', async (event) => {
    try {
      const response = await fetch('http://localhost:5000/all');
      const files = await response.json();
      event.sender.send('queryAll-success', files)
    } catch (err) {
      console.error(err)
      event.sender.send('queryAll-error', err)
    }
  });

  ipcMain.on('queryDB', async (event, { query, paths }) => {
    try {
      const queryStr = encodeURIComponent(query)
      const pathsStr = encodeURIComponent(paths)
      const response = await fetch(`http://localhost:5000/query?query=${queryStr}&paths=${pathsStr}`);
      const files = await response.json();
      event.sender.send('queryDB-success', files)
    } catch (err) {
      console.error(err)
      event.sender.send('queryDB-error', err)
    }
  });

  ipcMain.on('openFile', async (event, { path }) => {
    try {
      shell.showItemInFolder(path)
      event.sender.send('openFile-success')
    } catch (err) {
      console.error(err)
      event.sender.send('openFile-error', err)
    }
  });

  ipcMain.on('searchDirectory', async (event) => {
    try {
      const files = await dialog.showOpenDialog({ properties: ['openDirectory'] });
      if (files === undefined) {
        console.log('No file selected')
        event.sender.send('searchDirectory-error', { response: 'No file selected' })
        return //stop it from sending success 
      }
      event.sender.send('searchDirectory-success', files);
    } catch (err) {
      console.error(err)
      event.sender.send('searchDirectory-error', err)
    }
  });
});
