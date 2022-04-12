#!/usr/bin/env node
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');
const { Torrent } = require('./torrentfilejs/torrent');


function cli(){
  var result = yargs(hideBin(process.argv))
    .alias('a', ['tracker', 'announce', 't'])
    .array('a')
    .describe('a', 'one or more tracker/announce URLs')
    .boolean('private')
    .describe('private', 'turns off dht and multi-tracker protocol')
    .describe('source', 'used primarily for cross-seeding purposes')
    .describe('comment', 'a comment that will be added to the metadata')
    .string('source')
    .string('comment')
    .describe('metaversion', 'which bittorrent version to use for formatting')
    .choices('metaversion', [1, 2, 3])
    .describe('piecelength', 'fixed size chunck of data for transferring pieces')
    .alias('piecelength', 'pl')
    .number('piecelength')
    .alias('p', 'path')
    .describe('p', 'absolute or relative path to contents.')
    .string('p')
    .parse()
    let tor = new Torrent(result['path'], result.announce, result.comment, result.piecelength,  result['private'], result.outfile, result.source);
    var meta = tor.assemble();
    tor.write();
    return tor;
}



console.log(cli());
