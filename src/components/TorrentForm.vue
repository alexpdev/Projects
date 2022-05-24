<template>
  <section id="torrentform" class="hero is-info">
    <div class="hero-body">
      <div class="container">
        <figure class="image">
          <img :src="image" />
        </figure>
        <h3 class="subtitle">{{ description }}</h3>
      </div>
    </div>
  </section>
    <form id="torrentform">
      <label for="path" class="label">Path</label>
      <div class="field has-addons">
        <input
        class="input"
        type="text"
        id="path"
        v-model="formData.path"
        readonly/>
        <button
          name="torrent"
          class="button is-info"
          type="button"
          @click="selectFolder()"
        >
          <span class="icon">
            <i class="fas fa-folder-open"></i>
          </span>
          <span> Select Folder</span>
        </button>
        <button
          name="torrent"
          class="button is-primary"
          type="button"
          @click="selectFile()"
        >
          <span class="icon">
            <i class="fas fa-file-import"></i>
          </span>
           <span>Select File</span>
        </button>
      </div>
      <label for="output" class="label">Save To</label>
      <div class="field has-addons">
          <input
            type="text"
            class="input"
            v-model="formData.output"
            id="output"
            name="output"
            readonly
          />
        <button
          name="torrent"
          class="button is-primary"
          type="button"
          @click="selectFile()"
        >
          <span class="icon">
            <i class="fas fa-file-import"></i>
          </span>
          <span>Select File</span>
        </button>
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
          rows="4"
          v-model="formData.announce"
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
                v-for="size in sizes"
                :value="size.Size"
                :key="size.ID"
              >
                {{ size.Size }}
              </option>
            </select>
          </div>
        </div>
        <div class="column is-4">
          <div class="field">
            <label for="version" class="label">Meta-Version</label>
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
          @click="submitFormData()"
          type="button"
        >
          Submit
        </button>
      </div>
    </form>
    <section class="section">
      <div id='filler' class="box">
        {{element}}
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
      element.innerHTML = '<progress class="progress is-danger" max="100">30%</progress>';
      this.element = element
    },
    selectFile() {
      let self:any = this;
      window.ipc.invoke("openFileExplorer", {}).then((result: string) => {
        self.formData.path = result;
        self.formData.output = result + '.torrent'
      })
    },
    selectFolder() {
      let self: any = this;
      window.ipc.invoke("openFolderExplorer", {}).then((result: string) => {
        self.formData.path = result;
        self.formData.output = result + '.torrent';
      })
    },
    async submitFormData() {
      const args = this.$data.formData;
      // console.log(size, args, pieceLength, version, announce)
      let pieceLength = 0;
      for (let i = 0; i < this.$data.sizes.length; i++){
        if (this.$data.sizes[i].Size == args.pieceLength){
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
      const result = await window.ipc.invoke(
        "createTorrent", version, params
        ).then((result: any) => {
        return result;
      })
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
