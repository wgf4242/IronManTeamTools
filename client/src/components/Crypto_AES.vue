<template>
  <p>8位以上字符能显示</p>
  <input v-model="enc" type="text" placeholder="输入密文">
  <input v-model="key" type="text" placeholder="KEY">
  <input v-model="iv" type="text" placeholder="IV">

  <table>
    <tr v-for="alg in ['AES','DES', 'RABBIT']" :key="alg">
      <td><button @click="submit(alg)">Decrypt</button></td>
      <td>{{ alg }}:</td>
      <td>{{ plains?.[alg] }}</td>
    </tr>
  </table>

  <div class="mt30">字典爆破: 字典放到: wordlists 下</div>

  <table class="content">
    <tr v-for="alg in ['AES','DES', 'RABBIT']" :key="alg">
      <td>{{ alg }}:</td>
      <td>选择字典<select v-model="select">
        <option v-for="item in wordlists" :key="item">{{ item }}</option>
      </select></td>
      <td>
        <button @click="submitBatch(alg)">开始爆破</button>
      </td>
      <td>结果: {{ plains?.[alg] }}</td>
    </tr>
  </table>

</template>

<script>
import {ref, onMounted, reactive} from "vue";
import {decryptAes, getWordlists} from '@/api'

export default {
  name: "Crypto_AES",
  setup() {
    const plains = reactive({});
    const enc = ref('');
    const key = ref('')
    const iv = ref('')

    const wordlists = ref([])
    const select = ref('')

    onMounted(async () => {
      let tmp = await getWordlists();
      wordlists.value = tmp;
      select.value = tmp.length ? tmp[0] : '';
    })

    const submitBatch = (ALG = 'AES') => {
      const data = {
        enc: enc.value,
        file: select.value,
        alg: ALG
      }
      decryptAes(data).then(r => {
        plains[ALG] = r
      })
    }
    const submit = (ALG = 'AES') => {
      const data = {
        enc: enc.value,
        key: key.value,
        iv: iv.value,
        alg: ALG
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
          .then(r => {
            plains[ALG] = r
          }).catch(e => plains[ALG] = '失败');
    }
    return {
      submit, enc, key, iv,  wordlists, submitBatch, plains, select
    }
  }
}
</script>

<style scoped>
table {
  border: 1px solid #eee;
}

.content td:nth-child(1),
.content td:nth-child(2),
.content td:nth-child(4) {
  width: 300px;
}

select {
  width: 100px;
}
</style>
