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
    <v-card v-if="tab === 0" class="mt-10">
      <data-set-layout />
    </v-card>
  </section>
</template>

<script>
import DataSetLayout from '@/components/data-set/DataSetLayout.vue'

export default {
  components: {
    DataSetLayout,
  },
  data() {
    return {
      tab: 0,
      tabItems: ['DataSet', 'Learning', 'Judge'],
    }
  },
  computed: {},
  methods: {},
}
</script>

<style lang="scss">
.wrap {
  max-width: 900px;
  margin: auto;
}
</style>
