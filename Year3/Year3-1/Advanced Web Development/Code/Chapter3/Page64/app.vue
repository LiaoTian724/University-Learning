<template>
    <div class="page">

        <h1>Page64 - Component Events</h1>

        <p>Parent Count: {{ count }}</p>

        <CustomButton
            label="Add 1"
            @action="count++"
        />

        <CustomButton
            label="Minus 1"
            @action="count--"
        />

        <CustomButton
            label="Reset"
            @action="reset"
        />


    </div>

    <AlertBox>Something bad happened!</AlertBox>

    <MyCard>
        <template #header>
            My Title
            <!-- My Title 传递给命名卡槽 header-->
        </template>
        <p>Hello Vue!</p>
        <!-- Hello Vue! 传递给默认卡槽 -->
    </MyCard>

</template>


<script>
    import CustomButton from './components/CustomButton.vue';
    import AlertBox from './components/AlertBox.vue';
    import MyCard from './components/MyCard.vue';
    
    export default {

        components: {
            CustomButton,
            AlertBox,
            MyCard
        },

        data() {
            return {
                count: 10
            };
        },

        methods: {
            reset() {
                this.count = 0;
            }
        }

    };
</script>

<style scoped>
    .page {
        font-family: Arial, sans-serif;
        margin: 30px;
    }

    button {
        margin-right: 10px;
    }
</style>