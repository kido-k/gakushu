<template>
  <section>
    <h1 class="layout__title">images</h1>
    <v-row class="image__layout">
      <v-col
        v-for="(path, index) in imagePathList"
        :key="index"
        class="d-flex child-flex"
        cols="4"
      >
        <v-card class="image__card">
          <v-img
            class="image__content"
            :src="require('~/assets/images/' + path)"
          />
        </v-card>
      </v-col>
    </v-row>
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

<style lang="scss">
.layout {
  &__title {
    font-size: 48px;
  }
}

.image {
  &__layout {
    padding: 20px;
  }
  &__card {
    margin: auto;
    padding: 20px;
  }
  &__content {
    width: 200px;
    margin: 10px;
    text-align: center;
  }
}
</style>
