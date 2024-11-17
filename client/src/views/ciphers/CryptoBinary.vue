<template>
  <h1>只存在2种字符时(自动删除空格)，会将二进制转为字符串</h1>
  <p>
    <button @click="handleBinary(result)">二进制测试</button>
  </p>
  <FileDropComponent @blob="handleBlob" @change="test"/>

  <pre>{{ result }}</pre>
  <pre>{{ resultBlob }}</pre>

</template>

<script>
import FileDropComponent from "@/components/FileDropComponent.vue";
import {ref} from "vue";
import { binfuzz } from '@/api/index.js'


export default {
  name: "CryptoBinary",
  components: {FileDropComponent},
  setup() {
    const result = ref('');

    const checkMorse = (data) => {
      // data 每2个字符切分为1 组
      const data1 = data.match(/.{1,2}/g)
      if (new Set(data1).size === 3 || new Set(data).size === 3) {
        return 'Morse Code'
      }
      return 'Not morse Code';
    }
    const handleBinary = data => {
      // 判断字符串是否只包含两种字符
      data = data.replaceAll(' ', '')
      let uniqueChars = [...new Set(data)];

      let isMorse = checkMorse(data)
      if (isMorse) {
        return isMorse
      }

      if (uniqueChars.length !== 2) {
        return '字符串不符合要求';
      }
      const [char1, char2] = uniqueChars;
      let str2 = data.replaceAll(char1, '1').replaceAll(char2, '0')
      let str1 = data.replaceAll(char1, '0').replaceAll(char2, '1')

      function fromBinary(string) {
        const paddedString = string.padEnd(Math.ceil(string.length / 8) * 8, '0');
        const arr = [...paddedString.matchAll(/\d{8}/g)].map(e => e[0])
        return arr.map(e => {
          let number = parseInt(e, 2);
          return String.fromCharCode(number);
        }).join('')
      }

      return [fromBinary(str1), fromBinary(str2)].join('\n');
    }
    const test = (data) => {
      result.value = handleBinary(data);
    }
    const resultBlob = ref('')
    const handleBlob = async (data) => {
      resultBlob.value = await binfuzz(data)
    }
    return {test, handleBinary, result, handleBlob, resultBlob}
  }
}
</script>

<style scoped>
</style>
