<script>
import { Doughnut } from 'vue-chartjs'

export default {
  extends: Doughnut,
  props: {
    labels: {
      type: Array,
      default: () => [],
    },
    data: {
      type: Array,
      default: () => [],
    },
    options: {
      type: Object,
      default: () => ({}),
    },
    colors: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chartData: {},
    }
  },
  mounted() {
    this.chartData.labels = this.labels
    this.chartData.datasets = [
      { data: this.data, backgroundColor: this.colors },
    ]
    this.renderChart(this.chartData, this.options)
  },
}
</script>
