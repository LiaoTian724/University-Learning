<template>
  Task:
  <el-input placeholder="Enter the task" v-model="taskName"></el-input>

  Due date: 
  <el-date-picker v-model="dueDate" type="date"></el-date-picker>
  <div>The task "{{ taskName }}" is due in {{ dueDateFromNow }} days.</div>
</template>

<script>
import { ElInput, ElDatePicker } from "element-plus";
import 'element-plus/dist/index.css';

export default {
  components: { ElInput, ElDatePicker },
  data() {
    return {
      taskName: '', 
      dueDate: new Date(), 
    };
  },
  computed: {
    dueDateFromNow() { 
      const oneDay = 1000 * 60 * 60 * 24;
      const today = new Date();
      let diff = (this.dueDate.getTime() - today.getTime()) / oneDay;
      return Math.ceil(diff);
    }
  }
}
</script>

<style scoped>
.el-input, .el-date-picker, div { width: 300px; margin: 10px 10px; }
</style>