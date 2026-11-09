
<template>
    <div class="counter">
        <h2>Composition API Counter</h2>

        <p>Count is: {{  count  }}</p>

        <button @click="increment">Add 1</button>
        <button v-on:click="reset">Reset</button>
    </div>
</template>


<script setup>
    import {ref, onMounted} from 'vue';

    const count = ref(0);

    function increment() {
        count.value++;
    }
    function reset() {
        count.value = 0;
    }

    onMounted(() => {
        console.log(`Composition API initial count: ${count.value}`);
    })
</script>

<style scoped>
.counter {
    border: 1px solid gray;
    border-radius: 6px;
    padding: 15px;
    margin: 10px 0;
}

button {
    margin-right: 10px;
    padding: 6px 12px;
}
</style>