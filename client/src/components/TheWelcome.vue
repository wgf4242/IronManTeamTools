<script setup>
import Temp from "./Temp.vue";

</script>

<template>
  <div id="container">
    <div id="left">
      <div class="item">Search</div>
      <ul>
        <li>
          <input type="text" placeholder="Search">
        </li>
        <li class="item white">工具列表</li>
        <li class="item">常规解码</li>
        <li class="item">AES</li>
        <li class="item"></li>
        <li class="item"></li>
      </ul>
    </div>
    <div id="center">
      Tool2
    </div>
    <div id="right">
      <Temp />
    </div>
  </div>
</template>

<style scoped>

body {
  margin: 0;
  padding: 0;
  font-weight: bold;
  font-size: 20px;
}

#header,
#footer {
  background: #eee;
  text-align: center;
  height: 60px;
  line-height: 60px;
}

#container {
  display: flex;
  height: calc(100vh - 120px);
}

#left {
  width: 300px;
  /*background: #f00;*/
  border: 1px solid #eee;
}

#center {
  width: 100px;
  /*background: #515050;*/
  border: 1px solid #eee;
}

#right {
  flex: 1;
  /*background: #0a0;*/
  border: 1px solid #eee;
  /* height: 100vh;overflow: hidden; */
}

#left ul {
  padding: 0;
}
</style>
