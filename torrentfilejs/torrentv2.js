const utils = require("./utils");
const Path = require("path");
const crypto = require("crypto");
const fs = require("fs");
const { benWrite } = require("./jsben");
const { Buffer } = require("buffer");

const BLOCKSIZE = 2 ** 14;
const HASHSIZE = 32;

class TorrentV2 {
  constructor(
    path = "",
    announce = [],
    comment = undefined,
    piecelength = undefined,
    privat = undefined,
    outfile = undefined,
    source = undefined,
    webseed = undefined
  ) {
    this.meta = new Map();
    this.info = new Map();
    if (announce.length > 0) {
      this.meta.set("announce", announce[0]);
      this.meta.set("announce-list", [announce]);
    } else {
      this.meta.set("announce", "");
      this.meta.set("announce-list", [[]]);
    }
    if (comment) {
      this.info.set("comment", comment);
    }
    if (webseed) this.meta.set("url-list", webseed);
    if (source) this.info.set("source", source);
    if (privat) this.info.set("private", 1);
    if (piecelength)
      this.info.set("piece length", utils.normalizePieceLength(piecelength));
    else this.info.set("piece length", utils.getPieceLength(path));
    this.outfile = outfile;
    this.meta.set("created by", "torrentfilejs");
    this.path = path;
    this.name = Path.basename(Path.resolve(this.path));
    this.info.set("name", this.name);
    this.meta.set("info", this.info);
    this.pieceLayers = new Map();
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
      let fhash = new Hasher(path, this.info.get("piece length"));
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

  write() {
    var path = this.path + ".torrent";
    benWrite(this.meta, path);
  }
}

function merkleRoot(blocks) {
  if (blocks.length > 1) {
    let arr = [];
    while (blocks.length > 1) {
      let block1 = blocks.shift();
      let block2 = blocks.shift();
      let block = Buffer.concat(
        [block1, block2],
        block1.length + block2.length
      );
      var shasum = crypto.createHash("sha256");
      shasum.update(block);
      block = shasum.digest();
      arr.push(block);
    }
    blocks = arr;
  }
  return blocks[0];
}

class Hasher {
  constructor(file, pieceLength) {
    this.pieceLength = pieceLength;
    this.root = null;
    this.pieceLayer = null;
    this.layerHashes = [];
    this.num_blocks = Math.floor(pieceLength / BLOCKSIZE);
    let current = fs.openSync(file);
    this.processFile(current);
  }

  processFile(fd) {
    while (1) {
      let blocks = [];
      let leaf = Buffer.alloc(BLOCKSIZE);
      for (let i = 0; i < this.num_blocks; i++) {
        var consumed = fs.readSync(fd, leaf, 0, BLOCKSIZE, null);
        if (!consumed) break;
        if (consumed < BLOCKSIZE) {
          leaf = leaf.subarray(0, consumed);
        }
        blocks.push(this.hash(leaf));
      }
      if (blocks.length == 0) {
        break;
      }
      if (blocks.length != this.numBlocks) {
        let remainder = this.numBlocks - blocks.length;
        if (this.layerHashes.length == 0) {
          let p2 = utils.nextPow2(blocks.length);
          remainder = p2 - blocks.length;
        }
        for (let j = 0; j < remainder; j++) {
          let padding = Buffer.alloc(32);
          blocks.push(padding);
        }
      }
      let layerHash = merkleRoot(blocks);
      this.layerHashes.push(layerHash);
    }
    this._calcRoot();
  }

  hash(buffer) {
    var shasum = crypto.createHash("sha256");
    shasum.update(buffer);
    return shasum.digest();
  }

  _calcRoot() {
    let size = 0;
    for (let hash of this.layerHashes) {
      size += hash.length;
    }
    this.pieceLayer = Buffer.concat(this.layerHashes, size);
    let hashes = this.layerHashes.length;
    if (hashes > 1) {
      let p2 = utils.nextPow2(hashes);
      let remainder = p2 - hashes;
      let arr = [];
      for (let i = 0; i < this.num_blocks; i++) {
        let padding = Buffer.alloc(HASHSIZE);
        arr.push(padding);
      }
      for (let j = 0; j < remainder; j++) {
        this.layerHashes.push(merkleRoot(arr));
      }
    }
    this.root = merkleRoot(this.layerHashes);
  }
}

module.exports = { TorrentV2 };
