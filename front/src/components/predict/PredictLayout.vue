<template>
  <section class="predict">
    <h2>学習モデル</h2>
    <div class="predict__model setting-group">
      <v-select
        v-model="selectModel"
        :items="selectModelList"
        label="select model"
        outlined
        hide-details
        class="predict__model__list"
      />
    </div>

    <h2>予測する画像</h2>
    <div class="setting-group">
      <v-hover>
        <template #default="{ hover }">
          <v-card flat class="predict__image">
            <div v-if="base64Image">
              <v-img :src="base64Image" :aspect-ratio="16 / 9" />
            </div>
            <div v-else class="no-image">
              <p class="no-image__text">NO IMAGE</p>
            </div>
            <v-fade-transition>
              <v-overlay v-if="hover" :absolute="true">
                <v-btn large @click="selectImage"> SELECT IMAGE </v-btn>
              </v-overlay>
            </v-fade-transition>
          </v-card>
        </template>
      </v-hover>
    </div>

    <input
      ref="inputImage"
      style="display: none"
      type="file"
      accept="image/jpeg, image/jpg, image/png"
      @change="selectedFile()"
    />
    <v-btn
      :disabled="!imageFile || !selectModel"
      large
      outlined
      class="predict__button"
      @click="predictImage"
    >
      PREDICT
    </v-btn>
    <div class="setting-group mb-10">
      <p class="predict__result">{{ predictResult }}</p>
      <v-layout v-if="predict" justify-center>
        <div v-for="(key, index) in Object.keys(predict)" :key="index">
          <span
            v-if="key !== 'result' && key !== 'imageUrl'"
            class="predict__result__detail"
          >
            {{ key }}: {{ predict[key] }}%
          </span>
        </div>
      </v-layout>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      selectModel: null,
      modelData: null,
      selectModelList: [],
      imageFile: null,
      base64Image: null,
      progress: false,
      overlay: false,
      learningRef: null,
      predictResult: null,
    }
  },
  computed: {
    predict() {
      if (!this.learningRef) return
      let learningData = null
      this.learningRef.on('value', (snapshot) => {
        learningData = snapshot.val()
      })
      learningData = learningData ? learningData.predict : {}
      this.updatePredictResult(learningData)
      return learningData
    },
  },
  watch: {
    selectModel() {
      if (this.selectModel) {
        this.learningRef = this.$firebase
          .database()
          .ref('results/learning/' + this.selectModel)
      }
    },
  },
  mounted() {
    this.updateModelList()
  },
  methods: {
    selectImage() {
      this.$refs.inputImage.click()
    },
    async selectedFile() {
      this.progress = true
      this.imageFile = this.$refs.inputImage.files[0]
      this.base64Image = await this.getBase64(this.imageFile)
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
      })
    },
    updateModelList() {
      this.$firebase
        .database()
        .ref('results/learning')
        .once('value', (snapshot) => {
          this.modelData = snapshot.val()
          this.selectModelList = Object.keys(this.modelData)
        })
    },
    predictImage() {
      const predictUrl = 'http://localhost:5000/predict'
      this.$postApi(
        predictUrl,
        (response) => {
          this.predictResult = response
        },
        (error) => {
          throw error
        },
        {
          predict_image_file: this.base64Image,
          model_name: this.selectModel,
          classes: this.modelData[this.selectModel].lerningCategories,
        }
      )
    },
    updatePredictResult(learningData) {
      this.base64Image = learningData.imageUrl
      this.predictResult = learningData.result
    },
  },
}
</script>

<style lang="scss" scoped>
.predict {
  text-align: center;
  &__model {
    &__list {
      max-width: 400px;
      margin: auto;
    }
  }
  &__image {
    width: 500px;
    margin: auto;
  }
  &__button {
    margin: 30px 0;
    padding: 30px !important;
  }
  &__result {
    font-size: 24px;
    font-weight: bold;
    &__detail {
      font-size: 14px;
      margin: 0 10px 0 0;
    }
  }
}

.no-image {
  width: 500px;
  height: 281px;
  background-color: rgba(0, 0, 0, 0.1);
  margin: auto;
  &__text {
    padding-top: 120px;
    font-size: 24px;
  }
}

.setting-group {
  padding: 40px;
  border-radius: 10px;
  border: 2px solid;
  margin: 0 0 20px 0;
}
</style>
