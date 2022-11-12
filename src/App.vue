<template>
<<<<<<< HEAD
  <img alt="Vue logo" src="./assets/logo.png">
  <OsLicensor/>
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import OsLicensor from './components/OsLicensor.vue'
console.log("App.Vue")
export default {
  name: 'App',
  components: {
    OsLicensor,
    HelloWorld
  }
}
</script>

<style>
=======
  <HeroTitle />
  <TorrentForm/>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TorrentForm from "./components/TorrentForm.vue";
import HeroTitle from "./components/HeroTitle.vue";
import TabBar from "./components/TabBar.vue";
import ProgressBar from "./components/ProgressBar.vue";

export default defineComponent({
  name: "App",
  components: {
    HeroTitle,
    TorrentForm,
    TabBar,
    ProgressBar
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
>>>>>>> 28e86b5a6d04e848413a728d58194aec7e587120
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
<<<<<<< HEAD
  color: #2c3e50;
  margin-top: 60px;
=======
  color: #fff;
>>>>>>> 28e86b5a6d04e848413a728d58194aec7e587120
}
</style>
