<!-- the root component in a Vue SFC -->

<template>
The time now is 
<div class='clock'>{{ timeNow }}</div>
<button type="button" @click="resetClockDisplay">Reset!</button>
</template>

<script setup>
import { ref, onMounted } from "vue";

const timeNow = ref(undefined);

onMounted(() => {
  timeNow.value = (new Date()).toLocaleTimeString();
  setInterval(() => {
      timeNow.value = (new Date()).toLocaleTimeString();
    }, 1000);
});

function resetClockDisplay(event) {
  timeNow.value = "Reset Display"
}
</script>

<style scoped>
.clock { padding: 2px; width: 6em; border: 1px solid gray; text-align: center; }
</style>