<template>
    <div class="alert-box">
        <strong>This is an Error for Demo Purposes </strong>
    
        <slot />
    </div>
</template>

<style scoped>
    .alert-box {
        border: 1px solid red;
        background-color: lightpink;
        padding: 15px;
        margin: 10px;
    }
</style>