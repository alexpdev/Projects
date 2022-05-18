<template>
  <section id="torrentform" class="hero is-info">
    <div class="hero-body">
      <div class="container">
        <figure class="image">
          <img :src="formData.image" />
        </figure>
        <h3 class="subtitle">{{ description }}</h3>
      </div>
    </div>
  </section>
  <div class="block">
    <form  id="torrentform">
      <div class="file has-name is-fullwidth is-primary">
        <label for="path" class="file-label">
          <input
            type="file"
            id="pathselection"
            class="file-input"
            name="contents"
            v-on:change="openModal()"
          />
          <span class="file-cta">
            <span class="file-icon">
              <i class="fas fa-upload"></i>
            </span>
            <span class="file-label"> Path</span>
          </span>
          <span class="file-name">
            {{ formData.path }}
          </span>
        </label>
      </div>
      <div class="field">
        <label for="output" class="label">Save To</label>
        <input
          type="text"
          class="input"
          v-model="formData.output"
          id="output"
          name="output"
          placeholder="/path/to/save/location.torrent"
        />
      </div>
      <div class="field">
        <label for="comment">Comment</label>
        <input
          type="text"
          class="input"
          v-model="formData.comment"
          name="comment"
          id="comment"
        />
      </div>
      <div class="field">
        <label class="label" for="source">Source</label>
        <input type="text" class="input" name="source" id="source" />
      </div>
      <div class="field">
        <label class="label" for="announce">Trackers</label>
        <textarea
          name="announce"
          id="announce"
          class="textarea"
          cols="80"
          rows="6"
        >
        </textarea>
      </div>
      <div class="columns">
        <div class="column is-4">
          <div class="field">
            <label class="label" for="private">Private</label>
            <input
              type="checkbox"
              name="private"
              id="private"
              v-model="formData.privat"
            />
          </div>
        </div>
        <div class="column is-4">
          <div class="field">
            <label for="pieceLength" class="label">Piece Length</label>
            <select
              name="pieceLength"
              id="pieceLength"
              class="select"
              v-model="formData.pieceLength"
            >
              <option
                v-for="size in formData.sizes"
                :value="size.Size"
                :key="size.Size"
              >
                {{ size.Size }}
              </option>
            </select>
          </div>
        </div>
        <div class="column is-4">
          <div class="field">
            <label for="version" class="label">Bittorrent Version</label>
            <input
              type="radio"
              class="radio"
              id="1"
              value="1"
              v-model="formData.version"
            />
            <label for="1" class="radio">1</label>
            <input
              type="radio"
              class="radio"
              id="2"
              value="2"
              v-model="formData.version"
            />
            <label for="2" class="radio">2</label>
            <input
              type="radio"
              class="radio"
              id="hybrid"
              value="hybrid"
              v-model="formData.version"
            />
            <label for="hybrid" class="radio">hybrid</label>
          </div>
        </div>
      </div>
      <div class="field">
        <button
          class="button is-info is-outlined pl-6 pr-6"
          @click="submitFormData"
        >
          Submit
        </button>
      </div>
    </form>
    <section class="section">
      <div class="box">
        <p>{{ JSON.stringify(formData, null, 2) }}</p>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import image from "./../assets/torrentfile.png";
import { TorrentV2, Torrent, TorrentV3 } from "../torrentfilejs/torrent";
import { dialog } from "@electron/remote";



export default defineComponent({
  name: "TorrentForm",
  data() {
    return {
      title: "torrentfile",
      description: "Torrent file builder, checker, and reviewer.",
      date: Date(),
      formData: {
        image: image,
        privat: false,
        source: "",
        comment: "",
        path: "",
        output: "",
        announce: "",
        version: "",
        pieceLength: "",
        sizes: [
          { ID: 14, Size: "16 KiB" },
          { ID: 15, Size: "32 KiB" },
          { ID: 16, Size: "64 KiB" },
          { ID: 17, Size: "128 KiB" },
          { ID: 18, Size: "256 KiB" },
          { ID: 19, Size: "512 KiB" },
          { ID: 20, Size: "1 MiB" },
          { ID: 21, Size: "2 MiB" },
          { ID: 22, Size: "4 MiB" },
          { ID: 23, Size: "8 MiB" },
          { ID: 24, Size: "16 MiB" },
          { ID: 25, Size: "32 MiB" },
          { ID: 26, Size: "64 MiB" },
          { ID: 27, Size: "128 MiB" },
          { ID: 28, Size: "256 MiB" },
        ],
      },
    };
  },
  methods: {
    openModal() {
      let pathname = "";
      if (process.platform !== 'darwin') {
        dialog.showOpenDialog({
            title: 'Select the .torrent file...',
            buttonLabel: 'Upload',
            filters: [],
            properties: ['openFile']
        }).then(file => {
          let filepath = file.filePaths[0].toString();
          console.log(file.canceled);
            if (!file.canceled) {
              pathname = filepath;
            }
        }).catch(err => {
            console.log(err);
        });
    } else {
        dialog.showOpenDialog({
            title: 'Select the File to be uploaded',
            buttonLabel: 'Upload',
            filters: [],
            properties: ['openFile', 'openDirectory']
        }).then(file => {
            console.log(file.canceled);
            if (!file.canceled) {
              let filepath = file.filePaths[0].toString();
              pathname = filepath;
            }
        }).catch(err => {
            console.log(err);
        });
      }
      this.formData.path = pathname;
      this.formData.output = pathname + ".torrent";
    },
    submitFormData(event: any) {
      const args = this.$data.formData;
      const params = [
        args.path,
        args.announce,
        "",
        "",
        args.pieceLength,
        args.privat,
        args.comment,
        args.source,
        args.output,
      ];
      let torrent;
      if (args.version === "1") {
        torrent = new Torrent(...params);
      } else if (args.version == "2") {
        torrent = new TorrentV2(...params);
      } else {
        torrent = new TorrentV3(...params);
      }
      torrent.assemble();
      torrent.write();
      return torrent;
    },
  },
});
</script>

<style>
#torrentform {
  margin-top: 12px;
}
.file-name,
.input,
.textarea,
.checkbox,
.select,
.button {
  border: #e51 solid 2px;
  border-radius: 2px;
  background-color: #404440;
  color: white;
}
.input:hover {
  border-color: #a51;
  border-width: 2px;
}
.input:active,
.input:focus {
  border-color: #a51;
}
</style>
