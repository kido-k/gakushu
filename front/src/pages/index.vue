<template>
  <section class="image">
    <h1 class="image__title">学習用画像</h1>
    <div class="image__search">
      <p>新しく画像を取得する</p>
      <div v-if="resultStatus" class="image__status">
        <v-simple-table>
          <template #default>
            <thead>
              <tr>
                <th class="text-left">検索ワード</th>
                <th class="text-left">ステータス</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(key, index) in Object.keys(resultStatus)"
                :key="index"
              >
                <td>{{ key }}</td>
                <td>{{ resultStatus[key].getImage }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
      <v-layout align-center>
        <v-text-field
          v-model="searchName"
          label="検索ワード"
          outlined
          type="text"
          hide-details
        />
        <v-text-field
          v-model="maxGetNumber"
          label="最大取得件数"
          type="number"
          class="image__max-get-number"
          hide-details
        />
        <v-btn
          class="image__search__button"
          large
          color="primary"
          :disabled="!searchName"
          @click="getImage"
        >
          取得
        </v-btn>
      </v-layout>
    </div>
    <div class="image__result">
      <v-layout max-width="400px">
        <v-select
          v-model="selectResult"
          :items="searchList"
          class="image__result__select"
        />
        <v-btn
          class="image__search__button"
          large
          color="primary"
          @click="updateImageList"
        >
          更新
        </v-btn>
      </v-layout>
      <v-row v-if="selectResult" class="image__result__layout">
        <v-col
          v-for="(image, index) in selectImageData"
          :key="index"
          class="d-flex child-flex"
          cols="4"
        >
          <v-card class="image__result__card">
            <v-img class="image__result__content" :src="image.path" />
          </v-card>
        </v-col>
      </v-row>
    </div>
  </section>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      searchName: '',
      maxGetNumber: 50,
      imageData: {},
      searchList: [],
      selectResult: null,
      resultRef: null,
    }
  },
  computed: {
    selectImageData() {
      if (!this.selectResult) return []
      const selectImage = this.imageData[this.selectResult]
      if (!selectImage) return []

      const selectImageList = []
      Object.keys(selectImage).forEach((key) => {
        selectImageList.push(selectImage[key])
      })
      return selectImageList
    },
    resultStatus() {
      if (!this.resultRef) return
      let status = null
      this.resultRef.on('value', (snapshot) => {
        status = snapshot.val()
      })
      return status
    },
  },
  mounted() {
    this.resultRef = this.$firebase.database().ref('results/images')
  },
  methods: {
    getImage() {
      this.resultRef.child(this.searchName).set({
        getImage: 'start',
      })
      const getImageUrl =
        'http://localhost:5000/get_images' +
          '?search_name=' +
          this.searchName +
          '&max_get_number=' +
          this.maxGetNumber || 50
      this.$getApi(getImageUrl)
      this.searchName = ''
      this.maxGetNumber = 50
    },
    updateImageList() {
      this.$firebase
        .database()
        .ref('images')
        .once('value', (snapshot) => {
          this.imageData = snapshot.val()
          this.searchList = Object.keys(this.imageData)
        })
    },
  },
}
</script>

<style lang="scss">
.image {
  &__title {
    font-size: 48px;
    margin: 0 0 20px 0;
  }
  &__status {
    margin: 10px 0;
  }
  &__max-get-number {
    margin: 0 10px 0 30px !important;
    max-width: 100px !important;
  }
  &__search {
    padding: 20px;
    margin: 0 0 20px 0;
    border-radius: 10px;
    border: 2px solid #2196f3;
    &__button {
      margin: 0 0 0 20px;
    }
  }

  &__result {
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #2196f3;
    &__select {
      width: 200px;
    }
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
}
</style>
