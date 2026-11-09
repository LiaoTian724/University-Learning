

<template>
    <div class="page">

        <h1>Page74 - Vue API Comparison</h1>

        <CounterOptions />
        <CounterComposition />
    </div>
</template>

<script setup>
    import CounterOptions from './components/CounterOptions.vue';
    import CounterComposition from './components/CounterComposition.vue';
    
    // script set 会自动注册, 不需要写下面的内容
    // export default {
    //     components: {
    //         CounterOptions,
    //         CounterComposition
    //     }
    // };
</script>


<style scoped>
.page {
    font-family: Arial, sans-serif;
    margin: 30px;
}
</style>