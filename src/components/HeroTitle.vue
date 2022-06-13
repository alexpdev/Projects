<template>
  <section id="HeroTitle" class="p-2">
    <div class="bg-dark text-secondary px-2 py-2 text-center">
      <div class="hstack">
        <img :src="image" style="max-width: 15%;" class="img-thubnail" />
        <h2 class="subtitle mx-3 text-light my-1">{{ description }}</h2>
      </div>
    </div>
  </section>
</template>


<script lang="ts">
import { defineComponent } from "vue";
import image from "./../assets/torrentfile.png";

export default defineComponent({
  name: 'HeroTitle',
  data() {
    return {
      title: 'torrentfile',
      description: "Torrent file builder, checker, and reviewer.",
      image: image,
    }
  }
})
</script>
