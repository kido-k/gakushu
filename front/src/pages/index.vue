<template>
  <section>
    <h1>images</h1>
    <div v-for="(path, index) in imagePathList" :key="index">
      <v-img class="image" :src="require('~/assets/images/' + path)" />
    </div>
  </section>
</template>

<script>
import imageJson from '~/assets/imageList.json'

export default {
  components: {},
  data() {
    return {
      imagePathList: imageJson.result,
    }
  },
  mounted() {},
}
</script>

<style>
.image {
  width: 200px;
  margin: 10px;
}
</style>
