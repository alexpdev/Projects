<template>
  <section id="HeroTitle" class="p-2">
    <div class="bg-dark text-secondary px-2 py-3 text-center">
      <div class="py-2">
        <figure class="image">
            <img :src="image" style="max-width: 50%;" class="img-thubnail mx-auto" />
        </figure>
        <h3 class="subtitle">{{ description }}</h3>
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
