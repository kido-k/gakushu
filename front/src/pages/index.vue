<template>
  <section class="wrap">
    <div class="text-center justify-center py-6">
      <h1 class="font-weight-bold display-3 basil--text">GaKuShu</h1>
    </div>
    <v-tabs v-model="tab" background-color="transparent" color="basil" grow>
      <v-tab v-for="item in tabItems" :key="item">
        {{ item }}
      </v-tab>
    </v-tabs>
    <div v-if="tab === 0" class="mt-10">
      <data-set-layout />
    </div>
    <div v-else-if="tab === 1" class="mt-10">
      <learning-layout />
    </div>
    <div v-else-if="tab === 2" class="mt-10">
      <predict-layout />
    </div>
  </section>
</template>

<script>
import DataSetLayout from '@/components/data-set/DataSetLayout.vue'
import LearningLayout from '@/components/learning/LearningLayout.vue'
import PredictLayout from '@/components/predict/PredictLayout.vue'

export default {
  components: {
    DataSetLayout,
    LearningLayout,
    PredictLayout,
  },
  data() {
    return {
      tab: 0,
      tabItems: ['DataSet', 'Learning', 'Judge'],
    }
  },
  computed: {},
  watch: {
    tab() {
      sessionStorage.setItem('gakushuTab', this.tab)
    },
  },
  mounted() {
    if (sessionStorage.getItem('gakushuTab')) {
      this.tab = Number(sessionStorage.getItem('gakushuTab'))
    }
  },
  methods: {},
}
</script>

<style lang="scss" scoped>
.wrap {
  max-width: 900px;
  margin: auto;
}
</style>
