<script setup>
import { computed, ref } from 'vue'

const get_value = ref('')
const url_encoding= computed(() => encodeURIComponent(get_value.value))
const shell_bypass = computed(() => {
  const map  ={
    ' ': '$IFS$9',
    '>': '${PS2}',
    '+': '${PS4}',
    "\t": "${9}",
  }
  // replace get_value.value with  map replace  key to value
  let value = get_value.value;
  Object.entries(map).forEach(([k, v]) => {
    value = value.replaceAll(k, v)
  })
  return value;
})
const php_bypass = computed(() => encodeURIComponent(get_value.value))

</script>

<template>
  <p>Input</p>
  <div> <textarea v-model="get_value"/></div>
  <p>Shell</p>
  <div> <textarea v-model="shell_bypass"/></div>
  <p>PHP</p>
  <div> <textarea v-model="php_bypass"/></div>
</template>

<style scoped>

textarea {
  width: 80%;
  height: 40px;
}
</style>
