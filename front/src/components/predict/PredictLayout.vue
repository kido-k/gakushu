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

    <template v-if="selectModel">
      <h2>予測する画像</h2>
      <v-layout class="setting-group" align-center justify-center>
        <v-hover>
          <template #default="{ hover }">
            <v-card flat class="predict__image">
              <div v-if="base64Image">
                <v-img :src="base64Image" :aspect-ratio="1" />
              </div>
              <div v-else class="no-image">
                <p class="no-image__text">NO IMAGE</p>
              </div>
              <v-fade-transition>
                <v-overlay v-if="hover" :absolute="true">
                  <v-btn large @click="selectImage"> SELECT IMAGE </v-btn>
                  <v-btn
                    v-if="base64Image"
                    fab
                    color="#808080"
                    small
                    class="ml-2"
                    @click="deletImage"
                  >
                    <v-icon color="#fff">mdi-minus</v-icon>
                  </v-btn>
                </v-overlay>
              </v-fade-transition>
            </v-card>
          </template>
        </v-hover>
        <div v-if="predictResult" class="predict__result">
          <p class="predict__result__text">{{ predictResult }}</p>
          <v-layout v-if="predict" justify-center>
            <chart
              :labels="chartLabels"
              :data="chartData"
              :options="chartOptions"
              :colors="chartColors"
              :styles="{ height: '350px', width: '350px' }"
            />
          </v-layout>
        </div>
      </v-layout>

      <input
        ref="inputImage"
        style="display: none"
        type="file"
        accept="image/jpeg, image/jpg, image/png"
        @change="selectedFile()"
      />
      <v-btn
        :disabled="!base64Image || !selectModel"
        large
        outlined
        class="predict__button"
        @click="predictImage"
      >
        PREDICT
      </v-btn>
    </template>
  </section>
</template>

<script>
import Chart from '@/components/common/Chart.vue'

export default {
  components: {
    Chart,
  },
  data() {
    return {
      selectModel: null,
      modelData: null,
      selectModelList: [],
      base64Image: null,
      progress: false,
      overlay: false,
      learningRef: null,
      predictResult: null,
      chartData: [],
      chartLabels: [],
      chartColors: [],
      chartOptions: {
        maintainAspectRatio: false,
        animation: {
          duration: 1500,
          easing: 'easeInOutCubic',
        },
      },
      baseChartColor: [
        'blue',
        'green',
        'red',
        'yellow',
        'pink',
        'skyblue',
        'gray',
        'purple',
      ],
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
      return learningData
    },
  },
  watch: {
    selectModel() {
      if (this.selectModel) {
        this.learningRef = this.$firebase
          .database()
          .ref('results/learning/' + this.selectModel)
        if (this.predict) this.updatePredictResult()
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
    deletImage() {
      this.base64Image = null
      this.predictResult = null
      this.learningRef.child('predict').set({})
    },
    async selectedFile() {
      this.progress = true
      const imageFile = this.$refs.inputImage.files[0]
      this.base64Image = await this.getBase64(imageFile)
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
          if (this.predict) this.updatePredictResult()
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
    updatePredictResult() {
      this.base64Image = this.predict.imageUrl
      this.predictResult = this.predict.result
      const predictDetail = this.predict.predictDetail

      if (predictDetail) {
        this.chartLabels = Object.keys(predictDetail) || []
        this.chartData = []
        Object.keys(predictDetail).forEach((key) => {
          this.chartData.push(predictDetail[key])
        })
        this.chartColors = this.baseChartColor.slice(0, this.chartLabels.length)
      }
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
  &__main {
    width: 350px;
    margin: auto;
  }
  &__image {
    width: 350px;
    margin: auto;
  }
  &__button {
    margin: 30px 0;
    padding: 30px !important;
  }
  &__result {
    width: 350px;
    &__text {
      font-size: 24px;
      font-weight: bold;
    }
    &__detail {
      font-size: 14px;
      margin: 0 10px 0 0;
    }
  }
}

.no-image {
  width: 350px;
  height: 350px;
  background-color: rgba(0, 0, 0, 0.1);
  margin: auto;
  &__text {
    padding-top: 140px;
    font-size: 20px;
  }
}

.setting-group {
  padding: 40px;
  border-radius: 10px;
  border: 2px solid;
  margin: 0 0 20px 0;
}
</style>
