
<template>
    <div>
        <p>Count: {{ count }}</p>

        <button @click='count++'>Add 1</button>
        <button v-on:click='reset'>Reset</button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                count: 0
            }
        },

        methods: {
            reset() {
                this.count = 0;
            }
        }
    }
</script>