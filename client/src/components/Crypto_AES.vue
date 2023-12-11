<template>
  <input v-model="enc" type="text" placeholder="输入密文">
  <input v-model="key" type="text" placeholder="KEY">
  <input v-model="iv" type="text" placeholder="IV">
  <p>
    <button @click="submit">Decrypt</button>
  </p>

  <table>
    <tr>
      <td>AES:</td>
      <td>{{ plain }}</td>
    </tr>
  </table>

  <div class="mt30">字典爆破

    <p>字典放到: wordlists 下</p>
  </div>

  <table>
    <tr>
      <td>AES:</td>
      <td>选择字典
        <select v-model="select">
          <option v-for="item in wordlists" :key="item">{{ item }}</option>
        </select>
      </td>
      <td>
        <button @click="submitBatch">开始爆破</button>
      </td>
      <td>结果: {{ plain }}</td>
    </tr>
  </table>

</template>

<script>
import {ref, onMounted} from "vue";
import {decryptAes, getWordlists} from '@/api'

export default {
  name: "Crypto_AES",
  setup() {
    const plain = ref('');
    const enc = ref('');
    const key = ref('')
    const iv = ref('')

    const wordlists = ref([])
    const select = ref('')

    onMounted(async () => {
      let tmp = await getWordlists();
      wordlists.value = tmp;
      select.value = tmp.length ?  tmp[0] : '';
    })

    const submitBatch = () => {
      const data = {
        enc: enc.value,
        file: select.value
      }
      decryptAes(data).then(r => {
        plain.value = r
      })
    }
    const submit = () => {
      const data = {
        enc: enc.value,
        key: key.value,
        iv: iv.value
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
    return {
      submit, enc, key, iv, plain, wordlists, submitBatch,
      select
    }
  }
}
</script>

<style scoped>
table {
  border: 1px solid #eee;
}

td:nth-child(1),
td:nth-child(2),
td:nth-child(4) {
  width: 300px;
}

select {
  width: 100px;
}
</style>
