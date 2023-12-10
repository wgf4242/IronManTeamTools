<template>
  <div id="app">
    <h1>解码工具</h1>

    <div>
      <input v-model="enc" @keyup="test" @change="test">
    </div>
    <button @click="test">Decode</button>
    <table>
      <tr v-for="(v, k, i) in plain">
        <td>{{ k }}</td>
        <td>{{ v }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: "Temp",
  setup() {
    const enc = ref('');
    const plain = ref('')
    const copy = () => {
      var text_to_copy = document.getElementById("textcopy")?.innerHTML;

      if (!navigator.clipboard) {/* use old commandExec() way */
      } else {
        navigator.clipboard.writeText(text_to_copy)
          .then(() => alert("copy to clipboard done!"))
          .catch(() => alert("err"))
      }
    }
    const test = () => {
      fetch('http://127.0.0.1:8000/test', {
        method: 'POST',
        body: enc.value
      }).then(res => {
        return res.json()
      }).then(r => plain.value = r)
    }
    console.log('123')
    return { test, copy, enc, plain }
  }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
}

td {
  border: 1px solid;
  white-space: pre;
}

td:nth-child(1) {
  width: 120px;
}

body,
td {
  font-family: ui-monospace, "Cascadia Mono", "Segoe UI Mono", "Liberation Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 19px;
  font-weight: 400;
  line-height: 1.5em;
}
</style>

