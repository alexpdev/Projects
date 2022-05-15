<template>
<section class="hero is_primary">
  <div class="hero-body">
    <div class="container">
      <span>
        <h1 class="title">{{ title }}</h1>
        <h3>{{ date }}</h3>
      </span>
      <h2 class="subtitle">{{ description }}</h2>
    </div>
  </div>
</section>
<div class="block">
  <form action="">
    <div class="field">
      <label for="path" class="label">Path</label>
      <input
      id="path"
      type="text"
      class="input"
      v-model="formData.path"
      placeholder="/path/to/torrent/content">
    </div>
    <div class="field">
      <label for="output" class="label">Save To</label>
      <input
      type="text"
      class="input"
      v-model="formData.output"
      id="output"
      name="output"
      placeholder="/path/to/save/location.torrent">
    </div>
    <div class="field">
      <label for="comment">Comment</label>
      <input
      type="text"
      class="input"
      v-model="formData.comment"
      name="comment"
      id="comment">
    </div>
    <div class="field">
      <label class="label" for="source">Source</label>
      <input type="text" class="input" name="source" id="source">
    </div>
    <div class="field">
      <label class="label" for="announce">Trackers</label>
      <textarea name="announce" id="announce" cols="30" rows="10"></textarea>
    </div>
    <div class="field">
      <label class="label" for="private">Private</label>
      <input
      type="checkbox"
      name="private"
      id="private"
      v-model="formData.privat">
    </div>
    <div class="field">
      <label for="pieceLength" class="label">Piece Length</label>
      <select
      name="pieceLength"
      id="pieceLength"
      class="select"
      v-model="formData.pieceLength">
        <option
        v-for="size in formData.sizes"
        :value="formData.pieceLength"
        :key="size">{{ size }}</option>
      </select>
    </div>
    <div class="field">
        <label for="version" class="label">Bittorrent Version</label>
        <input
        type="radio"
        class="radio"
        id="1"
        value="1"
        v-model="formData.version">
        <label for="1" class="radio">1</label>
        <input
        type="radio"
        class="radio"
        id="2"
        value="2"
        v-model="formData.version">
        <label for="2" class="radio">2</label>
        <input
        type="radio"
        class="radio"
        id="hybrid"
        value="hybrid"
        v-model="formData.version">
        <label for="hybrid" class="radio">hybrid</label>
    </div>
    <div class="field">
      <button
      class="button is-info is-outlined"
      @click="submitFormData" >
        Submit
      </button>
    </div>
  </form>
  <section class="section">
    <div class="box">
      <p>{{ JSON.stringify(formData, null, 2) }}</p>
    </div>
  </section>
</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "TorrentForm",
  data() {
    return {
      title: "torrentfile",
      description: "Torrent file builder, checker, and reviewer.",
      date: Date(),
      formData: {
        privat: false,
        source: "",
        comment: "",
        path: "",
        output: "",
        announce: "",
        version: "",
        pieceLength: "",
        sizes: ""
      }
    }
  },
  methods: {
    submitFormData () {
      return
    }
  }
})
</script>
