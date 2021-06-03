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
    <v-card v-if="tab === 0" flat class="mt-10">
      <data-set-layout />
    </v-card>
    <v-card v-else-if="tab === 1" flat class="mt-10">
      <learning-layout />
    </v-card>
  </section>
</template>

<script>
import DataSetLayout from '@/components/data-set/DataSetLayout.vue'
import LearningLayout from '@/components/learning/LearningLayout.vue'

export default {
  components: {
    DataSetLayout,
    LearningLayout,
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
      this.tab = sessionStorage.getItem('gakushuTab')
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
