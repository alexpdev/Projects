// electron/electron.js
const path = require('path');
const { protocol, app, BrowserWindow, ipcMain, dialog } = require('electron');


const isDev = process.env.IS_DEV == "true" ? true : false;

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

const ipc = ipcMain
let win, dlog;

function createWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: true,
      webSecurity: false
    },
  });
  console.log(mainWindow);

  // and load the index.html of the app.
  // win.loadFile("index.html");
  win = mainWindow;
  mainWindow.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../index.html')}`
  );
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
});

app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipc.on("openFileExplorer",(event, payload) => {
  dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] });
})


const getFileFromUser = () => {
  const files = dialog.showOpenDialog({
    properties: ['openFile']
  });
  if (!files) {return;}
  console.log(files);
}

// Exit cleanly on request from parent process in development mode.
if (isDev) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
