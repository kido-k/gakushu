<template>
  <section class="learning">
    <div class="learning__new-model">
      <v-btn
        large
        outlined
        class="learning__new-model__button"
        @click="dialog = true"
      >
        CREATE NEW MODEL
      </v-btn>
    </div>
    <div v-if="learningStatus" class="learning__status">
      <v-simple-table>
        <template #default>
          <thead>
            <tr>
              <th class="text-left">モデル名</th>
              <th class="text-left">ステータス</th>
              <th class="text-left">学習データ</th>
              <th class="text-left">削除</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(key, index) in Object.keys(learningStatus)"
              :key="index"
            >
              <td>{{ key }}</td>
              <td>{{ learningStatus[key].learningStatus }}</td>
              <td>
                <span
                  v-for="(category, learnIndex) in learningStatus[key]
                    .lerningCategories"
                  :key="learnIndex"
                >
                  <span v-if="learnIndex !== 0">,</span>
                  {{ category }}
                </span>
              </td>
              <td>
                <v-icon @click="deleteLearningModel(key)">mdi-delete</v-icon>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>
    <v-dialog v-model="dialog" max-width="650" persistent>
      <v-card class="pa-10" min-height="400">
        <create-model-dialog @closeDialog="dialog = false" />
      </v-card>
    </v-dialog>
  </section>
</template>

<script>
import CreateModelDialog from '@/components/learning/CreateModelDialog.vue'

export default {
  components: {
    CreateModelDialog,
  },
  data() {
    return {
      resultRef: null,
      dialog: false,
    }
  },
  computed: {
    learningStatus() {
      if (!this.resultRef) return
      let status = null
      this.resultRef.on('value', (snapshot) => {
        status = snapshot.val()
      })
      return status
    },
  },
  mounted() {
    this.resultRef = this.$firebase.database().ref('results/learning')
  },
  methods: {
    deleteLearningModel(modelName) {
      const deleteLearningModelUrl =
        'http://localhost:5000/delete_learning_model'
      this.progress = true
      this.$postApi(
        deleteLearningModelUrl,
        (_) => {
          this.progress = false
          const deleteResultRef = 'results/learning/' + modelName
          this.$firebase.database().ref(deleteResultRef).remove()
        },
        (error) => {
          this.progress = false
          throw error
        },
        {
          model_name: modelName,
        }
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.learning {
  &__new-model {
    font-size: 48px;
    margin: 0 0 20px 0;
    text-align: center;
    &__button {
      padding: 30px;
    }
  }
  &__status {
    padding: 20px;
    margin: 0 0 20px 0;
    border-radius: 10px;
    border: 2px solid;
    &__button {
      margin: 0 0 0 20px;
    }
  }
}
</style>
