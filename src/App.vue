<template>
  <div id="root" class="container">
    <section class="section">
      <div class="columns is-centered">
        <div class="column is-10">
          <TorrentForm/>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">

import { defineComponent, reactive, ref, toRefs } from "vue";
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
