const fs = require("fs");
const Path = require("path");

function exists(path) {
  return fs.access(path, (err) => {
    if (err) return false;
    return true;
  });
}

function humanizeBytes(amount) {
  if (amount < 1024) return new String(amount);
  if (1024 <=  amount && amount < 1048576) return amount / 1024 + " KiB";
  if (1048576 <= amount && amount < 1073741824) return amount / 1048567 + " MiB";
  return amount / 1073741824 + " GiB";
}

function normalizePieceLength(pieceLength) {
  if (typeof pieceLength === "string") pieceLength = parseInt(pieceLength);
  if (13 < pieceLength && pieceLength <= 27) return Math.pow(2, pieceLength);
  if (pieceLength > 28) {
    let log = Math.log2(pieceLength);
    if (Math.pow(2, log) === pieceLength) return pieceLength;
  }
  throw "Incorrect input for `pieceLength`. Acceptable values include numbers 14 - 27 or any perfect power of 2 between 2^14 and 2^27.";
}

function getPieceLength(size) {
  let exp = 14;
  while (size / Math.pow(2, exp) > 200 && exp < 25) exp += 1;
  return Math.pow(2, exp);
}

const traverse = (path, result = []) => {
  fs.readdirSync(path).forEach((file) => {
    const fpath = Path.resolve(path, file);
    const stats = { file, path: fpath };
    if (fs.statSync(fpath).isDirectory()) {
      stats.type = "dir";
      stats.files = [];
      result.push(stats);
      return traverse(fpath, stats.files);
    }
    stats.type = "file";
    result.push(stats);
  });
  return result;
};


function fileListTotal(path) {
  const stats = fs.statSync(path);
  if (stats.isFile()) return { files: [path], size: stats.size };
  let total = 0;
  let file_list = [];
  for (let fd of fs.readdirSync(path)) {
    const fpath = Path.resolve(path, fd);
    var result = fileListTotal(fpath);
    total += result.size;
    file_list = file_list.concat(result.files);
  }
  return { size: total, files: file_list };
}

function pathSize(path) {
  const file_list = fileListTotal(path);
  return file_list.size;
}

function getFileList(path) {
  const result = fileListTotal(path);
  return result.files;
}


function pathStat(path) {
  const { size, files } = fileListTotal(path);
  const pieceLength = getPieceLength(size);
  return { files: files, size: size, pieceLength: pieceLength };
}

function pathPieceLength(path) {
  const size = pathSize(path);
  return getPieceLength(size);
}

function nextPow2(value) {
  if (!value & (value - 1) && value) {
    return value;
  }
  let start = 1;
  while (start < value) {
    start <<= 1;
  }
  return start;
}

function isfile(path) {
  return fs.statSync(path).isFile();
}

function isdir(path) {
  return fs.statSync(path).isDirectory();
}

function getsize(path) {
  return fs.statSync(path).size;
}

function pathparts(from, to) {
  let rel = Path.relative(from, to);
  let arr = rel.split(Path.sep);
  return arr;
}

function bufJoin(arr) {
  let total = 0;
  for (var i = 0; i < arr.length; i++) {
    total += arr[i].length;
  }
  return Buffer.concat(arr, total);
}

module.exports = {
  nextPow2,
  pathPieceLength,
  pathSize,
  fileListTotal,
  pathStat,
  getFileList,
  getPieceLength,
  normalizePieceLength,
  exists,
  isfile,
  getsize,
  pathparts,
  bufJoin,
  isdir,
};
