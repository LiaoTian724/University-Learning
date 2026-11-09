<!-- Page63 -->
<template>
    <div>
        <h4>{{ title }}</h4>
    </div>
</template>

<script>

// 这个组件可以接收一个来自父组件的属性，名称叫 title
// 这个 title 是我们自己定义的，不是 Vue 强制要求必须叫 title
    export default {
        props: ['title']
    }
</script>

<style scoped>
    h4 {
        color: #42b983;
    }
</style>