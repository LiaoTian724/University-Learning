
<script>
export default {
    data() {
        return {
            message: 'Hello Vue!',
            count: 0
        };
    }
};
</script>

<template>
    <h1>{{ message }}</h1>

    <p>Count: {{ count }}</p>

    <button @click='count++'> Add 1 </button>
</template>