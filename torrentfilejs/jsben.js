const { Buffer } = require('buffer');
const fs = require('fs');


function bencode(data){
  if (intanceof(data))
}

function encodeBytes(buffer){
  var sep = Buffer.from(buffer.length + ':','utf-8');
  return Buffer.concat(sep, buffer);
}

function encodeString(text){
  var buffer = Buffer.from(text);
  var l = buffer.length;
  return Buffer.from(l + ":" + text);
}

function encodeInt(n){
  return Buffer.from("i" + n + "e", 'utf-8')
}

function encodeList(elems){
  var arr = Buffer.from("l", "utf-8");
  for (elem of elems) {
    encode
  }
}
