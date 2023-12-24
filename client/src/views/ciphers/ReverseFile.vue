<template>
  <h1>文件二进制反向</h1>
  <h2>拖入文件会自动生成反序文件并用资源管理器打开目录</h2>
  <FileDropComponent @changeObj="download"/>
  <input type="text">
  <button @click="download()">Download</button>

  <pre>{{ result }}
  </pre>

</template>

<script>
import FileDropComponent from "@/components/FileDropComponent.vue";
import {ref} from "vue";
import {reverse_file} from "@/api/index.js";


export default {
  name: "ReverseFile",
  components: {FileDropComponent},
  setup() {
    const result = ref('');
    const file= ref('')

    const download1 = async fileObj => {
      console.log('fileObj', fileObj)
      const formData = new FormData();
      formData.append('file', fileObj);
      const [blobPromise, filename] = await reverse_file(formData)
      const blob = await blobPromise;

      // 处理文件下载
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    const download = async fileObj => {
      if(!fileObj && file.value){
        // if (!fileObj && file.value) {
        fileObj = file.value
      }
      const formData = new FormData();
      formData.append('file', fileObj);
      file.value = fileObj
      await reverse_file(formData)
    }

    return {result, download}
  }
}
</script>
