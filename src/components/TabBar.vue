<template>
  <nav class="nav justify-content-center nav-fill" id="tabbar">
    <ul class="nav nav-tabs current">
      <li class="nav-item">
        <a id="create" class="nav-link active" aria-current="page" @click="createTab()">Create</a>
      </li>
    </ul>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a id="info" class="nav-link" @click="infoTab()">Info</a>
      </li>
    </ul>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a id="recheck" class="nav-link" @click="recheckTab()">Recheck</a>
      </li>
    </ul>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a id="edit" class="nav-link" @click="editTab()" >Edit</a>
      </li>
    </ul>
  </nav>

</template>


<script lang="ts">
import {defineComponent} from "vue";
import TorrentForm from "./TorrentForm.vue"

export default defineComponent({
  name: "TabBar",
  components: {
    TorrentForm
  },
  data() {
    return {
      title: "tabs"
    };
  },
  methods: {
    editTab() {
      let edittab = document.getElementById("edit");
      if (edittab){
        if (edittab.hasAttribute("active"))
          return;
      }
    },
    createTab() {
      let edittab = document.getElementById("create");
      if (edittab){
        if (edittab.hasAttribute("active"))
          return;
      }
    },
    infoTab() {
      let edittab = document.getElementById("info");
      if (edittab){
        if (edittab.hasAttribute("active"))
          return;
      }
    },
    recheckTab() {
      let edittab = document.getElementById("recheck");
      if (edittab){
        if (edittab.hasAttribute("active"))
          return;
      }
    }
  },
})
</script>
