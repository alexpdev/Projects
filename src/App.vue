<template>
  <div id="root" class="container">
    <section class="section">
      <div class="columns">
        <div class="column is-9 align-center">
          <TorrentForm/>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, toRefs } from "vue";
import { itunesSearch } from "./services/iTunesAPI";
import { ItunesTypes } from "./types/ItunesTypes.interface";
import TheShowAlbum from "./components/TheShowAlbum.vue";
import TorrentForm from "./components/TorrentForm.vue";


export default defineComponent({
  name: "App",
  components: {
    TheShowAlbum,
    TorrentForm
  },
  data: () => {
    return {
      data: {} as ItunesTypes,
      searchText: ""
    };
  },
  methods: {
    async searchItunes(search: string): Promise<void> {
      const value = await itunesSearch(search);
      this.data = value;
      console.log("data", value);
    }
  },
  setup() {
    let albums = reactive<{ data: ItunesTypes }>({ data : {} });
    let searchText = ref("");
    const searchItunes = async (search: string): Promise<void> => {
      const value = await itunesSearch(search);
      albums.data = value;
      console.log("data", albums);
    };
    return { searchItunes, ...toRefs(albums), searchText };
  }
});
</script>

<style>
/* @import "bulma/css/bulma.css"; */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#root {
  background-color: #555855;
  color: white;
}
.label {
  color: white;
}
</style>
