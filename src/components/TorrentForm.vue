<template>
  <div class="container mt-2">
    <form id="torrentform">
      <div class="hstack gap-2 my-3">
        <label for="path" class="col-form-label text-nowrap">Content</label>
        <input
          class="form-control inp"
          type="text"
          id="path"
          name="path"
          v-model="formData.path"
        />
        <button
          name="torrent"
          class="btn button text-nowrap"
          type="button"
          @click="selectFolder()"
        >
          <span>
            <i class="fa fa-folder"></i>
            <span>&nbsp;Slect Folder</span>
          </span>
        </button>
        <div class="vr"></div>
        <button
          name="torrent"
          class="btn button text-nowrap"
          type="button"
          @click="selectFile()"
        >
          <i class="fas fa-file"></i>&nbsp;Select File
        </button>
      </div>
      <div class="hstack gap-3">
        <label for="output" class="col-form-label text-nowrap">Output</label>
        <input
          type="text"
          class="form-control inp"
          v-model="formData.output"
          id="output"
          name="output"
          placeholder="path/to/content"
        />
        <button
          name="torrent"
          class="btn button text-nowrap"
          type="button"
          @click="selectFile()"
        >
          <span class="icon">
            <i class="fas fa-file-import"></i>
          </span>
          <span>&nbsp;Save Path</span>
        </button>
      </div>
      <hr />
      <div class="hstack gap-3 my-3">
        <label
        for="pieceLength"
        class="form-control-label text-nowrap">
        Piece Length
        </label>
        <select
          name="pieceLength"
          id="pieceLength"
          class="form-select"
          v-model="formData.pieceLength"
        >
          <option v-for="size in sizes" :value="size.Size" :key="size.ID">
            {{ size.Size }}
          </option>
        </select>
        <div class="vr"></div>
        <div class="form-check">
          <input
            type="checkbox"
            name="private"
            class="form-check-input inp"
            id="private"
            v-model="formData.privat"
          />
          <label class="form-check-label" for="private">Private</label>
        </div>
      </div>
      <div class="hstack gap-4 my-4">
        <label>Meta Version</label>

          <div class="form-check mx-3">
            <input
            type="radio"
            class="form-check-input"
            id="1"
            value="1"
            v-model="formData.version"
          />
          <label for="1" class="form-check-label">v1</label>
        </div>
        <div class="form-check mx-3">
          <input
            type="radio"
            class="form-check-input"
            id="2"
            value="2"
            v-model="formData.version"
          />
          <label for="2" class="radio">v2</label>
        </div>
        <div class="form-check mx-3">
          <input
            type="radio"
            class="form-check-input"
            id="hybrid"
            value="hybrid"
            v-model="formData.version"
          />
          <label for="hybrid" class="form-check-label">hybrid</label>
        </div>
      </div>
      <div class="hstack gap-4 my-3">
        <div class="input-group">
          <span class="input-group-text">Source</span>
          <input
            type="text"
            class="form-control inp"
            aria-describedby="inputGroup-sizing-sm"
            placeholder="optional"
            name="source"
            id="source"
          />
        </div>
      </div>
      <div class="hstack gap-4 my-3">
        <div class="input-group">
          <span class="input-group-text">Comment</span>
          <input
            type="text"
            class="form-control inp"
            v-model="formData.comment"
            name="comment"
            placeholder="optional"
            id="comment"
          />
        </div>
      </div>
      <div class="hstack gap-4 my-3">
        <div class="input-group mb-3">
          <span class="input-group-text">Trackers</span>
          <textarea
            name="announce"
            id="announce"
            class="form-control inp"
            placeholder="https://example..."
            style="height: 100px"
            v-model="formData.announce"
          >
          </textarea>
        </div>
      </div>
      <div class="field">
        <button class="btn-primary btn" @click="submitFormData()" type="button">
          Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import image from "./../assets/torrentfile.png";

export default defineComponent({
  name: "TorrentForm",
  data() {
    return {
      title: "torrentfile",
      description: "Torrent file builder, checker, and reviewer.",
      date: Date(),
      image: image,
      formData: {
        privat: false,
        source: "",
        comment: "",
        path: "",
        output: "",
        announce: "",
        version: "",
        pieceLength: "",
      },
      element: "",
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
    };
  },
  methods: {
    fillElement() {
      let element: any = document.getElementById("filler");
      element.innerHTML =
        '<progress class="progress is-danger" max="100">30%</progress>';
      this.element = element;
    },
    selectFile() {
      let self: any = this;
      window.ipc.invoke("openFileExplorer", {}).then((result: string) => {
        self.formData.path = result;
        self.formData.output = result + ".torrent";
      });
    },
    selectFolder() {
      let self: any = this;
      window.ipc.invoke("openFolderExplorer", {}).then((result: string) => {
        self.formData.path = result;
        self.formData.output = result + ".torrent";
      });
    },
    async submitFormData() {
      const args = this.$data.formData;
      // console.log(size, args, pieceLength, version, announce)
      let pieceLength = 0;
      for (let i = 0; i < this.$data.sizes.length; i++) {
        if (this.$data.sizes[i].Size == args.pieceLength) {
          pieceLength = this.$data.sizes[i].ID;
          break;
        }
      }
      let version = parseInt(args.version);
      let announce = args.announce.split("\n");
      const params = [
        args.path,
        announce,
        pieceLength,
        args.privat,
        args.comment,
        args.source,
        args.output,
      ];
      this.fillElement();
      const result = await window.ipc
        .invoke("createTorrent", version, params)
        .then((result: any) => {
          return result;
        });
    },
  },
});
</script>

<style></style>
