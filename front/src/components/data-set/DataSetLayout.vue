<template>
  <section class="image">
    <div class="image__search">
      <div v-if="resultStatus" class="image__status">
        <v-simple-table>
          <template #default>
            <thead>
              <tr>
                <th class="text-left">検索ワード</th>
                <th class="text-left">ステータス</th>
                <th class="text-left">最大取得件数</th>
                <th class="text-left">取得件数</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(key, index) in Object.keys(resultStatus)"
                :key="index"
              >
                <td>{{ key }}</td>
                <td>{{ resultStatus[key].getImageStatus }}</td>
                <td>{{ resultStatus[key].maxGetNumber }}</td>
                <td>{{ resultStatus[key].getImageNumber }}</td>
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
          class="image__search__button text-button"
          outlined
          large
          :disabled="!searchName"
          @click="getImage"
        >
          GET
        </v-btn>
      </v-layout>
    </div>
    <div class="result">
      <v-layout align-center class="result__select">
        <v-select
          v-model="selectResult"
          :items="searchList"
          class="result__select__selector"
        />
        <v-btn
          class="result__update__button text-button"
          large
          outlined
          @click="updateImageList"
        >
          UPDATE
        </v-btn>
      </v-layout>
      <v-row v-if="selectResult" class="result__view__layout">
        <v-col
          v-for="(image, index) in selectImageData"
          :key="index"
          class="d-flex child-flex"
          cols="4"
        >
          <v-card class="result__view__card">
            <v-img class="result__view__content" :src="image.path" />
          </v-card>
        </v-col>
      </v-row>
    </div>
  </section>
</template>

<script>
export default {
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
    this.updateImageList()
    this.resultRef = this.$firebase.database().ref('results/images')
  },
  methods: {
    getImage() {
      this.resultRef.child(this.searchName).set({
        getImageStatus: 'start',
        maxGetNumber: this.maxGetNumber || 50,
        getImageNumber: 0,
      })
      this.deleteImageList()
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
    deleteImageList() {
      this.$firebase.database().ref('images').child(this.searchName).set({})
    },
  },
}
</script>

<style lang="scss" scoped>
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
    border: 2px solid;
    &__button {
      margin: 0 0 0 20px;
    }
  }
}

.result {
  padding: 20px;
  margin: 0 0 20px 0;
  border-radius: 10px;
  border: 2px solid;
  &__select {
    max-width: 500px;
  }
  &__update {
    &__button {
      margin: 0 0 0 20px;
    }
  }
  &__view {
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
