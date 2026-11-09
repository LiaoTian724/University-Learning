
<template>
    <button @click='$emit("action")'>
        {{ label }}
    </button>
</template>

<script>
    export default {
        // 组件可以从父组件接收一个 label 属性
        // 组件声明了一个自定义事件，名称为 action。这里的 action 是我们自己取的名称，不是 Vue 内置的固定事件
        props: ['label'],
        emits: ['action']
    }
</script>

<style scoped>
    button {
        padding: 8px 15px;
        margin-right: 10px;
        cursor: pointer;
    }
</style>