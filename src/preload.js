const {readFileSync} = require("fs");
const { contextBridge } = require("electron");

function getLicenseData(){
  const contents = readFileSync("./src/assets/licenses.json");
  const LicenseData = JSON.parse(contents);
  console.log(LicenseData);
  return LicenseData
}

const LicenseData = getLicenseData();

contextBridge.exposeInMainWorld("licInfo", {
  data: LicenseData,
  getInfo: (symb) => {
    let filename = LicenseData[symb].filename;
    let content = readFileSync("./src/assets/licenses/" + filename);
    return {
      title: LicenseData[symb]["title"],
      filename: filename,
      content: content,
      symbol: symb,
    }
  }
})

// contextBridge.exposeInMainWorld("ipc", {
//   send: (channel, data) => {
//     ipcRenderer.send(channel, data);
//   },
//   receive: (channel, func) => {
//     ipcRenderer.on(channel, (event, ...args) => func(...args));
//   },
//   sendSync: (channel, ...args) => {
//     return ipcRenderer.sendSync(channel, ...args);
//   },
//   invoke: (channel, ...args) => {
//     console.log(channel);
//     return ipcRenderer.invoke(channel, args).then((result) => {
//       console.log(result);
//       return result;
//     });
//   }
// }
// );
