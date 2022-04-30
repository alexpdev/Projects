<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <form @sumbit.prevent="submit">
          <div class="column is-full">
            <div class="field">
              <label for="path" class="label">Path</label>
              <div class="control">
              <input type="text" v-model="form.path" name="path" id="path" class="form-field input">
              </div>
            </div>
          </div>
          <div class="column is-full">
            <div class="field">
              <label class="label" for="announce">Trackers</label>
              <div class="control">
                <textarea class="textarea" v-model="form.announce" name="announce" id="announce" cols="50" rows="6"></textarea>
              </div>
            </div>
          </div>
          <div class="column is-full">
            <div class="column is-half">
              <div class="field">
                <div class="control">
                  <label for="priv" class="checkbox">
                    Private
                    <input type="checkbox" class="checkbox" v-model="form.priv" id="priv" name="priv">
                  </label>
                </div>
              </div>
            </div>
            <div class="column is-half">
              <div class="field">
                <div class="control">
                  <label class="radio">
                    Meta Version
                    <label class="radio" >
                    <input type="radio" name="mversion" v-model="form.mversion">
                    1
                    </label>
                    <label class="radio">
                    <input type="radio" name="mversion" v-model="form.mversion">
                    2
                    </label>
                    <label class="radio">
                    <input type="radio" name="mversion" v-model="form.mversion">
                    hybrid
                    </label>
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-full">
            <div class="field">
              <label for="source" class="label">Source</label>
              <div class="control">
              <input type="text" v-model="form.source" name="source" id="source" class="form-field input">
              </div>
            </div>
          </div>
          <div class="column is-full">
            <div class="field">
              <label class="label" for="comment">Comment</label>
              <div class="control">
                <textarea class="textarea" v-model="form.comment" name="comment" id="comment" cols="50" rows="6"></textarea>
              </div>
            </div>
          </div>
          </div>
          <div class="column is-full">
            <div class="field">
              <label for="out" class="label">Save To</label>
              <div class="control">
              <input type="text" v-model="form.source" name="source" id="source" class="form-field input">
              </div>
            </div>
          </div>
          <div class="column">
            <div class="field">
              <input type="button"  value="submit">
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "TorrentForm",
  data() {
    return {
      form: {
        path: "",
        announce: "",
        priv: "",
        mversion: "",
        out: "",
        comment: "",
        source: "",
      }
    };
  },
  methods: {
    async submit() {
      const { path, announce, priv, mversion, out, comment, source } = this.form;
      if (!path) {
        alert("Path field required");
        return;
      }
      const {id} = this.$route.params;
      if (id) {
        await axios.put()
      }
    }
  }
}
</script>
