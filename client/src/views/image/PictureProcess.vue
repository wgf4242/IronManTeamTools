<template>
  <h1>图片处理</h1>
  <div class="container">
    <FileDropComponent @changeObj="setFile"/>
    <div class="input-group">
      <label>密钥:</label>
      <input v-model="key" type="text" placeholder="请输入密钥">
    </div>
    <div class="button-group">
      <button @click="processImage" :disabled="!fileObj">处理图片</button>
      <button @click="fixQRCode" :disabled="!fileObj">修复条形码</button>
    </div>

    <div class="result" v-if="result">
      <h3>处理结果:</h3>
      <table>
        <tr v-for="(value, key) in result" :key="key">
          <td class="key">{{ key }}:</td>
          <td class="value">{{ value }}</td>
        </tr>
      </table>
    </div>

    <div class="image-result" v-if="fixedImage">
      <h3>修复结果:</h3>
      <img :src="fixedImage" alt="Fixed QR Code">
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import FileDropComponent from '@/components/FileDropComponent.vue'

export default {
  name: 'PictureProcess',
  components: { FileDropComponent },
  setup() {
    const key = ref('')
    const result = ref('')
    const fileObj = ref(null)
    const fixedImage = ref(null)

    const setFile = (file) => {
      fileObj.value = file
      fixedImage.value = null
    }

    const processImage = async () => {
      if (!fileObj.value) return

      const formData = new FormData()
      formData.append('file', fileObj.value)
      formData.append('key', key.value)

      try {
        const response = await fetch('/api/picture/upload', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        result.value = data
      } catch (error) {
        result.value = { error: error.message }
      }
    }

    const fixQRCode = async () => {
      if (!fileObj.value) return

      const formData = new FormData()
      formData.append('file', fileObj.value)

      try {
        const response = await fetch('/api/picture/fix-qrcode', {
          method: 'POST',
          body: formData
        })

        if (response.headers.get('content-type').includes('image')) {
          const blob = await response.blob()
          fixedImage.value = URL.createObjectURL(blob)
          result.value = { status: '条形码修复成功' }
        } else {
          const data = await response.json()
          result.value = data
        }
      } catch (error) {
        result.value = { error: error.message }
        fixedImage.value = null
      }
    }

    return {
      key,
      result,
      fileObj,
      fixedImage,
      setFile,
      processImage,
      fixQRCode
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.input-group {
  margin: 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-group label {
  min-width: 60px;
}

.input-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

.key {
  font-weight: bold;
  width: 200px;
  vertical-align: top;
}

.value {
  word-break: break-all;
  font-family: monospace;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.image-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.image-result img {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}
</style>
