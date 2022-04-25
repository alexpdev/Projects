const utils = require("./utils");
const Path = require("path");
const fs = require("fs");
const { benWrite } = require("./jsben");
const { Buffer } = require("buffer");
const { Hasher1, Hasher2, Hasher3 } = require("./hasher");

class TorrentFile {
  constructor(
    path=undefined,
    announce=undefined,
    httpseed=undefined,
    urllist=undefined,
    piecelength=undefined,
    priv=undefined,
    comment=undefined,
    source=undefined,
    outfile=undefined,
    cwd=undefined,
  ) {
    this.meta = new Map();
    this.info = new Map();
    this.path = path;
    this.name = Path.basename(Path.resolve(this.path));
    this.meta.set("created by", "torrentfilejs");
    this.info.set("name", this.name);
    if (urllist) this.meta.set("url-list", urllist);
    if (httpseed) this.meta.set("httpseeds", httpseed)
    if (comment) this.info.set("comment", comment);
    if (webseed) this.meta.set("url-list", webseed);
    if (source) this.info.set("source", source);
    if (priv) this.info.set("private", 1);
    if (announce && announce.length > 0) {
      this.meta.set("announce", announce[0]);
      this.meta.set("announce-list", [announce]);
    } else {
      this.meta.set("announce", "");
      this.meta.set("announce-list", [[""]]);
    }
    if (piecelength) this.pieceLength = utils.normalizePieceLength(piecelength);
    else this.pieceLength = utils.getPieceLength(path);
    this.info.set("piece length", this.pieceLength);
    if (!outfile && cwd) this.outfile = "./" + this.name + ".torrent";
    else this.outfile = outfile;
    this.meta.set("info", this.info);
  }

  sortMeta() {
    let info = this.meta.get("info");
    info = new Map([...map].sort());
    this.meta.set("info", info);
    meta = new Map([...this.meta].sort());
    this.meta = meta;
    return meta;
  }

  write() {
    this.sortMeta();
    var path;
    if (this.outfile) path = this.outfile;
    else  path = this.path + ".torrent";
    benWrite(this.meta, path);
  }
}

class Torrent extends TorrentFile {
  constructor(...args){
    super(...args)
  }

  assemble(){
    let info = this.info;
    let { size, files } = utils.fileListTotal(this.path);
    if (utils.isfile(this.path)) info.set("length", size);
    else {
      info.set("files", []);
      files.forEach((path) => {
        let obj = new Map();
        obj.set("length", utils.getsize(path));
        obj.set("path", utils.pathparts(this.path, path));
        info.get("files").push(obj);
      });
    }
    let pieces = Buffer.alloc(0);
    let feeder = new Hasher1(files, this.info.get("piece length"));
    feeder.iter();
    pieces = utils.bufJoin(feeder.pieces);
    info.set("pieces", pieces);
    this.meta.set("info", info);
    return this.meta;
  }
}

class TorrentV2 extends TorrentFile{
  constructor(...args){
    super(...args);
  }

  assemble() {
    let info = this.info;
    let { size, files } = utils.fileListTotal(this.path);
    if (utils.isfile(this.path)) {
      info.set("length", size);
      var fileTree = new Map();
      fileTree.set(info.get("name"), this._traverse(this.path));
      info.set("file tree", fileTree);
    } else {
      info.set("file tree", this._traverse(this.path));
    }
    info.set("meta version", 2);
    this.meta.set("piece layers", this.pieceLayers);
    this.info = info;
    this.meta.set("info", this.info);
  }

  _traverse(path) {
    if (utils.isfile(path)) {
      let size = utils.getsize(path);
      if (size == 0) {
        return new Map([["", new Map([["length", size]])]]);
      }
      let fhash = new Hasher2(path, this.info.get("piece length"));
      if (size > this.info.get("piece length")) {
        this.pieceLayers.set(fhash.root, fhash.pieceLayer);
      }
      let inner = [
        ["length", size],
        ["pieces root", fhash.root],
      ];
      return new Map([["", new Map(inner)]]);
    } else {
      let fileTree = new Map();
      if (utils.isdir(path)) {
        for (fd of fs.readdirSync(path)) {
          const fpath = Path.resolve(path, fd);
          fileTree.set(fd, this._traverse(fpath));
        }
      }
      return fileTree;
    }
  }
}

class TorrentV3 extends TorrentFile{
  constructor(...args){
    super(...args);
  }
  assemble() {
    let info = this.info;
    info.set("meta version", 2);
    if (utils.isfile(this.path)) {
      info.set("length", size);
      var fileTree = new Map();
      fileTree.set(info.get("name"), this._traverse(this.path));
      info.set("file tree", fileTree);
    } else {
      info.set("file tree", this._traverse(this.path));
      info.set("files", this.files);
    }
    this.meta.set("piece layers", this.pieceLayers);
    info.set("pieces", utils.bufJoin(this.pieces));
    this.info = info;
    this.meta.set("info", this.info);
  }

  _traverse(path) {
    if (utils.isfile(path)) {
      let size = utils.getsize(path);
      let parts = [
        ["length", size],
        ["path", utils.pathparts(this.path, path)],
      ];
      this.files.push(new Map(parts));
      if (size == 0) {
        return new Map([["", new Map([["length", size]])]]);
      }
      let fhash = new Hasher3(path, this.info.get("piece length"));
      if (size > this.info.get("piece length")) {
        this.pieceLayers.set(fhash.root, fhash.pieceLayer);
      }
      this.hashes.push(fhash);
      this.pieces.push(utils.bufJoin(fhash.pieces));
      if (fhash.paddingFile) {
        this.files.push(fhash.paddingFile);
      }
      let inner = [
        ["length", size],
        ["pieces root", fhash.root],
      ];
      return new Map([["", new Map(inner)]]);
    } else {
      let fileTree = new Map();
      if (utils.isdir(path)) {
        for (let fd of fs.readdirSync(path)) {
          const fpath = Path.resolve(path, fd);
          fileTree.set(fd, this._traverse(fpath));
        }
      }
      return fileTree;
    }
  }
}

module.exports = { Torrent, TorrentV2, TorrentV3 };
