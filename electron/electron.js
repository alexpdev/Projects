const path = require('path');
const { protocol, app, BrowserWindow, ipcMain, dialog } = require('electron');
const {Torrent, TorrentV2, TorrentV3} = require("./torrentfilejs/torrent");

const isDev = process.env.IS_DEV == "true" ? true : false;

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let win;

function createWindow() {
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

  win = mainWindow;
  mainWindow.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../index.html')}`
  );
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
});
app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
ipcMain.handle("openFileExplorer", (event, payload) => {
  let path = dialog.showOpenDialogSync(win, {
    properties: ['openFile'],
    message:"select torrent file"
  });
  return path[0];
})
ipcMain.handle("openFolderExplorer",(event, payload) => {
  let path = dialog.showOpenDialogSync(win, {
    properties: ['openDirectory'],
    message:"select torrent folder"
  });
  return path[0];
})
ipcMain.handle("selectOutput", (event, payload) => {
  let path = dialog.showSaveDialogSync(win, {
    filters:[
      {name: "torrents", extensions: [".torrent"]}
    ]
  })
  return path[0];
})
ipcMain.handle("createTorrent",async (event, version, args) => {
  let torrent;
  if (version == 3){
    torrent = new TorrentV3(...args);
  }
  else if (version == 2){
    torrent = new TorrentV2(...args);
  }
  else {
    torrent = new Torrent(...args);
  }
  console.log(args);
  torrent.assemble();
  const meta = await torrent.write();
  return meta;
})


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
