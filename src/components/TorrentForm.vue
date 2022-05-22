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
    <form id="torrentform">
      <div class="field">
        <label for="path" class="label">Path</label>
        <div class="columns">
          <div class="column is-6">
            <input class="input" type="text" v-model="formData.path"/>
          </div>
          <div class="column is-1">
            <button
              name="torrent"
              class="button is-primary"
              type="button"
              @click="selectFolder()"
            >
            <span class="icon">
              <i class="fas fa-folder-open"></i>
            </span>
            <span>
              select folder
            </span>
            </button>
          </div>
          <div class="column is-2"></div>
          <div class="column is-1">
            <button
              name="torrent"
              class="button is-primary"
              type="button"
              @click="selectFile()"
            >
            <span class="icon">
              <i class="fas fa-file-import"></i>
            </span>
            <span>
              select file..
            </span>
            </button>
          </div>
        </div>
      </div>
      <div class="field">
        <label for="output" class="label">Save To</label>
        <p class="control">
          <input
            type="text"
            class="input"
            v-model="formData.output"
            id="output"
            name="output"
            placeholder="/path/to/save/location.torrent"
          />
        </p>
      </div>
      <div class="field">
        <label for="comment">Comment</label>
        <p class="control">
          <input
            type="text"
            class="input"
            v-model="formData.comment"
            name="comment"
            id="comment"
          />
        </p>
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
import { PathReturn } from "../types/windowType";
import { Torrent, TorrentV2, TorrentV3 } from "../torrentfilejs/torrent";

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
        path: "...",
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
    selectFile() {
      let result = window.ipc.invoke("openFileExplorer", {});
      this.formData.path = result;
    },
    selectFolder() {
      let result = window.ipc.invoke("openFolderExplorer", {});
      this.formData.path = result;
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
