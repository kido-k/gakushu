<template>
  <section class="model-dialog">
    <h2 class="model-dialog__title">NEW MODEL</h2>
    <v-text-field
      v-model="modelName"
      label="モデル名"
      outlined
      type="text"
      hide-details
      class="model-dialog__name mt-8"
    />
    <v-select
      v-model="selectCategories"
      :items="images"
      label="分類したいカテゴリ"
      chips
      multiple
      outlined
      hide-details
      class="model-dialog__category mt-8"
    />
    <v-layout justify-end class="mt-5">
      <v-btn large outlined class="model-dialog__cancel" @click="closeDialg">
        CANCEL
      </v-btn>
      <v-btn
        :disabled="!modelName && !selectCategories"
        large
        outlined
        class="model-dialog__button ml-5"
        @click="addNewModel"
      >
        ADD MODEL
      </v-btn>
    </v-layout>
  </section>
</template>

<script>
export default {
  data() {
    return {
      modelName: null,
      selectCategories: null,
      images: [],
      imagesRef: null,
      validate: false,
    }
  },
  computed: {},
  mounted() {
    this.clearData()
    this.imagesRef = this.$firebase.database().ref('results/images')
    this.learningRef = this.$firebase.database().ref('results/learning')
    this.updateImages()
  },
  methods: {
    updateImages() {
      if (!this.imagesRef) return
      let result = null
      this.imagesRef.on('value', (snapshot) => {
        result = snapshot.val()
      })
      this.images = Object.keys(result)
    },
    addNewModel() {
      if (this.validate) return
      this.learningRef.child(this.modelName).set({
        learningStatus: 'start',
        lerningCategories: this.selectCategories,
      })
      this.postCreateModel()
      this.$emit('closeDialog')
      this.updateImages()
    },
    postCreateModel() {
      const learningUrl = 'http://localhost:5000/learning'
      this.$postApi(
        learningUrl,
        (_) => {
          this.updateImages()
        },
        (error) => {
          throw error
        },
        {
          file_name: this.modelName,
          classes: this.selectCategories,
        }
      )
    },
    closeDialg() {
      this.$emit('closeDialog')
    },
    clearData() {
      this.modelName = null
      this.selectCategories = null
    },
  },
}
</script>

<style lang="scss" scoped>
.model-dialog {
  &__title {
    text-align: center;
  }
}
</style>
