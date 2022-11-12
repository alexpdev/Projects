const fs  =  require("fs");
const { Buffer } =  require("buffer");
const { bufJoin } =  require("./utils");

const D = 100;
const L = 108;
const I = 105;
const E = 101;
const COLON = 58;

function bencode(data) {
  if (typeof data == "number") {
    return encodeInt(data);
  } else if (typeof data == "string") {
    return encodeString(data);
  } else if (data instanceof Buffer) {
    return encodeBytes(data);
  } else if (data instanceof Array) {
    return encodeList(data);
  } else if (data instanceof Map) {
    return encodeMap(data);
  }
}

function encodeBytes(buffer) {
  var sep = Buffer.from(buffer.length + ":", "utf-8");
  var final = bufJoin([sep, buffer]);
  return final;
}

function encodeString(text) {
  var buffer = Buffer.from(text);
  var l = buffer.length;
  return Buffer.from(l + ":" + text);
}

function encodeInt(n) {
  return Buffer.from("i" + n + "e", "utf-8");
}

function encodeList(elems) {
  var arr = Buffer.from("l", "utf-8");
  for (elem of elems) {
    var elem = bencode(elem);
    arr = bufJoin([arr, elem]);
  }
  arr = bufJoin([arr, Buffer.from("e", "utf-8")]);
  return arr;
}

function encodeMap(mp) {
  let start = Buffer.from("d", "utf-8");
  for (let key of mp) {
    let buf1 = bencode(key[0]);
    let buf2 = bencode(key[1]);
    start = bufJoin([start, buf1, buf2]);
  }
  start = bufJoin([start, Buffer.from("e", "utf-8")]);
  return start;
}

function bendecode(data) {
  return decode(0, data).result;
}

function decode(i, data) {
  while (i < data.length) {
    let char = data[i];
    i += 1;
    if (char === D) {
      return decodeMap(i, data);
    } else if (char === L) {
      return decodeList(i, data);
    } else if (char === I) {
      return decodeInt(i, data);
    } else {
      return decodeString(i, data);
    }
  }
}

function decodeMap(i, data) {
  var map = new Map();
  while (i < data.length) {
    if (data[i] == E) {
      i += 1;
      break;
    }
    let key = decodeString(i, data);
    let val = decode(key.index, data);
    map.set(key.result, val.result);
    i = val.index;
  }
  return { index: i, result: map };
}

function decodeList(i, data) {
  let list = [];
  while (i < data.length) {
    if (data[i] == E) {
      i += 1;
      break;
    }
    let val = decode(i, data);
    list.push(val.result);
    i = val.index;
  }
  return { index: i, result: list };
}

function decodeInt(i, data) {
  let n = "";
  while (i < data.length) {
    if (data[i] == E) {
      i += 1;
      break;
    }
    i += 1;
    n = n + data[i];
  }
  return { index: i, result: n };
}

function decodeString(i, data) {
  let text = "";
  while (data[i] != COLON) {
    text = text + data[i];
    i += 1;
  }
  i += 1;
  let length = parseInt(text);
  let key = "";
  for (let j = 0; j < length; j++) {
    key = key + data[i];
    i += 1;
  }
  return { index: i, result: key };
}

function benWrite(data, path) {
  var fd = fs.openSync(path, "w");
  var bits = bencode(data);
  fs.writeSync(fd, bits);
  fs.closeSync(fd);
  return path;
}

module.exports = { benWrite };
