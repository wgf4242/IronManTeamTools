<script setup>
import { computed, ref } from 'vue'

const get_value = ref('')

const url_encoding= computed(() => encodeURIComponent(get_value.value))


</script>

<template>
  <p>Get 请求转码:</p>
  <div> <textarea v-model="get_value"/></div>
  <p>转码结果:</p>
  <div> <textarea v-model="url_encoding"/></div>
</template>

<style scoped>

textarea {
  width: 80%;
  height: 40px;
}
</style>
