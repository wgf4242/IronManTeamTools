<script setup>
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>

  <div id="container">
    <div id="left">
      <div class="item">Search</div>
      <ul>
        <li>
          <input type="text" placeholder="Search">
        </li>
        <li class="item bg-white">工具列表</li>
        <RouterLink to="/common">  <li class="item">常规解码</li></RouterLink>
        <RouterLink to="/aes"><li class="item">AES/DES/3DES/Rabbit</li></RouterLink>
        <RouterLink to="/lsb"><li class="item">LSB</li></RouterLink>
        <RouterLink to="/frequency"><li class="item">词频统计</li></RouterLink>
        <RouterLink to="/coordinate"><li class="item">Draw Coordinate</li></RouterLink>
        <li class="item"></li>
        <li class="item"></li>
      </ul>
    </div>
<!--    <div id="center">-->
<!--      Tool2-->
<!--    </div>-->
    <div id="right">
      <div class="right-container">
        <RouterView />
      </div>

    </div>
  </div>


<!--  <header>-->
<!--     <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->
<!--    <div class="wrapper">-->
<!--       <HelloWorld msg="You did it!" /> -->
<!--      <nav><RouterLink to="/">Home</RouterLink></nav>-->
<!--    </div>-->
<!--  </header>-->


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

/*#center {*/
/*  width: 100px;*/
/*  !*background: #515050;*!*/
/*  border: 1px solid #eee;*/
/*}*/

#right {
  flex: 1;
  /*background: #0a0;*/
  border: 1px solid #eee;
  /* height: 100vh;overflow: hidden; */
  overflow: hidden;
}
#right > :first-child  {
  max-height: 100vh;
  height: 100%;
  overflow: auto;

}

#left ul {
  padding: 0;
}
a,a:visited{
  color: unset;
  text-decoration: none;
}

</style>
