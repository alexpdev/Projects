const utils = require('./utils');
const Path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const { Buffer } = require('buffer')

class Torrent{
  constructor(
      path='',
      announce=[],
      comment=undefined,
      piecelength=undefined,
      privat=undefined,
      outfile=undefined,
      source=undefined,
      ) {
    this.meta = new Map();
    this.info = new Map();
    if (announce.length > 0){
      this.meta.set('announce', announce[0]);
      this.meta.set('announce-list', [announce]);
    }
    else {
      this.meta.set('announce', '');
      this.meta.set('announce-list', [[]]);
    }
    if (comment) {
      this.info.set('comment', comment);
    }
    if (source)
      this.info.set('source', source);
    if (privat)
      this.info.set('private', 1);
    if (piecelength)
      this.info.set('piece length', utils.normalizePieceLength(piecelength));
    else
      this.info.set('piece length', utils.getPieceLength(path));
    this.outfile = outfile;
    this.meta.set('created by', 'torrentfilejs')
    this.path = path;
    this.name = Path.basename(Path.resolve(this.path));
    this.info.set('name', this.name);
    this.meta.set("info",this.info);
    }

    assemble() {
      let info = this.info;
      let {size, files} = utils.fileListTotal(this.path);
      if (utils.isfile(this.path))
        info["length"] = size;
      else {
        info["files"] = [];
        files.forEach((path) => {
          let obj = {
            length: utils.getsize(path),
            path: utils.pathparts(this.path, path)
          }
          info.files.push(obj);
        })
      }
      let pieces = Buffer.alloc(0);
      let feeder = new Hasher(files, this.info.get("piece length"));
      for (var piece of feeder.iter()){
        pieces = Buffer.concat([pieces, piece], pieces.length + piece.length);
      }
      info["pieces"] = pieces;
      this.info = info;
      this.meta["info"] = this.info;
      return this.meta;
    }

    sortMeta(){
      let meta = this.meta;
      meta.info = meta.info.sort();
      meta = meta.sort();
      return meta;
    }

    write(){
    }

}


class Hasher {
  constructor(files, pieceLength){
    this.pieceLength = pieceLength;
    this.files = files;
    var sizes = files.map((file) => {
      var stats = fs.statSync(file);
      return stats.size;
    })
    this.total = sizes.reduce((a,b) => a + b, 0);
    this.index = 0;
    this.current = fs.openSync(this.files[this.index]);
  }

  nextFile(){
    this.index += 1;
    if (this.index < this.files.length){
      fs.close(this.current);
      this.current = fs.openSync(this.files[this.index]);
      return true;
    }
    return false;
  }

  handlePartial(buffer) {
    while (buffer.length < this.pieceLength && this.nextFile()) {
      var target = this.pieceLength - buffer.length;
      var temp = Buffer.alloc(target);
      var size = fs.readSync(this.current, temp, 0, target, -1);
      buffer = Buffer.concat([buffer, temp], buffer.length + size);
      if (size == target)
        break
    }
    return buffer;
  }

  *iter() {
    while (1){
      var buffer = Buffer.alloc(this.pieceLength);
      var consumed = fs.readSync(this.current, buffer, 0, this.pieceLength, null);
      if (!consumed){
        if (!this.nextFile()){
          return;
        }
      }
      else if (consumed < this.pieceLength){
        yield this.handlePartial(buffer.subarray(0,consumed));
      }
      else {
        var shasum = crypto.createHash('sha1');
        shasum.update(buffer);
        yield shasum.digest();
      }
    }
  }
}

module.exports = {Torrent};
