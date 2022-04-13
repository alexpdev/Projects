#!/usr/bin/env node
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const { TorrentV1 } = require("./torrentfilejs/torrentv1");
const { TorrentV2 } = require("./torrentfilejs/torrentv2");

function execute() {
  var args = yargs(hideBin(process.argv))
    .describe("a", "one or more tracker/announce URLs")
    .describe("private", "turns off dht and multi-tracker protocols")
    .describe("source", "used primarily for cross-seeding purposes")
    .describe("comment", "a comment that will be added to the metadata")
    .describe("metaversion", "which bittorrent version to use for formatting")
    .describe(
      "piecelength",
      "fixed size chunck of data for transferring pieces"
    )
    .describe("p", "absolute or relative path to contents.")
    .describe("o", "output save location for created torrent file.")
    .describe("webseed", "one or more Web Seed URLs (GetRight)")
    .describe("httpseed", "one or more Web Seed URLs (Hoffman)")
    .alias("o", "out")
    .alias("a", ["tracker", "announce", "t"])
    .alias("piecelength", "pl")
    .alias("p", "path")
    .array("a")
    .array("webseed")
    .string("p")
    .boolean("private")
    .string("o")
    .string("source")
    .string("comment")
    .number("piecelength")
    .choices("metaversion", [1, 2, 3])
    .parse();
  console.log(args);
  let torrent = null;
  if (args.metaversion == 1) {
    torrent = TorrentV1;
  } else if (args.metaversion == 2) {
    torrent = TorrentV2;
  }
  let tor = new torrent(
    args["path"],
    args.announce,
    args.comment,
    args.piecelength,
    args["private"],
    args.out,
    args.source,
    args.webseed
  );
  tor.assemble();
  tor.write();
  return tor;
}

execute();
