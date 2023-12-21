<template>
  <h1>词频统计</h1>

  <div id="dropZone"
       @dragover.prevent
       @drop="handleDrop"
  >将文件拖拽到此处
  </div>
  <div>文件信息: <span class="red">{{ fileObj?.name }}</span></div>
  <!--  <input v-model="key" type="text" placeholder="KEY">-->
  <!--  <p><button @click="submit">Decrypt</button></p>-->
  <button @click="submitWord(0)">统计单词</button>
  <button @click="submitChars(1)" class="ml30">统计字符</button>
  <button @click="reverse" class="ml30">反序</button>


  <pre>{{ plain }}</pre>


</template>

<script>
import {ref} from "vue";
import {WordFrequecy} from "@/api/index.js";

export default {
  name: "FrequencyComponent",
  setup() {
    const plain = ref('');
    const enc = ref('');
    const fileObj = ref(null);
    const is_count_char = ref(0)

    const submitWord = (char = 1) => {
      is_count_char.value = char;
      console.log('char', char, 'is', is_count_char.value)

      const formData = new FormData();
      formData.append('file', fileObj.value);
      formData.append('is_count_char', is_count_char.value.toString());
      WordFrequecy(formData).then(res => {
        plain.value = res;
      })
    }
    const submitChars = (char = 0) => {
      submitWord(char)
    }

    const handleDrop = (event) => {
      event.preventDefault();

      const files = event.dataTransfer.files;
      if (files.length > 0) {
        const file = files[0];
        fileObj.value = file;

        submitWord()
      }
    }

    const reverse = () => {
      plain.value = plain.value.split('\n').reverse().join('\n')
    }
    return {
      enc, plain, submitWord,
      handleDrop,
      fileObj,
      reverse, is_count_char,
      submitChars,
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
