<template>
  <el-card>
    <template #header>Properties / Attributes</template>
    <comp-part1></comp-part1>
  </el-card> 

  <el-card>
    <template #header>Bi-directional Binding</template>
    <comp-part2></comp-part2>
  </el-card> 

  <el-card>
    <template #header>Slots</template>
    <comp-part3></comp-part3>
  </el-card> 
</template>

<script>
import { ElCard } from "element-plus";
import 'element-plus/dist/index.css';

import CompPart1 from "./comp01.vue";
import CompPart2 from "./comp02.vue";
import CompPart3 from "./comp03.vue";

export default {
  components: { ElCard, CompPart1, CompPart2, CompPart3 }
};
</script>

<style scoped>
.el-card { margin-bottom: 1em; }
</style>
  