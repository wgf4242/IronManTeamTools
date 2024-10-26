<template>
  <h1>fuzz 像素信息, 需要传入起始点 间隔, 宽度</h1>
  <div style="padding: 10px">
    <span>start_x:<input type="number" v-model="start_x"> </span>
    <span>start_y:<input type="number" v-model="start_y"></span>
    <span>gap:<input type="number" v-model="gap"></span>
  </div>
  <FileDropComponent @changeObj="setFile" />

  <pre>{{ result }}</pre>

</template>

<script>
import FileDropComponent from '@/components/FileDropComponent.vue'
import { ref } from 'vue'
import { imgPixel } from '@/api/index.js'


export default {
  name: 'CryptoBinary',
  components: { FileDropComponent },
  setup() {
    const result = ref('')
    const start_x = ref('')
    const start_y = ref('')
    const gap = ref('')
    const setFile = async (file) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('start_x', start_x.value)
      formData.append('start_y', start_y.value)
      formData.append('gap', gap.value)
      result.value = await imgPixel(formData)
    }
    return {
      result, start_x, start_y, gap,
      setFile
    }
  }
}
</script>

<style scoped>
</style>
