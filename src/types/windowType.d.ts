export {};

declare global {
  interface Window {
    ipc: any;
  }
}

let ipc = Window.ipc;


export interface PathReturn {
  canceled: boolean;
  filePaths: string[];
}
