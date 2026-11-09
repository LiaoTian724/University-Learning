


<template>
    <div class="counter">
        <h2>Options API Counter</h2>

        <p>Count is: {{  count  }}</p>

        <button @click="increment">Add 1</button>
        <button v-on:click="reset">Reset</button>
    </div>
</template>



<script>
    export default {
        data() {
            return {
                count: 0
            };
        },

        methods: {
            increment() {
                this.count++;
            },
            reset() {
                this.count = 0;
            }
        },

        mounted(){
            console.log(`Options API initial count: ${this.count}`);
        }
    }
</script>



<style scoped>
.counter {
    border: 1px solid gray;
    border-radius: 6px;
    padding: 15px;
    margin: 10px 0;
}
</style>