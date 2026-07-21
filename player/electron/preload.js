const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainProcess('electronAPI', {
  openPlaylist: () => ipcRenderer.invoke('open-playlist-dialog'),
  savePlaylist: (content) => ipcRenderer.invoke('save-playlist', content),
  getAppPath: () => ipcRenderer.invoke('get-app-path'),
});