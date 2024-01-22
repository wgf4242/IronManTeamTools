<template>
  <div>
    <input v-model="enc" @keyup="submit" @change="submit">
  </div>
  <button @click="submit">Decrypt</button>
  <table>
    <tr v-for="(v, k, i) in plain">
      <td>{{ k }}</td>
      <td>{{ v }}</td>
    </tr>
  </table>
</template>

<script>
import {ref} from 'vue';
import RailFenceCipherTypeMDecode from "@/js/ciphers/RailFenceCipherDecodeMType.mjs";

export default {
  name: "TempComponent",
  setup() {
    let railFenceM = new RailFenceCipherTypeMDecode();
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

    function getRailFenceM(value) {
      let result = ''
      for (let i = 2; i < 10; i++) {
        result += railFenceM.run(value, [i, 0]) + "\n";
      }
      return result.trim();
    }

    const submit = () => {
      let rail_fence_M_d_Value = getRailFenceM(enc.value);

      fetch('http://127.0.0.1:8000/test', {
        method: 'POST',
        body: enc.value
      }).then(res => {
        return res.json()
      }).then(r => {
        let obj = {...r, rail_fence_M_d: rail_fence_M_d_Value};
        const sortedObj = {};
        Object.keys(obj).sort().forEach(key => {
          sortedObj[key] = obj[key];
        });

        plain.value = sortedObj;
      })
    }
    console.log('123')
    return {submit, copy, enc, plain}
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

