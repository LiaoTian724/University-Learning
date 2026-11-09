<template>
   <el-input placeholder="what's up?"
      v-model="message"></el-input>

   <el-progress :text-inside="true" :stroke-width="30"
                :percentage="progress" :color="customColors">     
   </el-progress>

   <el-button type="primary" @click="changeProgress">Change progress</el-button>
</template>

<script>
import { ElInput, ElProgress, ElButton } from "element-plus";
import 'element-plus/dist/index.css';

export default {
  components: { ElInput, ElProgress, ElButton },
  data() {
    return {
      message: 'Welcome to Vue!', progress: 70,
      customColors: [
        { color: '#f56c6c', percentage: 20 },
        { color: '#e6a23c', percentage: 40 },
        { color: '#5cb87a', percentage: 60 },
        { color: '#1989fa', percentage: 80 },
        { color: '#6f7ad3', percentage: 100 },
      ]
    };
  },
  methods: {
    changeProgress() { 
      this.progress += 10; 
      if (this.progress > 100) this.progress = 0; 
    }
  }
}
</script>

<style scoped>
.el-input, .el-progress { width: 300px; margin: 10px 10px; }
</style>