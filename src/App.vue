<template>
  <HeroTitle />
  <TabBar />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TorrentForm from "./components/TorrentForm.vue";
import HeroTitle from "./components/HeroTitle.vue";
import TabBar from "./components/TabBar.vue";

export default defineComponent({
  name: "App",
  components: {
    HeroTitle,
    TorrentForm,
    TabBar,
  },
  data: () => {
    return {};
  },
  methods: {},
  setup() {},
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
