<template>
  <div id="dropZone"
       @dragover.prevent
       @drop="handleDrop"
  >将文件拖拽到此处
  </div>
  <div>文件信息: <span class="red">{{ fileObj?.name }}</span></div>

</template>

<script>
import {ref} from "vue";

function arrayBufferToAscii(buffer) {
  const decoder = new TextDecoder('ascii'); // 使用 ASCII 编码
  return decoder.decode(buffer);
}


export default {
  name: "FileDropComponent",
  emits: ['change', 'changeObj'],
  setup(props, ctx) {
    const fileObj = ref(null);

    const handleDrop = (event) => {
      event.preventDefault();

      const files = event.dataTransfer.files;
      if (files.length > 0) {
        const file = files[0];
        fileObj.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          const fileContent = e.target.result;
          ctx.emit('change', arrayBufferToAscii(fileContent));
          ctx.emit('blob', fileContent);
          ctx.emit('changeObj', fileObj.value);
        };
        // reader.readAsText(file);
        reader.readAsArrayBuffer(file);
      }
    }

    return {handleDrop, fileObj}
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
