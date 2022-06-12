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
          @click="selectOutput()"
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
            v-model="formData.private_"
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
            v-model="formData.source"
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
      <div class="row">
        <div class="col-12 col">
          <p>{{ complete }}</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface SelectSize {
  ID: number;
  Size: string;
}

export default defineComponent({
  name: "TorrentForm",
  data() {
    var sizes: SelectSize[] = [];
    for (let i = 14; i < 29; i++){
      let value = Math.pow(2,i);
      let num = value / Math.pow(2,10);
      let text: string;
      if (num >= 1000){
        text =  value / Math.pow(2,20) + " MiB";
      } else {
        text = num + " KiB";
      }
      sizes.push({ID: i, Size: text});
    }
    return {
      formData: {
        private_: false,
        source: "",
        comment: "",
        path: "",
        output: "",
        announce: "",
        version: "",
        pieceLength: "",
      },
      element: "",
      sizes: sizes,
      complete: ""
    };
  },
  methods: {
    selectFile() {
      let self: any = this;
      window.ipc.invoke("openFileExplorer", {}).then((result: string) => {
        self.formData.path = result;
        self.formData.output = result + ".torrent";
      });
    },
    selectOutput() {
      let self: any = this;
      window.ipc.invoke("openFileExplorer", {}).then((result: string) => {
        self.formData.ouput = result;
      })
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
        args.private_,
        args.comment,
        args.source,
        args.output,
      ];
      const result = await window.ipc
        .invoke("createTorrent", version, params)
        .then((result: any) => {
          return result;
        });
        console.log(result);
        this.complete = "complete";
    },
  },
});
</script>

<style>
.button {
  background-color: rgb(2, 77, 124);
  color: rgb(219, 208, 144);
  border: 1px solid #E63;
}

</style>
