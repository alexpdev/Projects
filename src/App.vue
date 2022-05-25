<template>
  <div id="root" class="container">
    <section class="section" id="section">
      <div class="tabs is-medium">
        <ul>
          <li class="is-active"><a>Pictures</a></li>
          <li><a>Music</a></li>
          <li><a>Videos</a></li>
          <li><a>Documents</a></li>
        </ul>
      </div>
      <div class="columns is-centered">
        <div class="column is-10">
          <TorrentForm/>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TorrentForm from "./components/TorrentForm.vue";


export default defineComponent({
  name: "App",
  components: {
    TorrentForm
  },
  data: () => {
    return {};
  },
  methods: {
  },
  setup() {
  }
});
</script>

<style>
#section {
  padding-top: 6px;
  padding-left: 2px;
  padding-right: 2px;
}
body {
  background-color: #39434d;
}
.label {
  color: white;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
}
</style>
