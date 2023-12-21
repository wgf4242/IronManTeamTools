<template>
  <h1>LSB-cloacked-pixel</h1>

  <div id="dropZone"
       @dragover.prevent
       @drop="handleDrop"
  >将文件拖拽到此处
  </div>
  <div>文件信息: <span class="red">{{ fileObj?.name }}</span> </div>
  <!--  <input v-model="key" type="text" placeholder="KEY">-->
<!--  <p><button @click="submit">Decrypt</button></p>-->

  <table>
    <tr>
      <td>LSB-cloacked-pixel</td>
      <td>{{ plain }}</td>
    </tr>
  </table>

  <div class="mt30">字典爆破
    <p>字典放到: wordlists 下</p>
  </div>

  <table>
    <tr>
      <td>clock_pixel_lsb:</td>
      <td>选择字典
        <select v-model="select">
          <option v-for="item in wordlists" :key="item">{{ item }}</option>
        </select>
      </td>
      <td>
        <button @click="submitBatch">开始爆破</button>
      </td>
      <td>
        <pre>{{clock_pixel_lsb}}</pre>
      </td>
    </tr>
  </table>

</template>

<script>
import {ref, onMounted} from "vue";
import {decryptAes, decryptLSBAes, getWordlists} from '@/api/index.js'

export default {
  name: "Crypto_AES",
  setup() {
    const plain = ref('');
    const enc = ref('');
    const key = ref('');
    const clock_pixel_lsb = ref('');
    const fileObj = ref(null);

    const wordlists = ref([])
    const select = ref('')

    onMounted(async () => {
      let tmp = await getWordlists();
      wordlists.value = tmp;
      select.value = tmp.length ? tmp[0] : '';
    })


    const submitBatch = () => {

      const formData = new FormData();

      // formData.append('enc', enc.value);
      formData.append('wordlist', select.value);
      formData.append('file', fileObj.value);
      decryptLSBAes(formData).then(r => {
        clock_pixel_lsb.value = r
      })
    }
    const submit = () => {
      const data = {
        enc: enc.value,
      }

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      };
      fetch('http://127.0.0.1:8000/api/aes', requestOptions)
          .then(res => res.text()).catch(e => console.log(e))
          .then(r => plain.value = r).catch(e => plain.value = '失败');
    }

    const handleDrop = (event) => {
      event.preventDefault();

      const files = event.dataTransfer.files;
      if (files.length > 0) {
        const file = files[0];
        fileObj.value = file;
        // const reader = new FileReader();
        // reader.onload = (e) => {
        //   const fileContent = e.target.result;
        //   console.log(fileContent); // 在控制台输出文件内容
        // };
        // reader.readAsText(file);
      }
    }
    return {
      submit, enc, plain, wordlists, submitBatch,
      select, key,
      handleDrop,
      fileObj,
      clock_pixel_lsb,
    }
  }
}
</script>

<style scoped>

#dropZone {
  width: 300px;
  height: 300px;
  border: 2px dashed #ccc;
  text-align: center;
  padding: 10px;
  font-size: 18px;
}
</style>
