<template>
  <div class="container mt-5">
    <form id="torrentform">
      <div class="row">
        <div class="col-10 form-floating">
          <input
            class="form-control inp"
            type="text"
            id="path"
            placeholder="*.torrent"
            v-model="formData.path"
          />
          <label for="path">Path</label>
        </div>
        <div class="col-2 ">
          <div class="btn-group-vertical mt-3">
            <button
              name="torrent"
              class="btn button px-4 py-0"
              type="button"
              @click="selectFolder()"
            >
              <span class="icon">
                <i class="fas fa-folder-open"></i>
              </span>
              <span> Folder</span>
            </button>
            <button
              name="torrent"
              class="btn button px-4 py-0"
              type="button"
              @click="selectFile()"
            >
              <span class="icon">
                <i class="fas fa-file-import"></i>
              </span>
              <span> &nbsp;File</span>
            </button>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-10">
          <div class="form-floating">
            <input
              type="text"
              class="form-control inp"
              v-model="formData.output"
              id="output"
              name="output"
              placeholder="path/to/content"
            />
            <label for="output">Save To</label>
          </div>
        </div>
        <div class="col-2">
          <button
            name="torrent"
            class="btn button mt-3 py-2 px-4"
            type="button"
            @click="selectFile()"
          >
            <span class="icon">
              <i class="fas fa-file-import"></i>
            </span>
            <span>File</span>
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="form-floating">
            <input
              type="text"
              class="form-control inp"
              v-model="formData.comment"
              name="comment"
              placeholder="optional"
              id="comment"
            />
            <label for="comment">Comment</label>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="form-floating">
            <input
              type="text"
              class="form-control inp"
              placeholder="optional"
              name="source"
              id="source"
            />
            <label for="source">Source</label>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="form-floating">
            <textarea
              name="announce"
              id="announce"
              class="form-control inp"
              placeholder="https://example..."
              style="height: 100px"
              v-model="formData.announce"
            >
            </textarea>
            <label for="announce">Trackers</label>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-2">
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
        <div class="col-6">
          <div class="form-floating">
            <select
              name="pieceLength"
              id="pieceLength"
              class="form-control inp"
              placeholder="..."
              v-model="formData.pieceLength"
            >
              <label for="pieceLength" class="label">Piece Length</label>
              <option v-for="size in sizes" :value="size.Size" :key="size.ID">
                {{ size.Size }}
              </option>
            </select>
          </div>
        </div>
        <div class="col-4">
          <div class="btn-group-vertical">
            <input
              type="radio"
              class="radio"
              id="1"
              value="1"
              v-model="formData.version"
            />
            <input
              type="radio"
              class="radio"
              id="2"
              value="2"
              v-model="formData.version"
            />
            <label for="1" class="radio">1</label>
            <input
              type="radio"
              class="radio"
              id="hybrid"
              value="hybrid"
              v-model="formData.version"
            />
            <label for="2" class="radio">2</label>
            <label for="hybrid" class="radio">hybrid</label>
          </div>
        </div>
      </div>
      <div class="field">
        <button class="button btn" @click="submitFormData()" type="button">
          Submit
        </button>
      </div>
    </form>
  </div>
  <section class="section">
    <div id="filler" class="box">
      {{ element }}
    </div>
  </section>
  <section class="section">
    <div class="box">
      <p>{{ JSON.stringify(formData, null, 2) }}</p>
    </div>
  </section>
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
        path: "...",
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

<style>
.form-control {
  margin-top: 10px;
  margin-bottom: 10px;
}
.inp {
  background: #389;
}
.button {
  border: 1px solid #f64;
}
</style>
