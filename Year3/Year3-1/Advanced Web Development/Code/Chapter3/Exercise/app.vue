<!-- the root component in a Vue SFC -->

<template>
The time now is 
<div class='clock'>{{ timeNow }}</div>
</template>

<script>
export default {
  data() {
    return { timeNow: undefined }
  },
  mounted() {
    this.timeNow = (new Date()).toLocaleTimeString();
    setInterval(() => {
      this.timeNow = (new Date()).toLocaleTimeString();
    }, 1000);
  }
  // the template property is rewritten as a template element above
};
</script>

<style scoped>
.clock { padding: 2px; width: 6em; border: 1px solid gray; text-align: center; }
</style>