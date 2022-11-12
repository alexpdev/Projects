const { ipcRenderer, contextBridge } = require("electron");

window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }
  for (const dependency of ['chrome', 'node', 'electron']) {
    replaceText(`${dependency}-version`, process.versions[dependency])
  }
})

contextBridge.exposeInMainWorld('ipc', {
  require: require,
  send: (channel, data) => {
    ipcRenderer.send(channel, data);
  },
  receive: (channel, func) => {
    ipcRenderer.on(channel, (event, ...args) => func(...args));
  },
  once: (channel, func) => {
    ipcRenderer.once(channel, (event, ...args) => {
      func(...args);
    })
  },
  invoke: (channel, version, args) => {
    return ipcRenderer.invoke(channel, version, args).then((result) => {
      return result;
    })
  },
  sendSync: (channel, func) => {
    ipcRenderer.sendSync(channel, (event, ...args) => {
      func(...args);
    })
  },

})
